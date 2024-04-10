import os
import requests
import time
from dotenv import load_dotenv, dotenv_values
from datetime import datetime
load_dotenv()

COINMARKETCAP_API = os.getenv('COINMARKETCAP_API_KEY')
IFTTT_WEBHOOKS_URL = os.getenv('IFTTT_WEBHOOKS_URL')
COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

test = 'https://maker.ifttt.com/trigger/{}/with/key/c-Bvksw_rHomvDdLY388El'


def get_latest_crypto_price(coin, currency):
    response = requests.get(COINMARKETCAP_API_URL)

    parameters = {
        'symbol': coin,
        'convert': currency
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API
    }

    response = requests.get(
        COINMARKETCAP_API_URL, params=parameters, headers=headers).json()
    return float(response['data'][coin]['quote'][currency]['price'])


def post_ifttt_webhook(event, coin, value, currency):
    data = {'value1': coin,
            'value2': value,
            'value3': currency}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)


# Format prices and time & date
def format_crypto_history(crypto_history):
    rows = []
    for crypto_price in crypto_history:
        date = crypto_price['date'].strftime('%d.%m.%Y %H.%M')
        price = crypto_price['price']
        row = '{}: <b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)


def main():
    coin = input("Which coin would you like to see the value of? (ENTER COIN CODE)\n")
    currency = input("Which currency would you like to see the value of " + coin + " in? (ENTER THREE-LETTER CODE)\n")
    frequency = int(input("How often (in hours) would you like to recieve updates?\n"))
    print("Thank you. You will recieve updates about " + coin + " in " + currency + " every " + str(frequency) + " hour(s)")
    crypto_history = []
    while (True):
        price = get_latest_crypto_price(coin, currency)
        date = datetime.now()
        crypto_history.append({'date': date, 'price': price})

        post_ifttt_webhook('crypto_price_update', coin, format_crypto_history(crypto_history), currency)

        # Set the number of different prices that are sent as notification
        if len(crypto_history) == 5:
            # Clear price history list
            crypto_history = []
        # Set the interval between prices checks (in seconds)
        time.sleep(frequency * 3600)


if __name__ == '__main__':
    main()
