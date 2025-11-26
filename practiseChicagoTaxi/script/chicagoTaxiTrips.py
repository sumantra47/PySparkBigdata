from pyspark.sql import SparkSession
import os, sys, argparse
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType, FloatType
from pyspark.sql.functions import year,month,day
from pyspark.sql import functions as F
python_path=sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['JAVA_HOME'] = r"C:\Users\Lenovo\.jdks\corretto-1.8.0_462"


spark =SparkSession.builder\
    .appName("Chicago Taxi Trips Analysis") \
    .config("spark.hadoop.fs.permissions.umask-mode", "000") \
    .master("local[*]") \
    .getOrCreate()

#save data to bigquery
def save_data_to_bq(df,bq_table):
    df.write.format("bigquery") \
        .option("table", bq_table) \
        .option("temporaryGcsBucket", "practise-dev-data") \
        .mode("overwrite") \
        .save()

# Data Cleaning and Transformation
def data_transformation(df,bq_table):
    df = df.withColumn("trip_month", F.month(F.col("trip_start_time")))
    df= df.withColumn("trip_duration_seconds",F.col("trip_end_time").cast("long") - F.col("trip_start_time").cast("long")) \
        .withColumn("trip_duration_minutes",F.col("trip_duration_seconds")/60)
    max_fare_cc = df_taxi.filter(F.col("payment_type") == "Credit Card") \
            .agg(F.max("fare").alias("max_fare")) \
            .collect()
    print(f"Max fare : {max_fare_cc[0]['max_fare']} for Credit Card payment type")
    df_subset = df.select("payment_type","fare")
    df_subset.select(F.col("payment_type")).distinct().show()
    df.select(F.col("trip_month")).distinct().show()

    df_grouped = df_subset.groupBy("payment_type")\
        .agg(F.max("fare").alias("max_fare"),
         F.min("fare").alias("min_fare"),
         F.avg("fare").alias("avg_fare"),
         F.count("fare").alias("total_trips"))\
        .orderBy(F.desc("total_trips"))

    df_grouped.show(truncate=False)

    df_taxi_trip = df.groupBy("payment_type","trip_month")\
        .agg(F.sum("fare").alias("trip_fare"),
            F.sum("trip_miles").alias("trip_miles"),
            F.avg("fare").alias("avg_fare"))\
        .orderBy("payment_type","trip_month")

    df_taxi_trip.show(truncate=False)
    df.show(5,truncate=False)

    save_data_to_bq(df_taxi_trip,bq_table)
# Read input CSV file
file_path = r"gs://practise-dev-data/chicago_taxi_trips.csv"
df_taxi = spark.read.csv(file_path,header=True,inferSchema=True)
df_taxi.show(5,truncate=False)
df_taxi.printSchema()
bq_table = "practise-dev.chicago_taxi_raw.taxi_trips"
#save raw data to bigquery table
data_transformation(df_taxi,bq_table)
spark.stop()

