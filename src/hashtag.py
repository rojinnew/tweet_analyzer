"""
fetches tweets and performs feature engineering
"""

import time
import tweepy
import pandas as pd
from credential import api_key, api_secret_key, access_token, access_token_secret

def is_morning(datetime_str):
    """
    transforms date to time of day
    """
    datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    if 5 <= datetime_object.hour < 12:
        return 1
    return 0

def week_day(datetime_str):
    """
    transforms date to weekday
    """
    datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return datetime_object.strftime("%A")

def hash_tag_get_related_tweets(text_query):
    """
    fetches tweets using twitter api
    """
    # call the api
    # authorize the API Key
    authentication = tweepy.OAuthHandler(api_key, api_secret_key)
    # authorization to user's access token and access token secret
    authentication.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authentication, wait_on_rate_limit=True)
    df1 = pd.DataFrame(columns=["Tweets", "User", "User_statuses_count", "trump_biden"
                                , "user_followers", "User_location", "User_verified"
                                , "fav_count", "rt_count", "tweet_date", "created_at"
                                , "tweet_id", "tweet_text"])
    # list to store tweets
    count = 10
    _, _, tail = text_query.partition("#")
    file_name = tail
    limit = 10
    try:
        #Pulling individual tweets from query
        i = 0
        for tweet in tweepy.Cursor(api.search, q=text_query, count=count, lang="en",
                                   since_date="2020-11-01").items():
            print(i, end="\r")
            df1.loc[i, "tweet_id"] = tweet.id
            df1.loc[i, "tweet_text"] = tweet.text
            df1.loc[i, "Tweets"] = tweet.text
            df1.loc[i, "User"] = tweet.user.name
            df1.loc[i, "User_statuses_count"] = tweet.user.statuses_count
            df1.loc[i, "user_followers"] = tweet.user.followers_count #number of followers
            df1.loc[i, "User_location"] = tweet.user.location
            df1.loc[i, "User_verified"] = tweet.user.verified
            df1.loc[i, "fav_count"] = tweet.favorite_count
            df1.loc[i, "rt_count"] = tweet.retweet_count
            df1.loc[i, "tweet_date"] = tweet.created_at
            df1.loc[i, "country"] = tweet.place.name
            df1.to_csv("csv_files/{}.csv".format(file_name))
            i += 1
            if i == limit:
                break
            else:
                pass
        df1["tweet_date"] = df1.tweet_date.astype("datetime64")
        df1 = df1.sort_values(by="tweet_date")
        df1["rt_count_cumulative"] = df1.rt_count.cumsum()
        #df1 = df1.sort_values(by="tweet_date", ascending=False)
        df1["tweet_date"] = df1.tweet_date.dt.strftime("%m/%d/%y %H:%M")
        df1["is_morning"] = df1["tweet_date"].apply(lambda x: is_morning(x))
        df1["week_day"] = df1["tweet_date"].apply(lambda x: week_day(x))
        df1.to_csv("csv_files/"+ file_name + "_processed.csv")
        return file_name
    except BaseException as err:
        print("failed on_status,", str(err))
        time.sleep(3)

