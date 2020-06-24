from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

app = Flask(__name__)

app.vars = {}

@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('new_index.html')
    else:
        app.vars['ticker'] = request.form['symbol']
        app.vars['type'] = request.form['answer_from_datatype']
        return redirect('/graph')

@app.route('/graph')
def graph():
    symbol = app.vars['ticker']
    col_name = app.vars['type']
    API_URL = "https://www.alphavantage.co/query"
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'function': 'TIME_SERIES_DAILY',
          'symbol': symbol,
          'outputsize': "compact",
          'datatype': 'json',
          'apikey':'MDSXPMP4CPANL143'} 
        
     # sending get request and saving the response as response object 
    response = requests.get(API_URL, PARAMS)
    response_json = response.json() 
    data = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
    data = data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
    data = data[[ 'Open', 'High', 'Low', 'Close', 'Volume']]
 
    ydata = [float(x) for x in data[col_name].tolist()]
    xdata = pd.to_datetime(data.index)
    p = figure(x_axis_type="datetime")
    # add a line renderer with legend and line thickness
    p.line(xdata, ydata, legend_label= symbol, line_width=2)
    p.xaxis.axis_label = 'Month'
    p.yaxis.axis_label = 'Price'
    script, div = components(p)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run()
