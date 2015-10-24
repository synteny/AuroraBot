import threading
import uuid
from uuid import UUID
from messaging.Messaging import registerListener, getChanel

__author__ = 'arik'


class ConsumerThread(threading.Thread):
    def __init__(self, queue, callback_func, *args, **kwargs):
        super(ConsumerThread, self).__init__(*args, **kwargs)
        self.queue = queue
        self.callback_func = callback_func
        self.tag = registerListener(self.callback_func, self.queue)

    def run(self):
        print "Start " + self.tag
        getChanel().start_consuming()

    def stopRecieve(self):
        print "Stop " + self.tag
        getChanel().basic_cancel(self.tag)