import time

class EventManager:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def add(self, listener):
        self.listeners[ listener ] = 1

    def remove(self, listener):
        del self.listeners[ listener ]

    def post(self, event):
        print "post event %s" % event.name
        for listener in self.listeners.keys():
            listener.notify(event)

class Listener:
    def __init__(self, event_mgr=None):
        if event_mgr is not None:
            event_mgr.add(self)

    def notify(self, event):
        event(self)


class Event:
    def __init__(self, name="Generic Event"):
        self.name = name

    def __call__(self, controller):
        pass

class QuitEvent(Event):
    def __init__(self):
        Event.__init__(self, "Quit")

    def __call__(self, listener):
        listener.exit(self)

class TestEvent(Event):
    def __init__(self):
        Event.__init__(self, "Test")

    def __call__(self, listener):
        print "test called"


class RunController(Listener):
    def __init__(self, event_mgr):
        Listener.__init__(self, event_mgr)
        self.running = True
        self.event_mgr = event_mgr

    def exit(self, event):
        print "exit called"
        self.running = False

    def run(self):
        print "run called"
        i = 0
        while self.running:
            if i>10:
                event = QuitEvent()
            else:
                event = TestEvent()
            i = i + 1
            # event = QuitEvent()
            # event = TestEvent()
            self.event_mgr.post(event)
            time.sleep(0.5)

em = EventManager()
run = RunController(em)
run.run()