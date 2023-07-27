from aggregation import data_aggregation

my_data = data_aggregation('https://europe-west1-hype-dev.cloudfunctions.net/storage-timeline-all?format=string&schema=ethereum.lovelyswap-v4.lovely.finance&timeLine=0x3aB9323992DFf9231D40E45C4AE009db1a35e40b')
my_data.get_data()
my_data.group_by_time('D', length = 14, smooth_step=6, indicators = ['RSI'])

