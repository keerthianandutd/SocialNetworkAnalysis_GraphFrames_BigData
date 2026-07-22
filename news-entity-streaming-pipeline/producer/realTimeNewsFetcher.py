import os
from newsapi import NewsApiClient
from kafka import KafkaProducer
import json
import time

# Setup NewsAPI
# Get a free API key from https://newsapi.org/ and set it as an environment
# variable instead of hard-coding it here.
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    raise RuntimeError("Please set the NEWSAPI_KEY environment variable")

newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    top_headlines = newsapi.get_top_headlines(language='en', page_size=10)

    for article in top_headlines['articles']:
        if article['title']:
            news_text = article['title']
            producer.send("datafetchtopic", {"text": news_text})
            print(f"[Sent to Kafka]: {news_text}")

    time.sleep(60)
