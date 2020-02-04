import json
import requests
from subprocess import Popen, PIPE
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from bot_v1.models import *
from subprocess import Popen, PIPE


# Клавиатура
BUTTON1_SEARCH = "Новый поиск"
BUTTON2_HISTORY = "История"

def get_base_reply_keyboard():
    keyboard = [
    [
    KeyboardButton(BUTTON1_SEARCH),
    KeyboardButton(BUTTON2_HISTORY),
    ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard,
    resize_keyboard=True)


# обработка ошибок
def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = 'Произошла ошибка: {}'.format(e)
            print(error_message)
            raise e
    return inner


# Подключение к API
def get_address(update: Update, context: CallbackContext, **kwargs):

    req = update.message.text
    req_url = requests.get('https://geocode-maps.yandex.ru/1.x/?format=json&apikey=5ee7f7a0-4e38-4217-a958-5215b17c4fe1&geocode={}'.format(req))
    addresses = req_url.json()
    data = addresses['response']['GeoObjectCollection']['featureMember']
    for adress_data in data:
        address = adress_data['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        return address
        saved_addresses.append(address)

saved_addresses = []


# оптравка сообщений
@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    #u, _ = BotUser.objects.get_or_create(user_id=chat_id, search_history=text)

    reply_markup = get_base_reply_keyboard()
    if text == BUTTON1_SEARCH:
        get_address(update, context, address=adr)
        resp = saved_addresses
        reply_text = "На ваш запрос <{}> найдены следуйщие результаты:\n{}".format(text, resp)
        update.message.reply_text(text=reply_text, reply_markup = get_base_reply_keyboard())
    elif text == BUTTON2_HISTORY:
        pass
    else:
        reply_text = "На ваш запрос {} найдены следуйщие результаты:\n{}".format(adr, text)
        update.message.reply_text(text=reply_text, reply_markup = get_base_reply_keyboard())



# БОТ
class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # Подключение
        request = Request(connect_timeout=0.5, read_timeout=1,)
        bot = Bot(request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL,)
        print(bot.get_me())


        # Обработчики
        updater = Updater(bot=bot, use_context=True,)


        message_handler = MessageHandler(Filters.text, do_echo)
        address_handler = MessageHandler(Filters.text, get_address)


        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(address_handler)


        # Запусткает бесконечный обработчик
        updater.start_polling()
        updater.idle()
