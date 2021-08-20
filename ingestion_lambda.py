import requests
import json
import pandas as pd
import numpy as np
import json
import datetime
from datetime import date
import boto3

root_url = 'https://api.binance.com/api/v3/klines' # endpoint of binance to get the price for the currencies

today = date.today()


def get_price(symbol, interval = '1h'):
   
   end_date = datetime.datetime.strptime(str(today), '%Y-%m-%d') 
   start_date = end_date - datetime.timedelta(hours=23)

   # the binance api takes server time as input but since we're looking for daily price and we can't specify
   # that in servertime format, we convert the timestamp of 23 hours back from not into server time and pass
   # it inside url in addition to the currency exchange symbol and the interval we want 1h for this case
   start_time = int(start_date.timestamp() * 1000)
   end_time = int(end_date.timestamp() * 1000)
   url = root_url+'?symbol='+symbol+'&interval='+interval+'&startTime='+str(start_time)+'&endTime='+str(end_time)

   data = json.loads(requests.get(url).text)
   df = pd.DataFrame(data)
   df.columns = ['open_time',
                 'o', 'h', 'l', 'c', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
    # the servertime is then converted to datetime so as to return the values in understandable form
   df.index = [datetime.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
   return df


def lambda_handler(event,context):
   s3 = boto3.resource('s3')
   BUCKET = "programming-challenge-123-1"
   # The 24 hour price of each currency are stored in different csv files
   # lambda function requires any files to be stored inside /tmp directory
   # therefore that is the reason for doing so
   adabtc = get_price('ADABTC')
   adausdt = get_price('ADAUSDT')
   btcusdt = get_price('BTCUSDT')

   adabtc.to_csv('/tmp/ADABTC.csv')
   adausdt.to_csv('/tmp/ADAUSDT.csv')
   btcusdt.to_csv('/tmp/BTCUSDT.csv')

   s3.Bucket(BUCKET).upload_file("/tmp/ADABTC.csv", "ADABTC.csv")
   s3.Bucket(BUCKET).upload_file("/tmp/ADAUSDT.csv", "ADAUSDT.csv")
   s3.Bucket(BUCKET).upload_file("/tmp/BTCUSDT.csv", "BTCUSDT.csv")


   return 'Loaded to S3'
