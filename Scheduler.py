import json
import requests
from datapoller.download import download
from datapoller.settings import NOWCAST_DATA_URL
from messaging.Messaging import sendMessage
from sessioncontroller.model import get_users

__author__ = 'arik'


import sched, time



def processUpdate():
    print "Start update"
    (dataList, time) = download(NOWCAST_DATA_URL)
    allUsers = get_users()
    print "Process update"
    for user in allUsers:
        geo_id = user[0]
        level = dataList[geo_id]
        if(level >= 5):
            sendMessage("send", json.dumps({"geo": user[2], "chanel_id": user[1], "level": level}))


s = sched.scheduler(time.time, time.sleep)
while(True):
    try:
        s.enter(10, 1, processUpdate, ())
        s.run()
    except Exception, e:
        print e