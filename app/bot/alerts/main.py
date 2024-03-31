import telebot
from bot.config import AdminSettings
from utils.get_text_from_template import get_text_funding


def funding_alert(users_id: list, fundings: list):
    API_TOKEN = AdminSettings().bot_token
    msg = get_text_funding(fundings)
    bot = telebot.TeleBot(API_TOKEN)
    for i in users_id:
        bot.send_message(i, msg)
