import hashlib
import os

class Model(object):

    # -------------------------
    # Base Model Class
    # -------------------------
    
    def __init__(self):
        super(Model, self).__init__()


class Duplicate(Model):

    def __init__(self):
        super(Duplicate, self).__init__()
        self.duplicatesList = {}

    # -------------------------
    # Public API
    # -------------------------
    
    def add(self, filePath):
        if os.path.basename(filePath).startswith('.'):
            return
        fileHash = self._createFileHash(filePath)
        if not self.contains(filePath):
            self.duplicatesList[fileHash] = [filePath]

        filePathIsPresentInDict = False
        for path in self.duplicatesList[fileHash]:
            if os.path.basename(path) == os.path.basename(filePath):
                filePathIsPresentInDict = True

        if not filePathIsPresentInDict:
            self.duplicatesList[self._createFileHash(filePath)].append(filePath)
            

    def contains(self, filePath):
        if self._createFileHash(filePath) in self.duplicatesList:
            return True
        return False

    def getDuplicates(self, filePath):
        if self.contains(filePath):
            return self.duplicatesList[self._createFileHash(filePath)]
        return False

    # -------------------------
    # Private Methods
    # -------------------------

    def _createFileHash(self, filePath):
        hash = hashlib.md5()
        for chunk in self._getChunk(filePath):
            hash.update(chunk)
        return hash.digest()
    
    def _getChunk(self, filePath, chunkSize = 1024):
        with open(filePath, "rb") as file:
            while True:
                chunk = file.read(chunkSize)
                if not chunk:
                    return
                yield chunk
        