#!/usr/bin/env python

import sys
import os
import hashlib

class Scanner(object):
    
    def __init__(self, args):
        self.path = args.path
        
    def scan(self):
        if self.path:
            self.checkForDuplicates(self.path)
        else:
            print('No path specified')
    
    def checkForDuplicates(self, paths, hash=hashlib.sha1):
        hashes = {}
        for path in paths:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    fullPath = os.path.join(dirpath, filename)
                    hashObj = hash()
                    for chunk in self.chunkReader(open(fullPath, 'rb')):
                        hashObj.update(chunk)
                    fileID = (hashObj.digest(), os.path.getsize(fullPath))
                    duplicate = hashes.get(fileID, None)
                    if duplicate:
                        print 'Duplicate found: %s and %s' %(fullPath, duplicate)
                    else:
                        hashes[fileID] = fullPath
    
    def chunkReader(self, file, chunkSize=1024):
        while True:
            chunk = file.read(chunkSize)
            if not chunk:
                return
            yield chunk
    