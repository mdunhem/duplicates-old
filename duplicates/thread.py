import sys
import os
import threading
import Queue
import model
import event

# ----------------------------
# ScanFilesThread Class
# ----------------------------
class ScanFilesThread(threading.Thread):
    def __init__(self, queue, path, eventDispatcher, lock):
        super(ScanFilesThread, self).__init__()
        self.queue = queue
        self.path = path
        self.eventDispatcher = eventDispatcher
        self.lock = lock
    
    def run(self):
        for root, directories, files in os.walk(self.path):
            for file in files:
                self.lock.acquire()
                self.queue.put((root, file))
                self.lock.release()
    
        self.eventDispatcher.dispatch('Thread.ScanFiles.Done')
        return

# ----------------------------
# ProcessFilesThread Class
# ----------------------------
class ProcessFilesThread(threading.Thread):
    def __init__(self, queue, duplicate, eventDispatcher, lock):
        super(ProcessFilesThread, self).__init__()
        self.queue = queue
        self.duplicate = duplicate
        self.eventDispatcher = eventDispatcher
        self.lock = lock
        self.running = True
    
    def run(self):
        while True:
            self.lock.acquire()
            if not self.queue.empty():
                root, file = self.queue.get()
                filePath = os.path.join(root, file)
                self.duplicate.add(filePath)
                self.queue.task_done()
            else:
                self.eventDispatcher.dispatch('Thread.ProcessFiles.Done')
                return
            self.lock.release()
            

