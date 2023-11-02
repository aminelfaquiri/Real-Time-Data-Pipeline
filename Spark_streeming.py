import findspark
findspark.init()

import pymongo
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json, to_json, col, concat_ws,explode,concat, lit,date_format, current_date, datediff,floor
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, ArrayType, TimestampType, MapType
import uuid

# ______________________________________

spark = SparkSession.builder \
    .appName("kafka_spark_streeming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,"
            "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,"
            "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0") \
    .getOrCreate()

# ______________________________________

# Read data from Kafka topic:
kafka_data = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "messages") \
    .load()

# Specify the value deserializer
kafka_data = kafka_data.selectExpr("CAST(value AS STRING)")

# Define a schema with fields at the same level as the JSON
schema = StructType([
    StructField("gender", StringType(), True),
    StructField("name", StructType([
        StructField("title", StringType(), True),
        StructField("first", StringType(), True),
        StructField("last", StringType(), True)
    ]), True),
    StructField("location", StructType([
            StructField("street", StructType([
                StructField("number", IntegerType(), True),
                StructField("name", StringType(), True)
            ]), True),
            StructField("city", StringType(), True),
            StructField("state", StringType(), True),
            StructField("country", StringType(), True),
            StructField("postcode", IntegerType(), True),
            StructField("timezone", StructType([
                StructField("offset", StringType(), True),
                StructField("description", StringType(), True)
            ]), True)
        ]), True),
    StructField("email", StringType(), True),
    StructField("dob", StructType([
        StructField("date", TimestampType(), True),
        StructField("age", IntegerType(), True)
    ]), True),
    StructField("registered", StructType([
        StructField("date", TimestampType(), True),
        StructField("age", IntegerType(), True)
    ]), True),
    StructField("nat", StringType(), True)
])

parsed_data = kafka_data.select(from_json(kafka_data.value, schema).alias("data")).select("data.*")

# select the columns needed :
selected_data = parsed_data.select(
    lit(str(uuid.uuid4())).alias("id"),
    col("gender"),
    concat(col("name.first"), lit(" "), col("name.last")).alias("full_name"),
    concat_ws(" ", 
        col("location.street.number"),
        col("location.street.name"),
        col("location.city"),
        col("location.state"),
        col("location.country"),
        col("location.postcode")
    ).alias("full_address"),
    (substring_index(col("email"), "@", -1)).alias("domain_email"),
    date_format(col("dob.date"), "yyyy-MM-dd").alias("birthday"),
    floor(datediff(current_date(), col("dob.date")) / 365).alias("age"), # Calculate the age in years
    date_format(col("registered.date"), "yyyy-MM-dd").alias("registered_date"),
    col("nat").alias("nationality")
)

# ______________________________ casandra _______________________________

# Define your Cassandra keyspace and table
cassandra_keyspace = "user"
cassandra_table = "user_informations"

# create a Cassandra connection :
try:
    # provide contact points
    cluster = Cluster(["localhost"])
    session = cluster.connect()
    print("__________________ Connection successfull ____________________.")

except:
    print("__________________ Connection failed __________________________.")


# create Keyspace "user" :
try:
    create_keyspace_query = " CREATE KEYSPACE IF NOT EXISTS "+cassandra_keyspace+ \
    " WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}"
    session.execute(create_keyspace_query)
    print("_______________________ Keyspace was created successfully ________________________________")
except:
    print(f"Error in creating keyspace {cassandra_keyspace}.")

# Create table :
try:
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {cassandra_keyspace}.{cassandra_table} (
        id UUID PRIMARY KEY,
        gender TEXT,
        full_name TEXT,
        full_address TEXT,
        domain_email TEXT,
        birthday TEXT,
        age TEXT,
        registered_date TEXT,
        nationality TEXT
    )
    """

    session.execute(create_table_query)
    print("_______________________ table was created successfully. _________________________________")
except Exception as e:
    print(f"__________________ Error in creating keyspace {cassandra_table}: {str(e)} ______________")

# insert into keyspace :
selected_data.writeStream \
    .outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("checkpointLocation", "./checkpoint/data") \
    .option("keyspace", cassandra_keyspace) \
    .option("table", cassandra_table) \
    .start()

print("_____________________ Casandra insert into keyspace Successfully ______________________________")

#______________________________________________ MongoDB _______________________________________________#

mongo_uri = "mongodb://localhost:27017/"
mongo_db_name = "user"
collection_name = "user_informations"


selected_data_mongo = selected_data.drop("id")

selected_data_mongo.writeStream \
    .foreachBatch(lambda batchDF, batchId:
        batchDF.write \
        .format("mongo") \
        .option("uri", mongo_uri) \
        .option("database", mongo_db_name) \
        .option("collection", collection_name) \
        .mode("append") \
        .save()

    ) \
    .outputMode("append") \
    .start()


print("__________________________ MongoDb Is Successfully ________________________________")

selected_data.writeStream.outputMode("append").format("console").start().awaitTermination()