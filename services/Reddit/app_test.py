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
    return render_template('index.html')


if __name__ == "__main__":

    exchanges = api.metadata_list_exchanges()

    for exchange in exchanges:
        print(exchange['name'])
    app.run(debug=True)
'''
    data_table = reddit.create_table(reddit.bitcoin)
    data_table.to_csv('out.csv', index=False)
    #firebase_app.add_data("test", data_table)
'''
