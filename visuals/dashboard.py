import streamlit as st
import pandas as pd
import altair as alt

# Load sentiment-labeled tweets
DATA_PATH = "data/tweets_with_sentiment.csv"

st.set_page_config(page_title="Tweet Sentiment Dashboard", layout="wide")
st.title("💬 Real-Time Tweet Sentiment Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
sentiment_filter = st.sidebar.multiselect("Sentiment", ["positive", "neutral", "negative"], default=["positive", "neutral", "negative"])
keyword = st.sidebar.text_input("Search in tweet text")

# Filter data
filtered_df = df[df["sentiment"].isin(sentiment_filter)]
if keyword:
    filtered_df = filtered_df[filtered_df["text"].str.contains(keyword, case=False)]

st.subheader(f"📊 Showing {len(filtered_df)} Tweets")

# Sentiment distribution
st.markdown("### Sentiment Distribution")
chart_data = filtered_df["sentiment"].value_counts().reset_index()
chart_data.columns = ["Sentiment", "Count"]

chart = alt.Chart(chart_data).mark_bar().encode(
    x="Sentiment",
    y="Count",
    color="Sentiment"
).properties(width=600)
st.altair_chart(chart)

# Tweet viewer
st.markdown("### 📝 Tweets")
st.dataframe(filtered_df[["text", "sentiment"]].reset_index(drop=True), use_container_width=True)
