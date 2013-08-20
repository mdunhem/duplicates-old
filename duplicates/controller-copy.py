import view
import model
import thread
import event
import options
import Queue
import os
import sys
import threading

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
        self.lock = threading.Lock()
        self.count = 0

        self.eventDispatcher = event.EventDispatcher()
        self.view = view.CommandLineView()
        self.duplicates = model.Duplicate()
        
        self.running = True

    def run(self):
        try:
            self.scanFilesThread = thread.ScanFilesThread(self.filesQueue, self.path, self.eventDispatcher, self.lock)
            self.scanFilesThread.start()
            
            self.processFilesThread = thread.ProcessFilesThread(self.filesQueue, self.duplicates, self.eventDispatcher, self.lock)
            self.processFilesThread.start()
            
            # self.eventDispatcher.add('Thread.ScanFiles.Done', self._stopScanFilesThread())
            # self.eventDispatcher.add('Thread.ProcessFiles.Done', self._printResults())
            
        except Exception, errtxt:
            print errtxt
        
        while self.running:
            self.handleEvents()
        
        # while True:
        #     self.lock.acquire()
        #     if self.filesQueue.empty():
        #         processFilesThread.running = False
        #         break
        #     self.lock.release()
        # while not self.filesQueue.empty():
        #     file = self.filesQueue.get()
        #     filePath = os.path.join(self.root, file)
        #     self.duplicates.add(filePath)
    
    def handleEvents(self):
        for event in self.eventDispatcher.get(): # event handling loop
            if (event.name == 'Thread.ProcessFiles.Done'):
                self.view.output('\n')
                self.view.output('Thread.ProcessFiles.Done')
                self.view.output('\n')
                self._printResults()
                self.running = False
                
    
    def _printResults(self):
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