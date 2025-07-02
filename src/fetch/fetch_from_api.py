import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

def create_headers():
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

def fetch_tweets_api(query="AI", max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        'query': query,
        'max_results': max_results,
        'tweet.fields': 'created_at,text,author_id,lang',
    }

    response = requests.get(search_url, headers=create_headers(), params=params)

    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}, {response.text}")

    tweets = response.json().get("data", [])
    df = pd.DataFrame(tweets)
    return df

if __name__ == "__main__":
    df = fetch_tweets_api("AI lang:en", max_results=20)
    print(df.head())
    df.to_csv("data/tweets_from_api.csv", index=False)
    print("✅ Tweets saved to data/tweets_from_api.csv")
