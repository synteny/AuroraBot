import os

__author__ = 'arik'


RABBIT_HOST = os.getenv("RABBITMQ_PORT_5672_TCP_ADDR", "localhost")
RABBIT_LOGIN = "guest"
RABBIT_PASSWORD = "guest"
RABBIT_NOTIFY_QUEUE = "send"
