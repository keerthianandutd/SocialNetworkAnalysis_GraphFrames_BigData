import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, explode, from_json, col, to_json, struct
from pyspark.sql.types import ArrayType, StringType, StructType
import spacy

# Reading command line arguments
kafka_bootstrap_servers = sys.argv[1]   # Example: "localhost:9092"
subscribe_type = sys.argv[2]             # Example: "subscribe"
input_topic = sys.argv[3]                # Example: "datafetchtopic"
output_topic = sys.argv[4]               # Example: "namedentitytopic"

# Loading SpaCy Model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    if text is not None:
        doc = nlp(text)
        return [ent.text for ent in doc.ents]
    else:
        return []

# Starting Spark Session
spark = SparkSession.builder \
    .appName("NERStreamingApp") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


# Reading Stream from Kafka (topic1)

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option(subscribe_type, input_topic) \
    .option("failOnDataLoss", "false") \
    .load()

# Converting value from binary to string
news_df = df.selectExpr("CAST(value AS STRING)")


# Parsing JSON incoming data
schema = StructType().add("text", StringType())

parsed_df = news_df.select(from_json(col("value"), schema).alias("data")).select("data.text")

# Named Entity Recognition UDF
entity_udf = udf(extract_entities, ArrayType(StringType()))

entities_df = parsed_df.withColumn("entities", entity_udf(col("text")))

exploded_df = entities_df.select(explode(col("entities")).alias("entity"))

entity_counts = exploded_df.groupBy("entity").count()


# Output for Kafka (topic2)
final_output_df = entity_counts.select(
    to_json(struct(col("entity"), col("count"))).alias("value")
)

final_output_df.printSchema()


#  Writing Stream to Kafka (topic2)

# query = final_output_df.writeStream \
#     .format("kafka") \
#     .outputMode("update") \
#     .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
#     .option("topic", output_topic) \
#     .option("checkpointLocation", "./checkpoint") \
#     .start()

# Printing output in console
query = final_output_df.writeStream\
    .outputMode('update')\
    .option("truncate", "false")\
    .format('console')\
    .start()

query.awaitTermination()
