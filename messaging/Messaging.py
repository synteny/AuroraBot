from time import sleep
from messaging.settings import RABBIT_HOST, RABBIT_LOGIN, RABBIT_PASSWORD

__author__ = 'arik'

import pika

def getConnection():
    credentials = pika.PlainCredentials(RABBIT_LOGIN, RABBIT_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBIT_HOST, credentials=credentials)
    )
    return connection

sendChanel = None

def declareQueue(queueName):
    getSendChannel().queue_declare(queue=queueName)


def getSendChannel():
    global sendChanel
    if sendChanel is None or sendChanel.is_open is False:
        sendChanel = getConnection().channel()
    return sendChanel

def sendMessage(queueName, message) :
    getSendChannel().basic_publish(exchange='',
                  routing_key=queueName,
                  body=message)