# -*- coding: utf-8 -*-import telegramfrom auroramodel.AuroraModel import processUserLocation, registerModelStoragefrom sessioncontroller.utils import get_kp_levelfrom settings import TELEGRAM_TOKENfrom pygeocoder import Geocoderimport pygeolibfrom model import subscribe, unsubscribefrom utils import lat_lon_to_cellbot = telegram.Bot(token=TELEGRAM_TOKEN)commands = [    '/subscribe Санкт-Петербург',    '/unsubscribe']botname = "telegram"def geo_code(address):    try:        business_geocoder = Geocoder(None, 'MY_API_KEY')        results = business_geocoder.geocode(address)        return results.latitude, results.longitude    except pygeolib.GeocoderError:        return Nonedef reply(update, message):    bot.sendMessage(        chat_id=update.message.chat_id,        reply_to_message_id=update.message.message_id,        text=message,    )def reply_by_chat_id(chat_id, message):    bot.sendMessage(        chat_id=chat_id,        text=message,    )def main(sharedDict):    offset = 0    registerModelStorage(sharedDict)    while True:        updates = bot.getUpdates(offset=offset+1)        for update in updates:            text = update.message.text            text_split = text.split(' ', 1)            command, arguments = text_split[0], None            if len(text_split) > 1:                arguments = text_split[1]            if command == '/subscribe':                geo = geo_code(arguments)                if not geo and update.message.location:                    geo = update.message.location.latitude, update.message.location.longitude                if geo is None:                    reply(update, "Не удалось определить координаты места")                else:                    geo_id = lat_lon_to_cell(geo[0], geo[1])                    kp_level = get_kp_level(geo[0])                    subscribe(update.message.chat_id, arguments, geo_id, kp_level, botname)                    reply(update, """Вы подписаны и получите уведомление о сиянии в Вашем регионе как только, так сразу!На всякий случай проверьте, что мы правильно определили Ваше местоположение.""")                    bot.sendLocation(                        chat_id=update.message.chat_id,                        latitude=geo[0],                        longitude=geo[1],                    )                    processUserLocation(geo_id, arguments, None, update.message.chat_id, botname)            elif command == '/unsubscribe':                unsubscribe(update.message.chat_id, botname)                reply(update, "Вы успешно отписаны.")            elif command == '/start':                reply(update, "Наш бот будет рад оказаться полезным.")            else:                reply(update, "Неизвестная комманда")            offset = update.update_idif __name__ == '__main__':    print 'Press Ctrl+C to kill...'    main({})