# coding=utf-8
from datetime import datetime
import json
from messaging.Messaging import declareQueue
from messaging.QueueConsumer import ConsumerThread
from messaging.settings import RABBIT_NOTIFY_QUEUE
from sessioncontroller.telegram_bot import reply, reply_by_chat_id

__author__ = 'arik'


def buidIntervalString(timestamp):
    total_seconds = (datetime.utcfromtimestamp(timestamp) - datetime.utcnow()).total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    returnStr = ""
    if(hours > 0):
        returnStr = u"%d час " % (hours)
    return returnStr + u"%d мин" % (minutes)


def main():
    print 'Press Ctrl+C to kill...'

    declareQueue(RABBIT_NOTIFY_QUEUE)

    def sendToUserCallback(ch, method, properties, body):
        print "Sending to user"
        recieve = json.loads(body)
        message = u"Прогноз на ближайшие {}. В вашем городе ({}) ожидается северное сияние видимое с вероятностью {}%"\
            .format(buidIntervalString(recieve["time"]), recieve["geo"], str(recieve["level"]))
        reply_by_chat_id(recieve["chat_id"], message)


    threads = []
    for i in range(1):
         threads.append(ConsumerThread(RABBIT_NOTIFY_QUEUE, sendToUserCallback))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
