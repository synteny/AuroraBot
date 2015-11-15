# coding=utf-8
from datetime import datetime
import json
from messaging.Messaging import declareQueue, getConnection
from messaging.settings import RABBIT_NOTIFY_QUEUE
from sessioncontroller.telegram_bot import reply, reply_by_chat_id

__author__ = 'arik'


def buidIntervalString(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    returnStr = ""
    if(hours > 0):
        returnStr = u"%d час " % (hours)
    return returnStr + u"%d мин" % (minutes)


def getIntervalSec(timestamp):
    return (datetime.utcfromtimestamp(timestamp) - datetime.utcnow()).total_seconds()


def main():
    declareQueue(RABBIT_NOTIFY_QUEUE)

    def sendToUserCallback(ch, method, properties, body):
        print "Sending to user"
        try:
            recieve = json.loads(body)
            validTime = getIntervalSec(recieve["time"])
            if validTime < 60: # to old
                return
            message = u"Через {} в вашем месте ({}) вероятность полярного сияния составит {}%"\
                .format(buidIntervalString(validTime), recieve["geo"], str(recieve["level"]))
            reply_by_chat_id(recieve["chat_id"], message)
        except StandardError as e:
            print(e)

    connection = getConnection()
    channel = connection.channel()
    channel.basic_consume(sendToUserCallback, queue=RABBIT_NOTIFY_QUEUE, no_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    print 'Press Ctrl+C to kill...'
    main()
