from coinbase.wallet.client import Client
import pandas as pd

api_key = '9TqBvv4hpY4z2WTZ'
api_secret = '7NAXuR71bJ5QPTRoVj3QgnqD2zaHrfke'
client = Client(api_key, api_secret)

def get_price(currency):
    currencies = {'bitcoin':'BTC', 'ethereum':'ETH', 'chainlink':'LINK', 'litecoin':'LTC'}
    curr_code = currencies[currency]

    curr_pair = curr_code + '-USD'
    price = client.get_spot_price(currency_pair = curr_pair)

    return(price)
    

