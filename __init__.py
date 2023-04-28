import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
import json
from pandas import json_normalize
import pandas_ta as ta
import plotly.express as px

class data_aggregation:

    indicators = {
        'RSI' : ta.rsi,
        'STOCH' : ta.stoch,
        'STOCHRSI' : ta.stochrsi,
        'ADX' : ta.adx,
        'MACD' : ta.macd,
        'WILLIAMS' : ta.willr,
        'CCI' : ta.cci,
        'ATR' : ta.atr,
        'HIGHLOW': ta.high_low_range,
        'ULTOSC': ta.uo,
        'ROC': ta.roc,
        'MA': lambda *args, **kwargs: (ta.sma(*args, **kwargs), ta.ema(*args, **kwargs))


    }

    def __init__(self, url):
        self.url = url
        self.data = None

    def get_data(self):
        if self.data is not None:
            return self.data
        self.update()
        return self.data

    def update(self):
        try:
            with urllib.request.urlopen(self.url) as f:
                unpr_data = f.read().decode('utf-8')
        except urllib.error.URLError as e:
            print(e.reason)
        df = pd.read_json(unpr_data).drop(['value'], axis=1)
        temp_df = pd.DataFrame(columns = ['address', 'price','address1', 'price1'])
        listofdictjson = json.loads(unpr_data)

        for i in range(df.shape[0]):
            x = pd.read_json(listofdictjson[i]['value'])
            x['address1'] = x.address[1]
            x['price1'] = x.price[1]
            temp_df = pd.concat([temp_df, x.drop([1],axis = 0)], ignore_index=True)
        df = pd.concat([df, temp_df], axis=1)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price1']  = pd.to_numeric(df['price1'], errors='coerce')
        df = df.loc[df['price'].notna() & df['price1'].notna()]
        df.set_index('time', inplace = True)
        fig = px.line(df, x = df.index, y = 'price')
        display(fig)
        self.data=df


    def group_by_time(self, time, length,  indicators = None, **kwargs):
        if indicators is None:
            indicators=list(self.indicators.keys())

        params = {
            'close' : self.data.resample(time).last().dropna()['price'],
            'open' : self.data.resample(time).first().dropna()['price'],
            'low' : self.data.resample(time).min().dropna()['price'],
            'high' : self.data.resample(time).max().dropna()['price']
        }

        for i in indicators:
            print(f'--------{i}--------')
            print(self.get_indicator(i)(length =length, **params, **kwargs ))
            print(f'----------------')



    def get_indicator(self, name):
        return self.indicators[name]

