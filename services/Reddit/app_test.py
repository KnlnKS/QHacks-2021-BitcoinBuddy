from flask import Flask, render_template, request, redirect, Response
import reddit
import fb_class
import pandas as pd
import sys, datetime

#sys.setrecursionlimit(150000)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'bonjour'

firebase_app = fb_class.fire_base_app()

@app.route('/')
def index():
    data = pd.read_csv(r'bitcoin_historical_data.csv')
    data = data.drop(['Open', 'High', 'Low', 'Vol.', 'Change %'], axis=1)
    for col in data.columns:
        print(col)
    print(data) 
    data.iloc[::-1]
    legend = 'Monthly Data'
    legend1 = "Test"
    labels = list(data.Date)
    values = list(data.Price)
    values = [i.replace(',','') for i in values]
    #values = [int(i) for i in values] 
    print(values[0])
    
    return render_template('index.html', values=values, labels=labels, legend=legend, legend1=legend1)


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
