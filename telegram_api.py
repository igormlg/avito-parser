import requests, json
from dotenv import load_dotenv
import os

def send_telegram(command, send_data):
    env_path = './.env'
    load_dotenv(env_path)

    tg_bot_token = os.getenv('BOT_FOR_AVITO_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHANNEL')

    send_data = {
        "chat_id": chat_id,
        "text": send_data,
    }

    tg_req = requests.post(
        'https://api.telegram.org/bot' + tg_bot_token + '/' + command,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(send_data)
    )
    return tg_req.json()
