from time import sleep
from messaging.settings import RABBIT_HOST, RABBIT_LOGIN, RABBIT_PASSWORD

__author__ = 'arik'

import pika

def getConnection():
    host = "localhost"
    credentials = pika.PlainCredentials(RABBIT_LOGIN, RABBIT_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBIT_HOST, credentials=credentials)
    )
    return connection

sendChanel = getConnection().channel()


def declareQueue(queueName):
    sendChanel.queue_declare(queue=queueName)


def sendMessage(queueName, message) :
    sendChanel.basic_publish(exchange='',
                  routing_key=queueName,
                  body=message)