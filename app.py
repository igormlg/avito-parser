from flask import Flask, request
import yaml, requests, json, os
from telegram_api import send_telegram
from refresh_token import get_token
from dotenv import load_dotenv
import re

app = Flask(__name__)

# token = None
# with open('token.yml') as f:
#     token = yaml.safe_load(f)['token']

# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {token}'
# }

# chat_id = ''
# user_id = 0
# author_id = 0
# text = ''

@app.route("/")
def hello():
    return 'Hello'

@app.route("/check/<check_str>")
def set_webhook(check_str):
    env_path = './.env'
    load_dotenv(env_path)

    if check_str == os.getenv('CHECK_STR'):
        get_token()
    # avito_hook_url = 'https://api.avito.ru/messenger/v3/webhook'
    # url_params = {
    #     'url': 'https://9dd0-176-116-136-197.ngrok-free.app/ans'
    # }
    # answer = requests.post(avito_hook_url, headers=headers, data=json.dumps(url_params))

    return 'IN'

@app.route("/ans", methods=['POST', 'GET'])
def ans_avito():

    if request.method == 'POST':

        data = request.json
        # print(data)

        chat_id = ''
        user_id = 0
        author_id = 0
        text = ''

        if 'payload' in data:
            chat_id = data['payload'].get('value', {}).get('chat_id', 'Default')
            user_id = data['payload'].get('value', {}).get('user_id', 'Default')
            author_id = data['payload'].get('value', {}).get('author_id', 'Default')
            text = data['payload'].get('value', {}).get('content', {}).get('text', 'Default')

            data_txt = 'Сообщение: {text}\n' \
                'chat_id: || {chat_id} ||\n' \
                'user_id: || {user_id} ||\n' \
            .format(**dict(
                text=text,
                chat_id=chat_id,
                user_id=user_id,
            ))
            # print(data_txt)
        if user_id != author_id:
            send_telegram('sendMessage', data_txt)
            
    return ('', 204)

@app.route("/ans_tg", methods=['POST', 'GET'])
def ans_tg():
    if request.method == 'POST':

        token = None
        with open('token.yml') as f:
            token = yaml.safe_load(f)['token']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        data = request.json
        print(data)

        if 'channel_post' in data:
            try:
                clean_str = data['channel_post'].get('reply_to_message', {}).get('text', 'Default')
                clean_str = clean_str.replace('\n', '').replace('\r', ' ')
                match_chat_id = re.search(r"chat_id: \|\| (.*?) \|\|", clean_str)
                match_user_id = re.search(r"user_id: \|\| (.*?) \|\|", clean_str)
                ans_text = data['channel_post']['text']

                if match_chat_id.group(1):
                    match_chat_id = match_chat_id.group(1)
                    match_user_id = match_user_id.group(1)

                    avito_ans_url = f'https://api.avito.ru/messenger/v1/accounts/{match_user_id}/chats/{match_chat_id}/messages'
                    avito_read_url = f'https://api.avito.ru/messenger/v1/accounts/{match_user_id}/chats/{match_chat_id}/read'
                    url_params = {
                        'message': {
                            'text': ans_text
                        },
                        'type': 'text'
                    }
                    answer = requests.post(avito_ans_url, headers=headers, data=json.dumps(url_params))
                    answer_read = requests.post(avito_read_url, headers=headers, data=json.dumps(url_params))
                return ('', 204)
            except:
                return ('', 204)


    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5087)