# -*- coding: utf-8 -*-

import telegram
from settings import TELEGRAM_TOKEN
from pygeocoder import Geocoder
import pygeolib
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

offset = 0
print 'Press Ctrl+C to kill...'
while True:
    updates = bot.getUpdates(offset=offset+1)
    for update in updates:
        text = update.message.text
        text_split = text.split(' ', 1)
        command, arguments = text_split[0], None
        if len(text_split) > 1:
            arguments = text_split[1]

        if command == '/subscribe':
            geo = geo_code(arguments)
            if geo is None:
                reply(update, "Не удалось определить координаты места")
            else:
                geo_id = lat_lon_to_cell(geo[0], geo[1])
                subscribe(update.message.chat_id, arguments, geo_id)
                reply(update, "Вы подписаны и получите уведомление о сиянии в Ваше регионе как только так сразу!")

        elif command == '/unsubscribe':
            unsubscribe(update.message.chat_id)
            reply(update, "Вы успешно отписаны.")

        else:
            reply(update, "Неизвестная комманда")
        offset = update.update_id
