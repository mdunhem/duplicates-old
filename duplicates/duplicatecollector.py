import os

from duplicate import Duplicate

class DuplicateCollector(object):

    def __init__(self):
        self.collection = []

    def add(self, fileOne, fileTwo):
        duplicate = Duplicate(fileOne, fileTwo)
        self.collection.append(duplicate)

    def write(self, shouldPrintToScreen = False):
        if shouldPrintToScreen:
            self._printToScreen()
        else:
            self._writeToFile()

    def _printToScreen(self):
        if len(self.collection) == 0:
            print 'No duplicates found'
        else:
            for duplicate in self.collection:
                print 'Duplicate found: %s and %s' %(duplicate.fileOne, duplicate.fileTwo)

    def _writeToFile(self):
        if len(self.collection) == 0:
            print 'No duplicates found'
        else:
            with open('DuplicatesFound.txt', 'w') as file:
                for duplicate in self.collection:
                    file.write('Duplicate found: %s and %s\n\n' %(duplicate.fileOne, duplicate.fileTwo))
