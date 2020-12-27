"""
contains user plots functions
"""
import os
import time
import pandas as pd
import plotly
from plotly import graph_objects as go
from plotly.subplots import make_subplots

def plot_user_piechart(input):
    """
    generates piechart
    """
    data_frame = pd.read_csv("csv_files/"+ input +"_processed.csv")
    counters = data_frame["week_day"].value_counts().tolist()#value_counts
    counter_keys = data_frame["week_day"].value_counts().keys().tolist()
    layout = go.Layout(autosize=True, title="<b>number of tweets of a user in various days of a week</b>", width=280)
    trace = go.Pie(labels=counter_keys, values=counters)
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(title_x=0.4)
    fig.show()
    plotly.io.orca.config.executable = "/usr/local/bin/orca"
    new_graph_name = "piechart" + str(time.time()) + ".png"
    for filename in os.listdir("static/"):
        if filename.startswith("piechart"):  # not to remove other images
            os.remove("static/" + filename)
    fig.write_image("static/" + new_graph_name)
    #fig.show()
    return new_graph_name


def plot_trend(input):
    """
    generates scatter plots
    """
    data_frame = pd.read_csv("csv_files/" + input + "_processed.csv")
    data_frame = data_frame.drop_duplicates(subset='tweet_date', keep="last")
    tweet_date = list(data_frame.tweet_date)
    rt_count = list(data_frame["rt_count"])
    user_cumulative = list(data_frame["rt_count_cumulative"])#the chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=tweet_date, y=rt_count, marker_color='indianred',
                             mode='lines+markers', name='User Retweets'))

    fig.add_trace(go.Bar(x=tweet_date, y=user_cumulative, marker_color='indianred',
                         opacity=.4, name='User Retweets Cumulative'), secondary_y=True)
    
    fig.update_layout(template='plotly_white', title='<b> User Retweet Metrics </b>',
                      barmode='group', bargap=0, bargroupgap=0.01, width=700,)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_layout(title_x=0.5)
    
    #fig.show()
    plotly.io.orca.config.executable = "/usr/local/bin/orca"
    new_graph_name = "trend" + str(time.time()) + ".png"
    for filename in os.listdir("static/"):
        if filename.startswith("trend"):  # not to remove other images
            os.remove("static/" + filename)
    fig.write_image("static/" + new_graph_name)
    fig.show()
    return new_graph_name
