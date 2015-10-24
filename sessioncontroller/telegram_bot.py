# -*- coding: utf-8 -*-

import telegram
from settings import TELEGRAM_TOKEN
from pygeocoder import Geocoder
import pygeolib
import re
from model import subscribe, unsubscribe
from utils import lat_lon_to_cell

bot = telegram.Bot(token=TELEGRAM_TOKEN)

commands = [
    '/subscribe Санкт-Петербург',
    '/unsubscribe'
]


def geo_code(address):
    try:
        business_geocoder = Geocoder(None, 'MY_API_KEY')
        results = business_geocoder.geocode(address)
        return results.latitude, results.longitude
    except pygeolib.GeocoderError:
        return None


def reply(update, message):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        reply_to_message_id=update.message.message_id,
        text=message,
    )


while True:
    updates = bot.getUpdates()
    for update in updates:
        text = update.message.text
        matches = re.search('/(.*) ?(.*)', text)
        if matches:
            command = matches.group(1)
            arguments = matches.group(2)
            print command, arguments
            if command == 'subscribe':
                geo = geo_code(arguments)
                if geo is None:
                    reply(update, "Не удалось определить координаты места")
                else:
                    print geo
                    geo_id = lat_lon_to_cell(geo[0], geo[1])
                    subscribe(update.message.chat_id, arguments, geo_id)
                    reply(update, "Вы подписаны и получите уведомление о сиянии в Ваше регионе как только так сразу!")

            if command == 'unsubscribe':
                unsubscribe(update.message.chat_id)
    # TODO: remove later
    exit()
