from datetime import timedelta, datetime
from auroramodel.AuroraModel import updateModel, hasValidModel, processUserLocation, registerModelStorage
from datapoller.settings import *
from messaging.Messaging import sendMessage, declareQueue
from messaging.settings import RABBIT_NOTIFY_QUEUE
from sessioncontroller.model import get_users

__author__ = 'arik'


import sched, time


def next_nowcast():
    t = datetime.now()
    remaining = NOWCAST_UPDATE_INTERVAL.seconds - ((t.minute * 60 + t.second) % NOWCAST_UPDATE_INTERVAL.seconds)
    next = t + timedelta(seconds=remaining)
    print("Next nowcast update: {0}".format(str(next)))
    return next


def fetch_nowcast():
    print "Fetching nowcast"
    updateModel()
    if hasValidModel():
        allUsers = get_users()
        print "Updating..."
        for user in allUsers:
            geo = user[0]
            geo_id = user[1]
            chat_id = user[2]
            kp_level = user[3]
            bot = user[4]
            processUserLocation(geo_id, geo, kp_level, chat_id, bot)


def main(sharedDict):
    registerModelStorage(sharedDict)
    declareQueue(RABBIT_NOTIFY_QUEUE)
    s = sched.scheduler(time.time, time.sleep)
    fetch_nowcast()
    while (True):
        try:
            s.enter((next_nowcast() - datetime.now()).total_seconds(), 1, fetch_nowcast, ())
            s.run()
        except Exception, e:
            print e


if __name__ == '__main__':
    print "Press Ctrl+C to kill..."
    main({})
