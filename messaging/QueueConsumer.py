import threadingimport uuidfrom uuid import UUIDfrom messaging.Messaging import getConnection__author__ = 'arik'class ConsumerThread(threading.Thread):    def __init__(self, queue, callback_func, *args, **kwargs):        super(ConsumerThread, self).__init__(*args, **kwargs)        self.queue = queue        self.callback_func = callback_func        self.connection = getConnection()        self.channel = self.connection.channel()        self.tag = self.channel.basic_consume(callback_func,                          queue=queue,                          no_ack=True)    def run(self):        print "Start " + self.tag        self.channel.start_consuming()    def stopRecieve(self):        print "Stop " + self.tag        self.channel.basic_cancel(self.tag)