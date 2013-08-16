
class Duplicate(object):
    
    def __init__(self, fileOne, fileTwo):
        self.fileOne = fileOne
        self.fileTwo = fileTwo

    def __str__(self):
        return 'Duplicate found: {0} and {1}\n\n'.format(self.fileOne, self.fileTwo)