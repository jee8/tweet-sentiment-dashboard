import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

def fetch_tweets(query, limit=100):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        tweets.append({
            "date": tweet.date,
            "content": tweet.content,
            "username": tweet.user.username,
            "followers": tweet.user.followersCount
        })
    df = pd.DataFrame(tweets)
    return df

if __name__ == "__main__":
    df = fetch_tweets("ai OR artificial intelligence lang:en", limit=50)
    print(df.head())
    df.to_csv("data/tweets_sample.csv", index=False)
    print("✅ Tweets saved to data/tweets_sample.csv")
