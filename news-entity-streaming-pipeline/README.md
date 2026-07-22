# Real-Time News Entity Streaming Pipeline

A real-time pipeline that fetches live news headlines, extracts named
entities (people, organizations, locations) from them, and indexes the
running entity counts into Elasticsearch for visualization in Kibana.

## Architecture

```
NewsAPI --> [producer/realTimeNewsFetcher.py] --> Kafka topic "datafetchtopic"
                                                          |
                                                          v
                                    [streaming/streamingApp.py] (Spark Structured Streaming + spaCy NER)
                                                          |
                                                          v
                                          Kafka topic "namedentitytopic"
                                                          |
                                                          v
                                         [logstash/logstash.conf] --> Elasticsearch --> Kibana
```

1. **`producer/realTimeNewsFetcher.py`** polls the NewsAPI top-headlines
   endpoint every 60 seconds and publishes each headline to the Kafka topic
   `datafetchtopic`.
2. **`streaming/streamingApp.py`** is a Spark Structured Streaming job that
   reads from `datafetchtopic`, runs spaCy Named Entity Recognition on each
   headline, aggregates entity counts, and writes the results out (to the
   console by default; a commented-out block shows how to publish to the
   Kafka topic `namedentitytopic` instead).
3. **`logstash/logstash.conf`** ships the entity-count events from Kafka into
   Elasticsearch, where they can be explored/visualized in Kibana.

## Prerequisites

- Java 8/11 (required by Kafka and Spark)
- Apache Kafka (tested with 2.13-4.0.0)
- Apache Spark with `spark-submit` on your `PATH`
- Python 3.9+

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3. Configure secrets
cp .env.example .env
# edit .env and fill in NEWSAPI_KEY and ELASTIC_PASSWORD
export $(grep -v '^#' .env | xargs)   # load them into your shell (macOS/Linux)
```

> **Never commit your real `.env` file or API keys.** Only `.env.example`
> (with placeholder values) is tracked in this repo.

## Running the pipeline

**1. Start Kafka** (in its own terminal):
```bash
bin/kafka-server-start.sh config/server.properties
```

**2. Create the two Kafka topics:**
```bash
bin/kafka-topics.sh --create --topic datafetchtopic  --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic namedentitytopic --bootstrap-server localhost:9092
```

**3. Start the news producer:**
```bash
python producer/realTimeNewsFetcher.py
```

**4. Start the Spark Structured Streaming job:**
```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  streaming/streamingApp.py \
  localhost:9092 subscribe datafetchtopic namedentitytopic
```

**5. Start Elasticsearch and Kibana**, then start Logstash to ship data into
Elasticsearch:
```bash
logstash -f logstash/logstash.conf
```

Open Kibana at `http://localhost:5601` to explore the indexed entity counts.

## Configuration

All secrets are read from environment variables — nothing is hard-coded:

| Variable | Used in | Purpose |
|---|---|---|
| `NEWSAPI_KEY` | `producer/realTimeNewsFetcher.py` | Auth for the NewsAPI client |
| `ELASTIC_PASSWORD` | `logstash/logstash.conf` | Auth for the `elastic` Elasticsearch user |
