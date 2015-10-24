from time import sleep
from messaging.settings import RABBIT_HOST, RABBIT_LOGIN, RABBIT_PASSWORD

__author__ = 'arik'

import pika

host = "localhost"
credentials = pika.PlainCredentials(RABBIT_LOGIN, RABBIT_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBIT_HOST, credentials=credentials)
)
channel = connection.channel()

def getChanel():
    return channel


def closeConnection():
    return connection.close()

def registerListener(callbackFn, queueName):
    print "Start queue listener"
    channel = getChanel()
    tag = channel.basic_consume(callbackFn,
                      queue=queueName,
                      no_ack=True)
    return tag


def declareQueue(queueName):
    getChanel().queue_declare(queue=queueName)


def sendMessage(queueName, message) :
    channel = getChanel()
    channel.basic_publish(exchange='',
                  routing_key=queueName,
                  body=message)