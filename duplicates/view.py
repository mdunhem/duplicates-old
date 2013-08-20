import sys
import time

class View(object):
    """Base View Class"""
    def __init__(self, *args, **kwargs):
        super(View, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.stdout = kwargs.get('stdout', sys.stdout)

    def output(self, text):
        self.stdout.write(text)


class CommandLineView(View):
    """docstring for CommandLineView"""
    def __init__(self, *args, **kwargs):
        super(CommandLineView, self).__init__()


class ProgressBar(View):
    """
        The options are:
            start   State from which start the progress. For example, if start is 
                    5 and the end is 10, the progress of this state is 50%
            end     State in which the progress has terminated.
            width   --
            fill    String to use for "filled" used to represent the progress
            blank   String to use for "filled" used to represent remaining space.
            format  Format
            incremental
    """
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)

        # Set the default values, can be changed before the progress bar is actually displayed
        self.start = 0
        self.end = 10
        self.width = 12
        self.fill = '='
        self.blank = '.'
        self.title = ''
        self.format = '[{0}>{1}] {2}%'
        self.incremental = True
        self.step = 100 / float(self.width) #fix
        self.reset()

    def reset(self):
        """Resets the current progress to the start point"""
        self.progress = self._getProgress(self.start)
        return self

    def increment(self, increment = 1):
        increment = self._getProgress(increment)
        if 100 > (self.progress + increment):
            self.progress += increment
        else:
            self.progress = 100
        return self

    def displayProgress(self):
        if hasattr(self.stdout, 'isatty') and self.stdout.isatty():
            self.stdout.write('\r')
        else:
            self.stdout.write('\n')
        self.stdout.write(str(self))
        self.stdout.flush()

    def done(self):
        self.stdout.write('  done.\n')
        self.stdout.flush()

    def _getProgress(self, increment):
        return float(increment * 100) / self.end

    def __str__(self):
        progressed = int(self.progress / self.step) #fix
        fill = progressed * self.fill
        blank = (self.width - progressed) * self.blank
        return self.title + self.format.format(fill, blank, int(self.progress))
        # return self.format % {'fill': fill, 'blank': blank, 'progress': int(self.progress)}

    __repr__ = __str__
        