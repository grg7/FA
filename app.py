# %%
# Install required libraries (you can run this separately in your notebook if needed)
#!pip install streamlit feedparser pandas

# Import libraries
import streamlit as st
import feedparser
import pandas as pd

# RSS feed sources
rss_feeds = [
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.investing.com/rss/news.rss",
    "https://www.reuters.com/finance/markets/rss",
    "https://www.bloomberg.com/feed/podcast/etf-report.xml"
]

# Fetch news
def fetch_news(feed_urls):
    news_items = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        # Check if feed.feed exists and has a title, otherwise use the URL as source
        source_title = feed.feed.title if hasattr(feed.feed, 'title') else url
        for entry in feed.entries:
            # Use getattr() with a default value to safely access attributes that might be missing
            title = getattr(entry, 'title', 'No Title Available')
            link = getattr(entry, 'link', '#') # Use '#' or a placeholder for missing links

            news_items.append({
                "title": title,
                "link": link,
                "source": source_title
            })
    return news_items

# Filter news
def filter_news(news_items, source=None, keyword=None):
    return [
        item for item in news_items
        if (not source or source.lower() in item["source"].lower()) and
           (not keyword or keyword.lower() in item["title"].lower())
    ]

# Streamlit UI
st.title("📈 Financial News Aggregator")

source_filter = st.text_input("Filter by Source")
keyword_filter = st.text_input("Filter by Keyword")

# Cache the news fetching to avoid re-fetching every time the UI updates
@st.cache_data(ttl=600) # Cache for 10 minutes
def get_news(urls):
    return fetch_news(urls)

if st.button("Fetch News"):
    with st.spinner("Fetching news..."):
        news = get_news(rss_feeds)
        filtered = filter_news(news, source_filter, keyword_filter)
        if filtered:
            df = pd.DataFrame(filtered)
            st.dataframe(df)
        else:
            st.write("No news found matching your criteria.")
