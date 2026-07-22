# Big Data Analytics Mini-Projects

This repository contains two independent mini-projects built with Apache Spark,
Kafka, and the Elastic Stack as part of a Big Data Analytics course
assignment. Each project lives in its own folder with its own `README.md`,
so it can be read, run, and reused on its own.

| Project | Folder | Summary |
|---|---|---|
| 🗞️ Real-Time News Entity Streaming Pipeline | [`news-entity-streaming-pipeline/`](./news-entity-streaming-pipeline) | Streams live headlines from NewsAPI through Kafka, extracts named entities in Spark Structured Streaming with spaCy, and indexes the results into Elasticsearch via Logstash for visualization in Kibana. |
| 🌐 Social Network Analysis with GraphFrames | [`graphframes-social-network-analysis/`](./graphframes-social-network-analysis) | Uses Spark GraphFrames on Databricks to analyze the Stanford SNAP `ego-Facebook` social graph — PageRank, connected components, triangle counting, and in/out-degree. |

## Repository structure

```
.
├── news-entity-streaming-pipeline/     # Project 1: Kafka + Spark Streaming + NER + ELK
├── graphframes-social-network-analysis/# Project 2: GraphFrames social network analysis
└── .gitignore
```

## Tech stack

- **Apache Spark** (Structured Streaming, GraphFrames)
- **Apache Kafka**
- **spaCy** (Named Entity Recognition)
- **NewsAPI**
- **Elasticsearch, Logstash, Kibana (ELK stack)**
- **Databricks** (notebook environment for the GraphFrames project)

## Getting started

Each project folder has its own setup and run instructions. Start with:

- [News streaming pipeline README](./news-entity-streaming-pipeline/README.md)
- [GraphFrames social network analysis README](./graphframes-social-network-analysis/README.md)

## Notes

- Large/derived artifacts (Spark Structured Streaming `checkpoint/` directories,
  `.crc` files, etc.) are intentionally excluded via `.gitignore` — they are
  runtime-generated and not part of the source.
- Any API keys or credentials referenced in the code are loaded from
  environment variables (see each project's `.env.example`). No real
  credentials are committed to this repository.
