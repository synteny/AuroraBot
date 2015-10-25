import calendar
import json
from datetime import timedelta, datetime
import requests
from datapoller.download import download
from datapoller.settings import NOWCAST_DATA_URL
from messaging.Messaging import sendMessage
from messaging.settings import RABBIT_NOTIFY_QUEUE
from sessioncontroller.model import get_users

__author__ = 'arik'


import sched, time

def main():
    def processUpdate():
        print "Start update"
        (dataList, time) = download(NOWCAST_DATA_URL)
        allUsers = get_users()
        print "Process update"
        for user in allUsers:
            geo_id = user[1]
            level = dataList[geo_id]
            if(level >= 0):
                timeInTs =  calendar.timegm(time.timetuple())
                sendMessage(RABBIT_NOTIFY_QUEUE, json.dumps({"time": timeInTs, "geo": user[0], "chat_id": user[2], "level": level}))


    s = sched.scheduler(time.time, time.sleep)
    s.enter(0, 1, processUpdate, ())
    while(True):
        try:
            s.enter(100, 1, processUpdate, ())
            s.run()
        except Exception, e:
            print e


if __name__ == '__main__':
    main()