
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

from functions import ob_data_plot
import plotly.graph_objects as go
import pandas as pd



def plot_ob(ob_data):
    bid_levels = ob_data['bid'][:]
    ask_levels = ob_data['ask'][:]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=bid_levels,
        y=list(range(20)),
        name='Bid',
        marker=dict(color='blue'),
        text=bid_levels,
        hovertemplate='Level: %{y}<br>Bid: %{x}'
    ))

    fig.add_trace(go.Bar(
        x=ask_levels,
        y=list(range(20)),
        name='Ask',
        marker=dict(color='red'),
        text=ask_levels,
        hovertemplate='Level: %{y}<br>Ask: %{x}'
    ))

    fig.update_layout(
        title='Order Book Levels',
        xaxis=dict(title='Price'),
        yaxis=dict(title='Level'),
        legend=dict(x=0.1, y=1, traceorder='normal')
    )

    return fig





def plot_line_ts(ts_line_plot):
    bid_levels = ts_line_plot['bid']
    ask_levels = ts_line_plot['ask']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ts_line_plot['timestamp'],
        y=bid_levels,
        mode='lines',
        name='Bid',
        line=dict(color='blue'),
        hovertemplate='Time: %{x}<br>Bid: %{y}'
    ))

    fig.add_trace(go.Scatter(
        x=ts_line_plot['timestamp'],
        y=ask_levels,
        mode='lines',
        name='Ask',
        line=dict(color='red'),
        hovertemplate='Time: %{x}<br>Ask: %{y}'
    ))

    fig.update_layout(
        title='Order Book Time Series',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Price'),
        legend=dict(x=0.1, y=1, traceorder='normal')
    )

    return fig




def plot_bar_ts(ts_bar_plot):

    ts_bar_plot['timestamp'] = pd.to_datetime(ts_bar_plot['timestamp'])
    ts_bar_plot['timestamp'] = ts_bar_plot['timestamp'].dt.strftime('%Y-%m-%d %H:%M')

    grouped_df = ts_bar_plot.groupby('timestamp')['spread'].apply(list).reset_index(name='spreads')

    fig = go.Figure()

    for _, row in grouped_df.iterrows():
        fig.add_trace(go.Box(
            x=[row['timestamp']] * len(row['spreads']),
            y=row['spreads'],
            name='Spread',
            marker=dict(color='blue'),
            boxpoints='outliers',  
            jitter=0.1,  
            
        ))

    fig.update_layout(
        title=None,
        xaxis=dict(title=None),
        yaxis=dict(title=None),
        showlegend=False, 
        modebar={'orientation': 'h'}  
    )

    return fig




















