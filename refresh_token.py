import requests, json, yaml
from dotenv import load_dotenv
import os

def get_token():
    env_path = './.env'
    load_dotenv(env_path)

    client_id = os.getenv('CLIENT_D')
    client_secret = os.getenv('CLIENT_SECRET')
    site_url = os.getenv('SITE_URL')

    try:
        req_token = requests.post(f'https://api.avito.ru/token/?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}')
        data = json.loads(req_token.text)
        print(data)
        token = data['access_token']
        
        to_yaml = {'token': token}

        with open('token.yml', 'w') as f:
            yaml.dump(to_yaml, f)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        avito_hook_url = 'https://api.avito.ru/messenger/v3/webhook'
        url_params = {
            'url': f'{site_url}/ans'
        }
        answer = requests.post(avito_hook_url, headers=headers, data=json.dumps(url_params))
    except Exception:
        print(Exception)

if __name__ == '__main__': 
    get_token()
