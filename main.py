
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: First laboratory                                                        -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: CarlosRumo                                                                     -- #
# -- license: GNU General Public License v3.0                                               -- #
# -- repository: https://github.com/CarlosRumo/myst-707135-lab1                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


import pandas as pd
import data as dt
import os
import sys

project_folder = os.path.abspath('')
sys.path.insert(0,project_folder)

import functions as fn
import json
import functions as fn

# Opening JSON file
f = open('files/orderbooks_06jun2021.json')

# Returns JSON object as a dictionary
orderbooks_data = json.load(f)

bitfinex_ts = list(orderbooks_data['bitfinex'].keys())
kraken_ts = list(orderbooks_data['kraken'].keys())

q1_results = fn.f_timestamps_info(ts_list_o=bitfinex_ts, ts_list_d=kraken_ts)

result = q1_results
print('Timestamps in Origin data:')
print('First Timestamp:', result['First Timestamp:'])
print('Last Timestamp:', result['Last Timestamp:'])
print('Total number of orderbooks:', result['Total number of orderbooks:'])
print()
print('Timestamps in Destination data:')
print('First Timestamp:', result['First Timestamp:'])
print('Last Timestamp:', result['Last Timestamp:'])
print('Total number of orderbooks:', result['Total number of orderbooks:'])
print()
print('Exact match of Timestamps:', result['Exact match of Timestamps:'])
print('First 2 values are:')
print(result['First 2 values are:'])
print('Last 2 values are:')
print(result['Last 2 values are:'])


display(bitfinex_ts[0:4])
display(kraken_ts[0:4])


ob_data = orderbooks_data['kraken']


kraken_without_nulls, before, after, dropped = fn.drop_null_timestamps(kraken=ob_data)

display("Number of historical Kraken orderbooks:")
display(f"Before dropping Nones: {before}")
display(f"After dropping Nones: {after}")

display('First timestamp: ' + list(kraken_without_nulls.keys())[0])
print('')
display('The Orderbook data is the following:')
print('')
display(pd.DataFrame(kraken_without_nulls[list(kraken_without_nulls.keys())[0]]))

display('Last timestamp: ' + list(kraken_without_nulls.keys())[-1])
print('')
display('The Orderbook data is the following:')
print('')
display(pd.DataFrame(kraken_without_nulls[list(kraken_without_nulls.keys())[-1]]))


ob_data = {orderbook: pd.DataFrame(kraken_without_nulls[orderbook])[['bid_size', 'bid', 'ask', 'ask_size']]
           for orderbook in list(kraken_without_nulls.keys())}


ob_data[list(ob_data.keys())[1]]


#Q3 : Make a horizontal barplot for the Orderbook representation (4pt)
ob_data_plot = fn.ob_data_plot(ob_data)

ob_data_plot.head()

plot_ob = vs.plot_ob(ob_data=ob_data_plot,timestamp='2021-07-05T13:07:10.414Z')
plot_ob.show()


# Q4 : Can you calculate the historical bid, ask and spread ? (2pt)
df_ts_tob = fn.spread(ob_data)
df_ts_tob


#Q5 : Display the timestamps above a particular spread value (2pt)
fn.filter_spread_above_8(ob_data)


#Q6 : Create a timeseries plot with bid and ask (Line plot) (2pt)
plot_2 = vs.plot_line_ts(ts_line_plot=df_ts_tob)
plot_2.show()


#Q7 : Create a boxplot graph with Spreads (5pt) 
df_ts_tob['spread'].describe()

plot_3 = vs.plot_bar_ts(ts_bar_plot=df_ts_tob)
plot_3.show()


#Q8 : Create Orderbook Imbalance Metric for all Orderbooks (2pt)
results_q8 = fn.calculate_imbalances(ob_data=ob_data)
display(results_q8)


#Q9 : Create Spread Metric for all Orderbooks (2pt)
results_q9 = fn.calculate_spread(ob_data=ob_data)
display(results_q9)


#Q10 : Create Midprice Metric for all Orderbooks (2pt)
results_q10 = fn.calculate_midprice(ob_data=ob_data)
display(results_q10)


#Q11 : Create Weighted Midprice Metric for all Orderbooks (2pt) 
results_q11 = fn.calculate_weighted_midprice(ob_data=ob_data)
display(results_q11)


#Q12 : Volume-Weighted Mid Price (4 pts)
results_q12 = fn.calculate_vwap(ob_data=ob_data)
display(results_q12)


#Public Trades
file_path = "files/publictrades_actualizado.parquet"
pt_data = dt.read_data(file_path)

display(pt_data)


#Q13 : Can you produce the following DataFrame of statistics ? (35pt) 
result_q13 = fn.public_trade_metrics(pt_data=pt_data)
result_q13