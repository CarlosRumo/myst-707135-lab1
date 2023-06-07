
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: First laboratory                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: CarlosRumo                                                                       -- #
# -- license: GNU General Public License v3.0                                               -- #
# -- repository: https://github.com/CarlosRumo/myst-707135-lab1                                                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd

def f_timestamps_info(ts_list_o, ts_list_d):
    result = {}

    result['Timestamps in Origin data:'] = ''
    result['First Timestamp:'] = min(ts_list_o)
    result['Last Timestamp:'] = max(ts_list_o)
    result['Total number of orderbooks:'] = len(ts_list_o)

    result['Timestamps in Destination data:'] = ''
    result['First Timestamp:'] = min(ts_list_d)
    result['Last Timestamp:'] = max(ts_list_d)
    result['Total number of orderbooks:'] = len(ts_list_d)

    exact_match = sorted(list(set(ts_list_o) & set(ts_list_d)))
    result['Exact match of Timestamps:'] = len(exact_match)
    result['First 2 values are:'] = exact_match[:2]
    result['Last 2 values are:'] = exact_match[-2:]

    return result



def drop_null_timestamps(kraken):

    total_records_before = len(kraken)

    kraken_without_nulls = {timestamp: data for timestamp, data in kraken.items() if data is not None}

    total_records_after = len(kraken_without_nulls)

    dropped_records = total_records_before - total_records_after

    return kraken_without_nulls, total_records_before, total_records_after, dropped_records



def ob_data_plot(ob_data):
    highest_volume_timestamp = None
    highest_volume = 0

    for timestamp, data in ob_data.items():
        bid_volume = sum(data['bid_size'])
        ask_volume = sum(data['ask_size'])
        total_volume = bid_volume + ask_volume

        if total_volume > highest_volume:
            highest_volume = total_volume
            highest_volume_timestamp = timestamp

    if highest_volume_timestamp is not None:
        ob_df = ob_data[highest_volume_timestamp]
        ob_df = ob_df[['bid_size', 'bid', 'ask', 'ask_size']] 

        ob_df = pd.DataFrame(ob_df)

        return ob_df
    else:
        
        return None

    

def spread(ob_data):

    new_data = pd.DataFrame(columns=['timestamp', 'bid', 'ask', 'spread'])

    for timestamp in ob_data.keys():

        top_row = ob_data[timestamp].iloc[0]

        bid = top_row['bid']
        ask = top_row['ask']
        spread = ask - bid

        new_row = {'timestamp': timestamp, 'bid': bid, 'ask': ask, 'spread': spread}
        new_data = pd.concat([new_data, pd.DataFrame(new_row, index=[0])])

    new_data.reset_index(drop=True, inplace=True)

    return new_data



def filter_spread_above_8(ob_data):
    filtered_data = []

    for timestamp in ob_data.keys():
        bid = ob_data[timestamp]['bid']
        ask = ob_data[timestamp]['ask']

        spread = ask - bid

        spread_above_8 = spread[spread > 8]

        if not spread_above_8.empty:
            for spread_value in spread_above_8:
                filtered_row = {
                    'timestamp': timestamp,
                    'bid': bid.iloc[0],
                    'ask': ask.iloc[0],
                    'spread': spread_value
                }
                filtered_data.append(filtered_row)

    new_data = pd.DataFrame(filtered_data)
    return new_data



def calculate_imbalances(ob_data):
    imbalances = []

    for timestamps, df in ob_data.items():
        bid_size = df['bid_size']
        bid = df['bid']
        ask = df['ask']
        ask_size = df['ask_size']

        I_TOB = bid_size / (bid_size + ask_size)
        I_LOB = bid.sum() / (bid.sum() + ask.sum())

        imbalances.append({'Timestamp': timestamps, 'I_TOB': I_TOB, 'I_LOB': I_LOB})

    imbalances_df = pd.DataFrame(imbalances)
    return imbalances_df



def calculate_spread(ob_data):
    spreads = []

    for timestamps, df in ob_data.items():
        best_ask_price = df['ask'].min()
        best_bid_price = df['bid'].max()

        spread = best_ask_price - best_bid_price

        spreads.append({'Timestamp': timestamps, 'Spread': spread})

    spreads_df = pd.DataFrame(spreads)
    return spreads_df


    
def calculate_midprice(ob_data):
    midpoints = []

    for timestamp, df in ob_data.items():
        best_ask_price = df['ask'].min()
        best_bid_price = df['bid'].max()

        midpoint = 0.5 * (best_ask_price + best_bid_price)

        midpoints.append({'Timestamp': timestamp, 'Midpoint': midpoint})

    midpoints_df = pd.DataFrame(midpoints)
    return midpoints_df



def calculate_weighted_midprice(ob_data):
    weighted_midpoints = []

    for timestamp, df in ob_data.items():
        best_ask_price = df['ask'].min()
        best_bid_price = df['bid'].max()
        volume_ask = df['ask_size'].sum()
        volume_bid = df['bid_size'].sum()

        weighted_midpoint = (volume_ask / (volume_bid + volume_ask)) * best_bid_price + (volume_bid / (volume_bid + volume_ask)) * best_ask_price

        weighted_midpoints.append({'Timestamp': timestamp, 'Weighted Midpoint': weighted_midpoint})

    weighted_midpoints_df = pd.DataFrame(weighted_midpoints)
    return weighted_midpoints_df



def calculate_vwap(ob_data):
    vwap_values = []

    for timestamp, df in ob_data.items():
        volume_bid = df['bid_size'].sum()
        volume_ask = df['ask_size'].sum()
        weighted_price_bid = (df['bid'] * df['bid_size']).sum()
        weighted_price_ask = (df['ask'] * df['ask_size']).sum()
        
        vwap = (weighted_price_bid + weighted_price_ask) / (volume_bid + volume_ask)
        
        vwap_values.append({'Timestamp': timestamp, 'VWAP': vwap})

    vwap_df = pd.DataFrame(vwap_values)
    return vwap_df



def public_trade_metrics(pt_data):

    avg_price = pt_data['price'].mean()
    total_volume = pt_data['amount'].sum()
    max_price = pt_data['price'].max()
    min_price = pt_data['price'].min()
    max_volume_buy = pt_data.loc[pt_data['side'] == 'buy', 'amount'].max()
    max_volume_sell = pt_data.loc[pt_data['side'] == 'sell', 'amount'].max()
    buy_percentage = pt_data.loc[pt_data['side'] == 'buy', 'amount'].sum() / total_volume * 100
    sell_percentage = pt_data.loc[pt_data['side'] == 'sell', 'amount'].sum() / total_volume * 100

    format_price = lambda x: f'${x:,.2f}' if x > 1000 else f'${x:.2f}'

    metrics = [
        ('Average Price', format_price(avg_price)),
        ('Total Traded Volume', total_volume),
        ('Max Traded Price', format_price(max_price)),
        ('Min Traded Price', format_price(min_price)),
        ('Max Traded Volume (Buy)', max_volume_buy),
        ('Max Traded Volume (Sell)', max_volume_sell),
        ('% of Buy Trades', buy_percentage),
        ('% of Sell Trades', sell_percentage)
    ]

    metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
    return metrics_df

