
import boto3
import pandas as pd
import json

s3 = boto3.client('s3')
BUCKET = "programming-challenge-123-1"  # bucket name on S3 where the results from the ingestion will be stored

s3.download_file(BUCKET,'ADAUSDT.csv','/tmp/ADAUSDT.csv') # file where daily price of ADAUSDT is stored
s3.download_file(BUCKET,'ADABTC.csv','/tmp/ADABTC.csv') # file where daily price of ADABTC is stored
s3.download_file(BUCKET,'BTCUSDT.csv','/tmp/BTCUSDT.csv') # file where daily price of BTCUSDT is stored



def get_price(symbol):
    # retreive the latest hourly data from S3 for the specific currency the user asks for
    if symbol == 'ADAUSDT':
        df = pd.read_csv('/tmp/ADAUSDT.csv')
        latest_data = df.tail(1)
        result = latest_data.to_json(orient='records')[1:-1].replace('},{', '} {')

    elif symbol == 'ADABTC':
        df = pd.read_csv('/tmp/ADABTC.csv')
        latest_data = df.tail(1)
        result = latest_data.to_json(orient='records')[1:-1].replace('},{', '} {')

    elif symbol == 'BTCUSDT':
        df = pd.read_csv('/tmp/BTCUSDT.csv')
        latest_data = df.tail(1)
        result = latest_data.to_json(orient='records')[1:-1].replace('},{', '} {')

    else:
        result = None
    return result

def get_profit(symbol, amount):
    # calculate the amount of profit that could have been made within the last 24 hours
    # by taking the difference of the high and low price at the last hour and multiplying
    # it by the amount of currency

    if symbol == 'ADAUSDT':
        df = pd.read_csv('/tmp/ADAUSDT.csv')
        latest_data = df.tail(1)
        profit = amount*((float(latest_data.h))-(float(latest_data.l)))
        result = str(profit) + symbol[-4:]

    elif symbol == 'ADABTC':
        df = pd.read_csv('/tmp/ADABTC.csv')
        latest_data = df.tail(1)
        profit = amount*((float(latest_data.h))-(float(latest_data.l)))
        result = str(profit) + symbol[-3:]

    elif symbol == 'BTCUSDT':
        df = pd.read_csv('/tmp/BTCUSDT.csv')
        latest_data = df.tail(1)
        profit = amount*((float(latest_data.h))-(float(latest_data.l)))
        result = str(profit) + symbol[-4:]

    else:
        result = None
    return result

def lambda_handler(event,context):
    # This is implemented to provide informatio for the two endpoints,
    # one to show the price, and two to show the profit
    # the system only accepts the three currencies ADAUSDT, ADABTC and BTCUSDT
    
    x = ""
    if "value" in event and "currency" in event : # this is for extracting the profit which needs the value and currency as input
        value = event['value']
        currency = event['currency']
        x = get_profit(currency,int(value))
        if x != None:
            return {
                    'statusCode'  : 200,

                    'Profit': x
            }
        else:
            return {
                    'statusCode': 400,
                    'error': "Please enter currencies ADAUSDT, ADABTC or BTCUSDT and valid value" }



    elif "currency" in event: # this is for extracting the hourly price information only
        currency = event['currency']
        x = get_price(currency)

        if x != None:
            return {
                    'statusCode'  : 200,
                    'Price': x
            }
        else:
            return {
                    'statusCode': 400,
                    'error': "Please enter currencies ADAUSDT, ADABTC or BTCUSDT " }


    else:

        return {
                    'statusCode': 500,
                    'error': "internal server error "
            }





