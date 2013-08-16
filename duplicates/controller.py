#!/usr/bin/env python

import sys
import os
import hashlib

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
            thread = Thread(target = self._checkForDuplicates)
            thread.start()
            thread.join()
        except Exception, errtxt:
            print errtxt
        finally:
            self.progressBar.done()
            if self.display:
                self._printToScreen()

            if self.write:
                self._writeToFile()

    def write(self):
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

        self.progressBar = ProgressBar()
        self.progressBar.end = self._getFileCount()

    def _checkForDuplicates(self):
        hashes = {}
        self.progressBar.displayProgress()
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                self.progressBar.increment()
                fullPath = os.path.join(dirpath, filename)
                hasher = hashlib.sha1()
                for chunk in self._getChunk(open(fullPath, 'rb')):
                    hasher.update(chunk)
                fileID = (hasher.digest(), os.path.getsize(fullPath))
                duplicate = hashes.get(fileID)
                if duplicate:
                    self._addDuplicate(fullPath, duplicate)
                else:
                    hashes[fileID] = fullPath
                self.progressBar.displayProgress()

    def _addDuplicate(self, fileOne, fileTwo):
        self.duplicates.append(Duplicate(fileOne, fileTwo))

    def _getChunk(self, file, chunkSize = 1024):
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
        if len(self.duplicates) == 0:
            print 'No duplicates found'
        else:
            for duplicate in self.duplicates:
                print str(duplicate)

    def _writeToFile(self):
        if len(self.duplicates) == 0:
            print 'No duplicates found'
        else:
            with open('DuplicatesFound.txt', 'w') as file:
                for duplicate in self.duplicates:
                    file.write(str(duplicate))


