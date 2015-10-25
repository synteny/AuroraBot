import calendar
import json
from datetime import timedelta, datetime
import requests
from datapoller.download import download
from datapoller.settings import *
from messaging.Messaging import sendMessage, declareQueue
from messaging.settings import RABBIT_NOTIFY_QUEUE
from sessioncontroller.model import get_users

__author__ = 'arik'


import sched, time


def next_nowcast():
    t = datetime.now()
    remaining = NOWCAST_UPDATE_INTERVAL.seconds - ((t.minute * 60 + t.second) % NOWCAST_UPDATE_INTERVAL.seconds)
    next = t + timedelta(seconds=remaining) + timedelta(minutes=1)
    print("Next nowcast update: {0}".format(str(next)))
    return (next - datetime.fromtimestamp(0)).total_seconds()


def fetch_nowcast():
    print "Fetching nowcast"
    (dataList, time) = download(NOWCAST_DATA_URL)
    allUsers = get_users()
    print "Updating..."
    for user in allUsers:
        geo_id = user[1]
        level = dataList[geo_id]
        if(level >= 0):
            timeInTs =  calendar.timegm(time.timetuple())
            sendMessage(RABBIT_NOTIFY_QUEUE, json.dumps({"time": timeInTs, "geo": user[0], "chat_id": user[2], "level": level}))


def main():
    print "Start scheduler"
    declareQueue(RABBIT_NOTIFY_QUEUE)
    s = sched.scheduler(time.time, time.sleep)
    fetch_nowcast()
    while (True):
        try:
            s.enter(next_nowcast() - time.time(), 1, fetch_nowcast, ())
            s.run()
        except Exception, e:
            print e


if __name__ == '__main__':
    main()
