from coinbase.wallet.client import Client
import pandas as pd

api_key = '9TqBvv4hpY4z2WTZ'
api_secret = '7NAXuR71bJ5QPTRoVj3QgnqD2zaHrfke'
client = Client(api_key, api_secret)

price = client.get_spot_price(currency_pair = 'BTC-USD')

print(price)

