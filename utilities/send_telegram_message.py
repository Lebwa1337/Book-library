import os

import requests


def send_tg_message(message):
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.post(url)



