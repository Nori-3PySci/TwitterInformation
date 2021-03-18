# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import tweepy
import datetime
import pandas as pd

account = "account"

timenow = datetime.datetime.now()

consumer_key = 'consumer key'
consumer_secret = 'consumer secret'
access_token = 'access token'
access_token_secret = 'access token secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)

# +
data = r"/path/data.csv"

output_tweet = r"/path/tweet_log/" + str(timenow.strftime("%Y%m%d_%H%M%S")) + ".txt"

# column_name = ["date", "tweet", "favorite", "follow", "follower", "retweet_tw", "favorite_tw"]

df = pd.read_csv(data)

df["date"] = pd.to_datetime(df["date"])


# -

def main():
    user = api.get_user(account)

    tweet_num = user.statuses_count
    favorite_num = user.favourites_count
    follow_num = user.friends_count
    follower_num = user.followers_count

    # print(tweet_num, favorite_num, follow_num, follower_num)

    tweets = tweepy.Cursor(api.user_timeline, tweet_mode = 'extended', id=account).items(100)

    tw_favorite_num = 0; tw_retweet_num = 0
    
    with open(output_tweet, "w") as f:
    
        for tw in tweets:
            if df.iloc[-1]["date"] < (tw.created_at + datetime.timedelta(hours=9)):
                if not (tw.full_text.startswith("RT")) or (tw.full_text.startswith("@")):
#                     print(tw.full_text + "\n")
                    f.write(tw.full_text)
                    tw_retweet_num = tw_retweet_num + tw.retweet_count
                    tw_favorite_num = tw_favorite_num + tw.favorite_count

    # print(tw_retweet_num, tw_favorite_num)
    
    api.update_status(str(timenow.strftime("%Y年%m月%d日")) + 
                      "\nツイート数　　　　：" + str(tweet_num - df.iloc[-1]["tweet"]) + "(計：" + str(tweet_num) + ")" +
                      "\nいいねした数　　　：" + str(favorite_num - df.iloc[-1]["favorite"]) + "(計：" + str(favorite_num) + ")" +
                      "\nフォロー数　　　　：" + str(follow_num - df.iloc[-1]["follow"])  + "(計：" + str(follow_num) + ")" +
                      "\nフォロワー数　　　：" + str(follower_num - df.iloc[-1]["follower"]) + "(計：" + str(follower_num) + ")" +
                      "\nリツイートされた数：" + str(tw_retweet_num) +
                      "\nいいねされた数　　：" + str(tw_favorite_num)) 
    
    df.loc[str(len(df))] = [timenow, tweet_num, favorite_num, follow_num, follower_num, tw_retweet_num, tw_favorite_num]

    df.to_csv(data, index=False)

if __name__ == '__main__':
    main()
