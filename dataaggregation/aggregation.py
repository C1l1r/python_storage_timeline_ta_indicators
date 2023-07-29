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
        temp_df = pd.DataFrame(columns = [])
        listofdictjson = json.loads(unpr_data)

        lower_bound = 0
        for i in range(df.shape[0]):
            try:
                x = pd.read_json(listofdictjson[i]['value'])
                x['reserve_0'] = x.r[0]
                x['reserve_1'] = x.r[1]
                x.drop('r', axis=1, inplace=True)
                x.drop(1, inplace=True)
                temp_df = pd.concat([temp_df, x], ignore_index=True)
            except Exception as e:
                lower_bound += 1
                print(f"An error occurred: {str(e)}")
                continue


        df = df.iloc[lower_bound:].reset_index(drop=True, inplace=False)
        df['reserve_0'] = temp_df['reserve_0']
        df['reserve_1'] = temp_df['reserve_1']
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['reserve_0'] = pd.to_numeric(df['reserve_0'], errors='coerce')
        df['reserve_1'] = pd.to_numeric(df['reserve_1'], errors='coerce')
        df = df.loc[df['reserve_0'].notna() & df['reserve_1'].notna()]
        df.set_index('time', inplace=True)
        df = df.sort_index(level='time')

        fig = px.line(df, x = df.index, y = 'reserve_0')
        display(fig)
        self.data=df


    def group_by_time(self, time):
        return  {
            'close' : self.data.resample(time).last().dropna()['reserve_0'],
            'open' : self.data.resample(time).first().dropna()['reserve_0'],
            'low' : self.data.resample(time).min().dropna()['reserve_0'],
            'high' : self.data.resample(time).max().dropna()['reserve_0']
        }

    def print_indicators(self, time, length, indicators = None,**kwargs):
        if indicators is None:
            indicators=list(self.indicators.keys())

        params = self.group_by_time(time)

        for i in indicators:
            print(f'--------{i}--------')
            print(self.indicators[i](length =length, **params, **kwargs ))
            print(f'----------------')






