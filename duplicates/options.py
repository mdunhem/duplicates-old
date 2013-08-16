import argparse
import os
from duplicates import metadata

class Options:

    def __init__(self, args = None):
        self.args = args
        self._initParser()

    ##
    #   API, Public Methods
    #

    def parse(self):
        parsedArgs = self.parser.parse_args(self.args[1:])

        # if parsedArgs.description:
        #     return self._epilog()
        # elif parsedArgs.verbose:
        #     print parsedArgs
        return parsedArgs

    ##
    #   Private Methods
    #

    def _initParser(self):
        self.parser = argparse.ArgumentParser(
            prog = self.args[0],
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = metadata.description,
            epilog = self._epilog()
        )
        self.parser.add_argument(
            '-v', '--verbose',
            help = 'print the results to the screen',
            action = 'store_true'
        )
        self.parser.add_argument(
            '-r', '--recursive',
            help = 'should recursively search through folders',
            action = 'store_true'
        )
        self.parser.add_argument(
            '-d', '--display',
            help = 'print out the results to stdout',
            action = 'store_true'
        )
        self.parser.add_argument(
            '-w', '--write',
            help = 'should write results to file',
            action = 'store_false'
        )
        self.parser.add_argument(
            '-p', '--path',
            help = 'set the path to the directory to search through, defaults to current directory',
            default = os.getcwd()
        )

    def _epilog(self):
        epilog = '''{project} v{version}\n\n{authors}\nURL: <{url}>'''.format(
            project = metadata.project,
            version = metadata.version,
            authors = '\n'.join(self._authors()),
            url = metadata.url
        )
        return epilog

    def _authors(self):
        authors = []
        for name, email in zip(metadata.authors, metadata.emails):
            authors.append('Author: {0} <{1}>'.format(name, email))
        return authors

