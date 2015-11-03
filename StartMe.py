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
    sсhedulerProcess = None
    sendToUserProcess = None
    telegramBotProcess = None
    manager = Manager()
    sharedDict = manager.dict()
    while True:
        try:
            if sсhedulerProcess is None or sсhedulerProcess.is_alive() is False:
                print "Starting schedulerProcess"
                sсhedulerProcess = Process(target=startScheduler, args=(sharedDict,))
                sсhedulerProcess.start()

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
