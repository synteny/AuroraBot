# coding=utf-8
import json
from messaging.QueueConsumer import ConsumerThread
from sessioncontroller.telegram_bot import reply, reply_by_chat_id

__author__ = 'arik'


def main():
    print 'Press Ctrl+C to kill...'

    def sendToUserCallback(ch, method, properties, body):
        print "Sending to user"
        recieve = json.loads(body)
        message = u"Прогноз на ближайшие пол часа. В вашем городе ({}) ожидается северное сияние видимое с вероятностью {}%"\
            .format(recieve["geo"], str(recieve["level"]))
        reply_by_chat_id(recieve["chat_id"], message)


    threads = []
    for i in range(1):
         threads.append(ConsumerThread("send", sendToUserCallback))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
