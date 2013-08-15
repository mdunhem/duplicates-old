from options import Options
from scanner import Scanner
from duplicatecollector import DuplicateCollector

class Controller:
    def __init__(self, options = None):
        if options and isinstance(options, Options):
            self.options = options
        else:
            self.options = Options()

    def run(self):
        parsedArgs = self.options.parse()
        scanner = Scanner(parsedArgs.path)
        duplicateCollector = DuplicateCollector()
        scanner.scan(duplicateCollector)

        if parsedArgs.verbose:
            duplicateCollector.write(True)
        else:
            duplicateCollector.write()
        
    
    # def display(self):
    #     print parsedArgs.description
    #     print parsedArgs.path
