#!/usr/bin/env python

import sys
import os
import hashlib

from duplicatecollector import DuplicateCollector
from progressbar import AnimatedProgressBar

class Scanner(object):
    
    def __init__(self, path):
        self.path = path
        
    def scan(self, duplicateCollector = None):
        if not duplicateCollector:
            duplicateCollector = DuplicateCollector()

        if self.path:
            self.checkForDuplicates(self.path, duplicateCollector)
        else:
            print('No path specified')
    
    def checkForDuplicates(self, path, duplicateCollector, hash = hashlib.sha1):
        hashes = {}
        progressBar = AnimatedProgressBar(end = self._getFileCount(path))
        progressBar.show_progress()
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                progressBar + 1
                fullPath = os.path.join(dirpath, filename)
                hashObj = hash()
                for chunk in self.chunkReader(open(fullPath, 'rb')):
                    hashObj.update(chunk)
                fileID = (hashObj.digest(), os.path.getsize(fullPath))
                duplicate = hashes.get(fileID, None)
                if duplicate:
                    duplicateCollector.add(fullPath, duplicate)
                    # print 'Duplicate found: %s and %s' %(fullPath, duplicate)
                else:
                    hashes[fileID] = fullPath
                progressBar.show_progress()
        progressBar.done()

    
    def chunkReader(self, file, chunkSize = 1024):
        while True:
            chunk = file.read(chunkSize)
            if not chunk:
                return
            yield chunk

    def _getFileCount(self, path):
        count = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                count = count + 1

        return count
    