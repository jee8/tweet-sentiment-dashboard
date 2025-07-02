import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import emoji
import re

# Load model and tokenizer
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Labels from the model card
labels = ['negative', 'neutral', 'positive']

# Preprocess tweet
def preprocess(text):
    text = emoji.demojize(text)  # Replace emojis with text
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)     # Remove @mentions
    text = re.sub(r"#", "", text)        # Remove hashtags
    return text.strip()

# Get sentiment label
def get_sentiment(text):
    text = preprocess(text)
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = F.softmax(logits, dim=1)
    label_id = torch.argmax(probs).item()
    return labels[label_id]

# Apply to all tweets
def analyze_file(path="data/tweets_from_api.csv"):
    df = pd.read_csv(path)
    df["sentiment"] = df["text"].apply(get_sentiment)
    df.to_csv("data/tweets_with_sentiment.csv", index=False)
    print("✅ AI-tagged tweets saved to data/tweets_with_sentiment.csv")
    return df

if __name__ == "__main__":
    df = analyze_file()
    print(df[["text", "sentiment"]].head())
