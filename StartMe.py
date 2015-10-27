from time import sleep
from gnomevfs._gnomevfs import Error
import Scheduler
import SendToUser
from sessioncontroller import telegram_bot

__author__ = 'arik'

from multiprocessing import Process


def startSheduler():
    Scheduler.main()


def startSendToUser():
    SendToUser.main()


def startTelegramBot():
    telegram_bot.main()


if __name__ == '__main__':
    print 'Press Ctrl+C to kill...'
    shedulerProcess = None
    sendToUserProcess = None
    telegramBotProcess = None
    while True:
        try:
            if shedulerProcess is None or shedulerProcess.is_alive() is False:
                print "Starting shedulerProcess"
                shedulerProcess = Process(target=startSheduler, args=())
                shedulerProcess.start()

            if sendToUserProcess is None or sendToUserProcess.is_alive() is False:
                print "Starting sendToUserProcess"
                sendToUserProcess = Process(target=startSendToUser, args=())
                sendToUserProcess.start()

            if telegramBotProcess is None or telegramBotProcess.is_alive() is False:
                print "Starting telegramBotProcess"
                telegramBotProcess = Process(target=startTelegramBot, args=())
                telegramBotProcess.start()

            sleep(100)
        except Error, e:
            print(e)
