# Big Data Analytics Mini-Projects

This repository contains two independent mini-projects built with Apache Spark,
Kafka, and the Elastic Stack as part of a Big Data Analytics course
assignment. Each project lives in its own folder with its own `README.md`,
so it can be read, run, and reused on its own.

| Folder | Summary |
|---|---|
| [`news-entity-streaming-pipeline/`](./news-entity-streaming-pipeline) | Streams live headlines from NewsAPI through Kafka, extracts named entities in Spark Structured Streaming with spaCy, and indexes the results into Elasticsearch via Logstash for visualization in Kibana. |
| [`graphframes-social-network-analysis/`](./graphframes-social-network-analysis) | Uses Spark GraphFrames on Databricks to analyze the Stanford SNAP `ego-Facebook` social graph — PageRank, connected components, triangle counting, and in/out-degree. |

## Tech stack

- **Apache Spark** (Structured Streaming, GraphFrames)
- **Apache Kafka**
- **spaCy** (Named Entity Recognition)
- **NewsAPI**
- **Elasticsearch, Logstash, Kibana (ELK stack)**
- **Databricks** (notebook environment for the GraphFrames project)