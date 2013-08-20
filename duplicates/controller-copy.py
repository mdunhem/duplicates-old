import view
import model
import utility
import event
import options
import Queue
import os
import sys

class Controller:
    def __init__(self, option = None):
        if option and isinstance(option, options.Options):
            self.options = option
        else:
            self.options = options.Options()
        self._initProperties()

    def _initProperties(self):
        parsedOptions = self.options.parse()
        self.path = parsedOptions.path
        # self.recursive = parsedOptions.recursive
        # self.display = parsedOptions.display
        # self.write = parsedOptions.write

        self.filesQueue = Queue.Queue()
        self.count = 0

        self.eventDispatcher = event.EventDispatcher()
        self.view = view.CommandLineView()
        self.duplicates = model.Duplicate()

        self._createFilesQueue()

    def run(self):
        while not self.filesQueue.empty():
            file = self.filesQueue.get()
            filePath = os.path.join(self.root, file)
            self.duplicates.add(filePath)

        for files in self.duplicates.duplicatesList:
            self.view.output('#########')
            self.view.output('\n')
            self.view.output(files)
            self.view.output('\n')
            for file in self.duplicates.duplicatesList[files]:
                self.view.output(file)
                self.view.output('\n')

    def _createFilesQueue(self):
        for root, directories, files in os.walk(self.path):
            self.root = root
            for file in files:
                sys.stdout.write('\r')
                sys.stdout.write('Counting files: {0}'.format(str(self.count)))
                sys.stdout.flush()
                self.filesQueue.put(file)
                self.count = self.count + 1
        sys.stdout.write('   done.\n')