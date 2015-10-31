import calendar
import json
from datetime import datetime
from datapoller.download import download
from datapoller.settings import *
from messaging.Messaging import sendMessage
from messaging.settings import RABBIT_NOTIFY_QUEUE
from sessioncontroller.utils import is_level_interesting_for_kp

__author__ = 'arik'

sharedDict = {}


def registerModelStorage(dict):
    global sharedDict
    sharedDict = dict

def updateModel():
    (lastLevels, validTime) = download(NOWCAST_DATA_URL)
    sharedDict['lastLevels'] = lastLevels
    sharedDict['validTime'] = validTime


def hasValidModel():
    lastLevels = sharedDict.get('lastLevels')
    validTime = sharedDict.get('validTime')
    return lastLevels is not None and validTime is not None and \
           getTimestamp(validTime) >= getTimestamp(datetime.utcnow())


def processUserLocation(geo_id, geo, kp_level, chat_id, bot):
    if hasValidModel() is False:
        return
    lastLevels = sharedDict.get('lastLevels')
    validTime = sharedDict.get('validTime')
    level = lastLevels[geo_id]
    if kp_level is None or is_level_interesting_for_kp(level, kp_level):
        sendMessage(
            RABBIT_NOTIFY_QUEUE,
            json.dumps({"time": getTimestamp(validTime), "geo": geo, "chat_id": chat_id, "level": level, "bot": bot})
        )


def getTimestamp(datetime):
    return calendar.timegm(datetime.timetuple())
