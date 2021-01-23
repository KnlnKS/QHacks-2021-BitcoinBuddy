from flask import Flask, render_template, request, redirect, Response, url_for
import reddit
import fb_class
import pandas as pd
import sys, datetime

#sys.setrecursionlimit(150000)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bonjour'

firebase_app = fb_class.fire_base_app()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.form:
        currency = request.form['currency']
        return redirect(url_for("display_crypto", currency=currency))
    else:
        return render_template('index.html')

@app.route('/currency/<currency>', methods=['POST', 'GET'])
def display_crypto(currency):
    csv = currency + '_historical_data.csv'
    data = pd.read_csv(csv)
    data = data.drop(['Open', 'High', 'Low', 'Vol.', 'Change %'], axis=1)
    for col in data.columns:
        print(col)
    #print(data) 
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
    
    if request.form:
        currency = request.form['currency']
        return redirect(url_for('display_crypto', currency=currency))
        return redirect(url_for('filler', currency=currency))
    else:
        return render_template('data.html', labels=labels, values=values)

@app.route('/temp')
def filler(currency):

    return redirect(url_for('display_crypto', currency=currency))

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
