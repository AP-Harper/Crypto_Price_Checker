import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
import requests
import time
from datetime import datetime


ETHEREUM_PRICE_THRESHOLD = 2000
COINMARKETCAP_API = os.getenv('COINMARKETCAP_API_KEY')
IFTTT_WEBHOOKS_URL = os.getenv('IFTTT_WEBHOOKS_URL')
COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


test = 'https://maker.ifttt.com/trigger/{}/with/key/c-Bvksw_rHomvDdLY388El'


def get_latest_ethereum_price():
    response = requests.get(COINMARKETCAP_API_URL)

    parameters = {
        'symbol': 'ETH',
        'convert': 'GBP'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API
    }

    response = requests.get(COINMARKETCAP_API_URL, params=parameters, headers=headers).json()
    return float(response['data']['ETH']['quote']['GBP']['price'])


def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)


# Format prices and time & date
def format_ethereum_history(ethereum_history):
    rows = []
    for ethereum_price in ethereum_history:
        date = ethereum_price['date'].strftime('%d.%m.%Y %H.%M')
        price = ethereum_price['price']
        row = '{}: £<b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)


def main():
    print(IFTTT_WEBHOOKS_URL)
    ethereum_history = []
    while (True):
        price = get_latest_ethereum_price()
        date = datetime.now()
        ethereum_history.append({'date': date, 'price': price})
        if price < ETHEREUM_PRICE_THRESHOLD:
            post_ifttt_webhook('crypto_price_emergency', price)

        # Set the number of different prices that are sent as notification        
        if len(ethereum_history) == 2:
            post_ifttt_webhook('crypto_price_update', format_ethereum_history(ethereum_history))

            # Clear price history list
            ethereum_history = []

        # Set the interval between prices checks (in seconds)
        time.sleep(1*10)


if __name__ == '__main__':
    main()
