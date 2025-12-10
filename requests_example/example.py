import os
import requests
import time


API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = os.getenv("BOT_TOKEN")
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int
print(BOT_TOKEN)
while counter < MAX_COUNTER:
    print('attempt = ', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    print(updates)
    if updates['result']:
        print("got an update")
        for result in updates['result']:
            msg = result['message']['text']
            print(f'send back for {msg}')
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            url = f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={msg}'
            # https://api.telegram.org/bot<token>/sendMessage?chat_id=<chat_id>&text=aaa
            updates = requests.get(url)
            print(updates.json())

    time.sleep(1)
    counter += 1