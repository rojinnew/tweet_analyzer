"""
generates plots for the the hashtags
"""
import re
import os
import time
import pandas as pd
from textblob import TextBlob
import plotly
from plotly import graph_objects as go

def plot_piechart(input):
    """
    returns piechart
    """
    data_frame = pd.read_csv("csv_files/" + input + "_processed.csv")
    counters = data_frame["week_day"].value_counts().tolist()
    counter_keys = data_frame["week_day"].value_counts().keys().tolist()
    layout = go.Layout(autosize=True, title=" <b> number of tweets with " + input + " hashtag</b>")
    trace = go.Pie(labels=counter_keys, values=counters)
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(title_x=0.4)
    #fig.show()

    plotly.io.orca.config.executable = "/usr/local/bin/orca"
    new_graph_name = "piechart" + str(time.time()) + ".png"
    for filename in os.listdir("static/"):
        if filename.startswith("piechart"):
            os.remove("static/" + filename)
    fig.write_image("static/" + new_graph_name)
    return new_graph_name

def plot_barchart(input):
    '''
    returns barchart
    '''
    data_frame = pd.read_csv("csv_files/" + input + "_processed.csv")
    counters = data_frame["week_day"].value_counts().tolist()
    counter_keys = data_frame["week_day"].value_counts().keys().tolist()
    layout = go.Layout(title="<b>number of tweets in various days of a week</b>",
                       plot_bgcolor="#FFFFFF",
                       legend=dict(itemclick="toggleothers", itemdoubleclick="toggle",),
                       xaxis=dict(title="days of week", linecolor="#BCCCDC",),
                       yaxis=dict(title="tweet count", linecolor="#BCCCDC"))

    colors = [" #009900"] * len(counters)
    fig = go.Figure([go.Bar(x=counter_keys, y=counters, marker_color=colors)], layout=layout)

    plotly.io.orca.config.executable = "/usr/local/bin/orca"
    new_graph_name = "barchart" + str(time.time()) + ".png"
    for filename in os.listdir("static/"):
        if filename.startswith("barchart"):
            os.remove("static/" + filename)
    fig.write_image("static/" + new_graph_name)
    return new_graph_name


def get_tweet_sentiment(tweet):
    """
    this is a local function to get tweets sentiment
    """
    #create TextBlob object of passed tweet text
    analysis = TextBlob(" ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))
    result = analysis.sentiment.polarity #set sentiment
    if result < 0:
        return "negative"
    if result == 0:
        return "neutral"
    if result > 0:
        return "positive"

def tweet_sentiment(input):
    """
    records tweets sentiment in dataframe
    """
    data_frame = pd.read_csv("csv_files/" + input + "_processed.csv")
    data_frame["sentiment"] = data_frame["tweet_text"].apply(lambda x: get_tweet_sentiment(x))
    data_frame.to_csv("csv_files/" + input +"_sentiment_processed.csv")

def plot_grouped_barchart(input):
    """
    creates grouped barchart
    """
    tweet_sentiment(input)
    data_frame = pd.read_csv("csv_files/" + input + "_sentiment_processed.csv")
    days = list(data_frame.week_day.unique())
    polarity = ["positive", "neutral", "negative"]
    dict_value = {}
    for pol in polarity:
        dict_value[pol] = {}
        for day in days:
            dict_value[pol][day] = 0

    for filter_keyword in days:
        polarity = data_frame[data_frame["week_day"] == \
                              filter_keyword]["sentiment"].value_counts().keys().tolist()
        polarity_value = data_frame[data_frame["week_day"] == \
                              filter_keyword]["sentiment"].value_counts().tolist()
        for i in range(0, len(polarity)):
            dict_value[polarity[i]][filter_keyword] = polarity_value[i]

    pos, neg, neu = [], [], []
    for key in days:
        pos.append(dict_value["positive"][key])
        neg.append(dict_value["negative"][key])
        neu.append(dict_value["neutral"][key])

    layout = go.Layout(title="<b>sentiment anslysis of " + input +" hashtag </b>",
                       title_x=0.4,
                       plot_bgcolor="#FFFFFF",
                       legend=dict(itemclick="toggleothers", itemdoubleclick="toggle",),
                       xaxis=dict(title="days of week - sentiment", linecolor="#BCCCDC",),
                       yaxis=dict(title="tweet count", linecolor="#BCCCDC"))

    fig = go.Figure(data=[go.Bar(name="positive", x=days, y=pos),
                          go.Bar(name="negative", x=days, y=neg),
                          go.Bar(name="neutral", x=days, y=neu)], layout=layout)

    #fig.show()
    plotly.io.orca.config.executable = "/usr/local/bin/orca"
    new_graph_name = "group_bar" + str(time.time()) + ".png"
    for filename in os.listdir("static/"):
        if filename.startswith("group"):
            os.remove("static/" + filename)
    fig.write_image("static/" + new_graph_name)
    return new_graph_name
