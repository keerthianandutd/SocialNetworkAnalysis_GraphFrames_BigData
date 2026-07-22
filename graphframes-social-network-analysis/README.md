# Social Network Analysis with GraphFrames

Graph analysis of a real social network using Spark GraphFrames 
on Databricks. The dataset is the Stanford SNAP **ego-Facebook** network, 
an undirected social graph of Facebook "friends lists" with 4,039 nodes.

- Dataset source: https://snap.stanford.edu/data/ego-Facebook.html

## What this notebook does

Using `data/facebook_combined.txt.gz` (edge list: `src dst` pairs) as input,
the notebook (`notebook/Analyzing Social Networks using GraphFrame.ipynb`)
builds a GraphFrame and computes:

- **PageRank** - the most "influential" nodes in the network
- **Connected components** - whether/how the graph is partitioned
- **Triangle count** - local clustering / community structure per node
- **In-degree / Out-degree** - most-connected nodes

| Metric | Top result (node id) |
|---|---|
| PageRank | `3437` (score approximatly 29.4) |
| Triangle count | `1912` (30,025 triangles) |
| In/Out-degree | `107` (1,045 connections) |
| Connected components | 1 component, 4,039 nodes (fully connected) |

## Running it

This notebook was built and run on **Databricks** (Databricks-flavored
notebook cells/metadata are still present in the `.ipynb` file).

1. Create a Databricks cluster.
2. Install the **GraphFrames** library on the cluster:
   - Go to **Compute** → select your cluster → **Libraries** tab.
   - Click **Install New** → **Maven** → **Search Packages** → choose
     **Spark Packages** → search for and select `graphframes`.
   - Click **Install**.
3. Upload `data/facebook_combined.txt.gz` to DBFS (e.g. `dbfs:/FileStore/tables/`).
4. Import and run `notebook/Analyzing Social Networks using GraphFrame.ipynb`,
   updating the input file path to match where you uploaded the dataset.

### Running locally instead (optional)

If you'd rather run this outside Databricks, you can use `pyspark` with the
GraphFrames package directly:

```bash
pyspark --packages graphframes:graphframes:0.8.3-spark3.5-s_2.12
```

Then adapt the notebook's file paths from `dbfs:/...` to a local/HDFS path
for `data/facebook_combined.txt.gz`.
