import sys

class EventDispatcher(object):
    def __init__(self):
        super(EventDispatcher, self).__init__()
        self.handlers = []
        self.events = []

    def add(self, eventName, handler):
        if eventName not in self.handlers:
            self.handlers[eventName] = []

        self.handlers[eventName].append(handler)

    def remove(self, eventName, handler):
        if eventName in self.handlers:
            self.handlers[eventName].remove(handler)

    def dispatch(self, eventName, *args, **kwargs):
        self.events.append(Event(eventName, *args, **kwargs))
        if eventName in self.handlers:
            event = Event(eventName, *args, **kwargs)
            for handler in self.handlers[eventName]:
                handler(event)
    
    def get(self):
        return self.events


class Event(object):
    def __init__(self, name, *args, **kwargs):
        super(Event, self).__init__()
        self.name = name
        self.args = args
        self.kwargs = kwargs
        
    
