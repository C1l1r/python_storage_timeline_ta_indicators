# python_storage_timeline_ta_indicators
This library reads, cleans and sorts data acquired from web database. 
Values in a storage expected to be in a json format with a following structure:

```{"time":1684968241256,"value":"{\"r\":[49208.040463174424,730195614842.3989]}"}```

Class data aggregation takes link as an argument to create instance of a database. The data from the database could be updated manualy via ```update``` function.

To calculate ta indicators function ```print_indicators``` should be used that takes next arguments:


```time``` in "2D", "4S" or "W" format that denotes length of even interwals time series will be divided.


```length``` takes int input and stands for number of intervals that will be used to calculate the indicator.


```indicators``` takes one (or multiple) of 'RSI', 'STOCH', 'STOCHRSI', 'ADX', 'MACD', 'WILLIAMS', 'CCI', 'ATR', 'HIGHLOW', 'ULTOSC', 'ULTOSC', 'ROC', 'MA'. If is None
calculates all of listed.

**IMPORTANT**
Some indicators require additional arguments. They should be added to ```print_indicators``` function with names used in ```ta-lib```.

### CODE EXAMPLE ###

```
from dataaggregation.aggregation import data_aggregation

my_data = data_aggregation('thelinkgoeshere')
my_data.get_data()
my_data.print_indicators('D', length = 14, smooth_step=6, indicators = ['RSI'])
```

## Anomaly detection ##

Should only be used with a great understanding of features of data it was trained on. Works best on a volatile time series with high liquidity.  

### CODE EXAMPLE ###

```
from dataaggregation.aggregation import lstm_anomaly_detection

anms = lstm_anomaly_detection(url = 'thelinkgoeshere')
anms.detect_anomalies(threshold=1.25)
```

#### Output example####

![Output sample](https://github.com/C1l1r/python_storage_timeline_ta_indicators/blob/lstm_functional_branch/detected%20anomalies%20sample.png?raw=true)

#### NOW AVALIABLE ON PIP! #####

pip install python_storage_timeline_ta_indicators






