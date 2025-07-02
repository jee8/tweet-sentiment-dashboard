import pandas as pd
from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

def process_tweets(csv_path="data/tweets_from_api.csv"):
    df = pd.read_csv(csv_path)
    df["sentiment"] = df["text"].apply(analyze_sentiment)
    return df

if __name__ == "__main__":
    df = process_tweets()
    print(df[["text", "sentiment"]].head())
    df.to_csv("data/tweets_with_sentiment.csv", index=False)
    print("✅ Sentiment-tagged tweets saved to data/tweets_with_sentiment.csv")
