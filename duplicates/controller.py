#!/usr/bin/env python

import sys
import os
import hashlib
import Queue

from threading import Thread
from options import Options
from duplicate import Duplicate
from view import ProgressBar

class Controller:
    def __init__(self, options = None):
        if options and isinstance(options, Options):
            self.options = options
        else:
            self.options = Options()

        self._initProperties()

    def run(self):
        try:
            searchForDuplicatesThread = SearchForDuplicatesThread(self.filesQueue, self.duplicatesQueue, self.root)
            searchForDuplicatesThread.start()
            searchForDuplicatesThread.join()
            # traverseFilesThread = Thread(target = self._createFilesList)
            # traverseFilesThread.start()
            # traverseFilesThread.join()

            # thread = Thread(target = self._checkForDuplicates)
            # thread.start()
            # thread.join()
        except Exception, errtxt:
            print errtxt
        finally:
            self.writeResults()

    def writeResults(self):
        if self.display:
            self._printToScreen()

        if self.write:
            self._writeToFile()

    # ----------------------
    # Private Methods
    # ----------------------

    def _initProperties(self):
        parsedOptions = self.options.parse()
        self.path = parsedOptions.path
        self.recursive = parsedOptions.recursive
        # self.verbose = parsedOptions.verbose
        self.display = parsedOptions.display
        self.write = parsedOptions.write

        self.duplicates = []

        self.filesQueue = Queue.Queue()
        self.duplicatesQueue = Queue.Queue()
        self.count = 0

        self._createFilesQueue()

        self._createFilesList()

        self.progressBar = ProgressBar()
        self.progressBar.end = self.fileCount

    def _checkForDuplicates(self):
        hashes = {}
        self.progressBar.displayProgress()
        for file in self.files:
            self.progressBar.increment()
            try:
                filePath = os.path.join(self.root, file)
                hasher = hashlib.sha1()
                for chunk in self._getChunk(filePath):
                    hasher.update(chunk)
                fileID = (hasher.digest(), os.path.getsize(filePath))
                duplicate = hashes.get(fileID)
                if duplicate:
                    self._addDuplicate(filePath, duplicate)
                else:
                    hashes[fileID] = filePath
            except Exception, e:
                pass # For now, no need to do anything besides suppress any errors
            finally:
                self.progressBar.displayProgress()
        self.progressBar.done()

    def _createFilesQueue(self):
        for root, directories, files in os.walk(self.path):
            self.root = root
            for file in files:
                self.filesQueue.put(file)
                self.count = self.count + 1

    def _createFilesList(self):
        self.files = []
        self.fileCount = 0
        for root, directories, files in os.walk(self.path):
            self.root = root
            for file in files:
                self.files.append(file)
                self.fileCount = self.fileCount + 1

    def _addDuplicate(self, fileOne, fileTwo):
        self.duplicates.append(Duplicate(fileOne, fileTwo))

    def _getChunk(self, filePath, chunkSize = 1024):
        file = open(filePath, 'rb')
        while True:
            chunk = file.read(chunkSize)
            if not chunk:
                return
            yield chunk

    def _getFileCount(self):
        count = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                count = count + 1

        return count

    def _printToScreen(self):
        if self.duplicatesQueue.empty():
            print 'No duplicates found'
        else:
            while not self.duplicatesQueue.empty():
                print str(self.duplicatesQueue.get())
        # if len(self.duplicates) == 0:
        #     print 'No duplicates found'
        # else:
        #     for duplicate in self.duplicates:
        #         print str(duplicate)

    def _writeToFile(self):
        if self.duplicatesQueue.empty():
            print 'No duplicates found'
        else:
            print 'Found {0} duplicates'.format(str(self.duplicatesQueue.qsize()))
            with open('DuplicatesFound.txt', 'w') as file:
                while not self.duplicatesQueue.empty():
                    file.write(str(self.duplicatesQueue.get()))

        # if len(self.duplicates) == 0:
        #     print 'No duplicates found'
        # else:
        #     print 'Found {0} duplicates'.format(str(len(self.duplicates)))
        #     with open('DuplicatesFound.txt', 'w') as file:
        #         for duplicate in self.duplicates:
        #             file.write(str(duplicate))

class SearchForDuplicatesThread(Thread):
    def __init__(self, filesQueue, duplicatesQueue, root):
        super(SearchForDuplicatesThread, self).__init__()
        self.filesQueue = filesQueue
        self.duplicatesQueue = duplicatesQueue
        self.root = root
        self.progressBar = ProgressBar()
        self.progressBar.end = self.filesQueue.qsize()

    def run(self):
        hashes = {}
        self.progressBar.displayProgress()
        while not self.filesQueue.empty():
            try:
                file = self.filesQueue.get()
                self.progressBar.increment()
                filePath = os.path.join(self.root, file)
                hasher = hashlib.sha1()
                for chunk in self._getChunk(filePath):
                    hasher.update(chunk)
                fileID = (hasher.digest(), os.path.getsize(filePath))
                duplicate = hashes.get(fileID)
                if duplicate:
                    self.duplicatesQueue.put(Duplicate(filePath, duplicate))
                else:
                    hashes[fileID] = filePath
            except Exception, e:
                pass
            finally:
                self.filesQueue.task_done()
                self.progressBar.displayProgress()
        self.progressBar.done()

    def _getChunk(self, filePath, chunkSize = 1024):
        file = open(filePath, 'rb')
        while True:
            chunk = file.read(chunkSize)
            if not chunk:
                return
            yield chunk
        

class TraverseFilesThread(Thread):
    def __init__(self, queue):
        super(Thread, self).__init__()
        self.queue = queue

    def run(self):
        pass