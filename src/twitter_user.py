"""
This code fetches the user info and tweet
"""
import time
from datetime import datetime
import tweepy
import pandas as pd
from credential import api_key, api_secret_key, access_token, access_token_secret

def is_morning(datetime_str):
    """
    transform date to time of day
    """
    #datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    datetime_object = datetime.strptime(datetime_str, "%m/%d/%y %H:%M")
    if 5 <= datetime_object.hour < 12:
        return 1
    return 0

def week_day(datetime_str):
    """
    transforms date to weekdays
    """
    #datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    datetime_object = datetime.strptime(datetime_str, "%m/%d/%y %H:%M")

    return datetime_object.strftime("%A")

def get_related_tweets(text_query):
    """
    fetched the tweets and perform feature engineering
    """
    data_frame = pd.DataFrame(columns=["Tweets", "User", "User_statuses_count", "trump_biden",
                                       "user_followers", "User_location", "User_verified",
                                       "fav_count", "rt_count", "tweet_date", "created_at",
                                       "tweet_id", "tweet_text"])
    # list to store tweets
    # no of tweets
    count = 10
    #file_name = "fridayfeeling"
    _, _, tail = text_query.partition("@")
    text_query = "from:" + tail
    file_name = tail
    limit = 10
    # authorize the API Key
    authentication = tweepy.OAuthHandler(api_key, api_secret_key)
    # authorization to user's access token and access token secret
    authentication.set_access_token(access_token, access_token_secret)
    # call the api
    api = tweepy.API(authentication, wait_on_rate_limit=True)
    print("..............")
    try:
        
        #Pulling individual tweets from query
        i = 0
        for tweet in tweepy.Cursor(api.search, q=text_query, count=count, lang="en",
                                   since_date="2020-11-01").items():
            print(i, end="\r")
            data_frame.loc[i, "tweet_id"] = tweet.id
            data_frame.loc[i, "tweet_text"] = tweet.text
            data_frame.loc[i, "Tweets"] = tweet.text
            data_frame.loc[i, "User"] = tweet.user.name
            data_frame.loc[i, "User_statuses_count"] = tweet.user.statuses_count
            data_frame.loc[i, "user_followers"] = tweet.user.followers_count
            data_frame.loc[i, "User_location"] = tweet.user.location
            data_frame.loc[i, "User_verified"] = tweet.user.verified
            data_frame.loc[i, "fav_count"] = tweet.favorite_count
            data_frame.loc[i, "rt_count"] = tweet.retweet_count
            data_frame.loc[i, "tweet_date"] = tweet.created_at
            data_frame.loc[i, "country"] = tweet.place.name
            data_frame.to_csv("csv_files/{}.csv".format(file_name))
            i += 1
            if i == limit:
                break
            else:
                pass
            
        #data_frame = pd.read_csv("csv_files/"+file_name + ".csv")
        data_frame["tweet_date"] = data_frame.tweet_date.astype("datetime64")
        data_frame = data_frame.sort_values(by="tweet_date", ascending=True)
        data_frame["rt_count_cumulative"] = data_frame.rt_count.cumsum()
        data_frame["tweet_date"] = data_frame.tweet_date.dt.strftime("%m/%d/%y %H:%M")
        #data_frame["is_morning"] = data_frame["tweet_date"].apply(lambda x: is_morning(x))
        data_frame["week_day"] = data_frame["tweet_date"].apply(lambda x: week_day(x))
        data_frame.to_csv("csv_files/" + file_name + "_processed.csv")
        return file_name
    
    
    
    except BaseException as err:
        print("failed on_status,", str(err))
        time.sleep(3)

