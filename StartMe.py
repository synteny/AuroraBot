from time import sleep
import Scheduler
import SendToUser
from sessioncontroller import telegram_bot

__author__ = 'arik'

from multiprocessing import Process, Manager


def startScheduler(sharedDict):
    Scheduler.main(sharedDict)


def startSendToUser():
    SendToUser.main()


def startTelegramBot(sharedDict):
    telegram_bot.main(sharedDict)


if __name__ == '__main__':
    print 'Press Ctrl+C to kill...'
    schedulerProcess = None
    sendToUserProcess = None
    telegramBotProcess = None
    manager = Manager()
    sharedDict = manager.dict()
    while True:
        try:
            if schedulerProcess is None or schedulerProcess.is_alive() is False:
                print "Starting schedulerProcess"
                schedulerProcess = Process(target=startScheduler, args=(sharedDict,))
                schedulerProcess.start()

            if sendToUserProcess is None or sendToUserProcess.is_alive() is False:
                print "Starting sendToUserProcess"
                sendToUserProcess = Process(target=startSendToUser, args=())
                sendToUserProcess.start()

            if telegramBotProcess is None or telegramBotProcess.is_alive() is False:
                print "Starting telegramBotProcess"
                telegramBotProcess = Process(target=startTelegramBot, args=(sharedDict,))
                telegramBotProcess.start()

            sleep(100)
        except StandardError, e:
            print(e)
