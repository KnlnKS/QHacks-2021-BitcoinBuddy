from flask import Flask, render_template, request, redirect, Response, url_for
import reddit
import fb_class
import pandas as pd
import sys, datetime

from coinbase_api import get_price

#sys.setrecursionlimit(150000)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bonjour'

firebase_app = fb_class.fire_base_app()

def twitter_pie(data_type, currency):
    if currency == 'bitcoin':
        csv_pie = 'tweet_data_btc.csv'
    else:
        csv_pie = 'tweet_data_eth.csv'

    data = pd.read_csv(csv_pie)
    positive_val = 0 
    negative_val = 0 
    neutral_val = 0
    for _,row in data.iterrows():
        if row['score'] > 0:
            positive_val += (row['score'] * row['magnitude'])
        elif row['score'] < 0:
            negative_val += (row['score'] * row['magnitude'])
        else:
            neutral_val += row['magnitude']
    
    return positive_val, neutral_val, negative_val

def reddit_pie(data_type, currency):
    pass


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.form:
        currency = request.form['currency']
        return redirect(url_for("display_crypto", currency=currency))
    else:
        return render_template('index.html')

@app.route('/currency/<currency>', methods=['POST', 'GET'])
def display_crypto(currency, data_type='twitter'):

    price_data = get_price(currency)
    price = price_data['amount']

    csv = currency + '_historical_data.csv'
    data = pd.read_csv(csv)
    data = data.drop(['Open', 'High', 'Low', 'Vol.', 'Change %'], axis=1)
    for col in data.columns:
        print(col)
    #print(data) 
    data_small = data.head(6)

    print(data_small)

    data_small = data_small.iloc[::-1]
    data_small = data_small.iloc[:5:]
    value_small = list(data_small.Price)
    label_small = list(data_small.Date)

    if currency in ['bitcoin', 'ethereum']:
        value_small = [i.replace(',','') for i in value_small]

    data1 = data.head(10)
    data1 = data1.iloc[::-1]
    data = data.iloc[10::10]
    data = data.iloc[::-1]

    print(data)
    values1 = list(data1.Price)
    values2 = list(data.Price)

    labels1 = list(data1.Date)
    labels2 = list(data.Date)
    #labels = list(data.Date)
    #values = list(data.Price)

    labels = labels2 + labels1
    values = values2 + values1
    if currency in ['bitcoin', 'ethereum']:
        values = [i.replace(',','') for i in values]
    #values = [int(i) for i in values] 
    print(values[0])

    positive_val = 0
    negative_val = 0
    neutral_val = 0

    csv_pie = ''
    if data_type == 'twitter':
        positive_val, neutral_val, negative_val = twitter_pie(data_type, currency)
    elif data_type == 'reddit':
        positive_val, neutral_val, negative_val = reddit_pie(data_type, currency)
        


    positive = positive_val
    neutral = neutral_val
    negative = -negative_val #nos

    #labels pie chart
    data_type_label = "Sentiment data from " + data_type
    positive_label  = "Positive sentiments from " + data_type
    neutral_label  = "Neutral sentiments from " + data_type
    negative_label  = "Negative sentiments from " + data_type
    
    if request.form.get('currency'):
        currency = request.form['currency']
        return redirect(url_for('display_crypto', currency=currency, data_type=data_type))
        #return redirect(url_for('filler', currency=currency))
    elif request.form.get('data_type'):
        data_type = request.form['data_type']
        return redirect(url_for('display_crypto', currency=currency, data_type=data_type))
    else:
        return render_template('data.html', labels=labels, values=values, value_small=value_small, label_small=label_small, 
        currency=currency, price=price, positive=positive, neutral=neutral, negative=negative, data_type_label=data_type_label, 
        positive_label=positive_label, neutral_label=neutral_label, negative_label=negative_label)

# @app.route('/temp')
# def filler(currency):

#     return redirect(url_for('display_crypto', currency=currency))

if __name__ == "__main__":

    #exchanges = api.metadata_list_exchanges()

    #for exchange in exchanges:
    #    print(exchange['name'])
    app.run(debug=True)
'''
    data_table = reddit.create_table(reddit.bitcoin)
    data_table.to_csv('out.csv', index=False)
    #firebase_app.add_data("test", data_table)
'''
