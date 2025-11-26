from pyspark.sql import SparkSession
import os, sys, argparse
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType, FloatType
from pyspark.sql.functions import year,month,day
python_path=sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['JAVA_HOME'] = r"C:\Users\Lenovo\.jdks\corretto-1.8.0_462"


spark =SparkSession.builder\
    .appName("Chicago Taxi Trips Analysis") \
    .config("spark.hadoop.fs.permissions.umask-mode", "000") \
    .master("local[*]") \
    .getOrCreate()

# Read input CSV file
df_taxi = spark.read.csv(r"D:\gcp_de_all\udemy_de_master_course\spark\spark_project_practise\PySparkBigdata\sparkFileReader\DataResource\chicago_taxi_trips.csv",header=True,inferSchema=True)
df_taxi.show(5,truncate=False)
df_taxi.printSchema()
# Data Cleaning and Transformation
from pyspark.sql import functions as F
from pyspark.sql.functions import month
max_fare_cc = df_taxi.filter(F.col("payment_type") == "Credit Card") \
    .agg(F.max("fare").alias("max_fare")) \
    .collect()
print(max_fare_cc[0]["max_fare"])
df_taxi = df_taxi.withColumn("trip_month", F.month(F.col("trip_start_time")))
df_taxi.show(5, truncate=False)

df_taxi_subset = df_taxi.select("payment_type","fare")
df_taxi_subset.select(F.col("payment_type")).distinct().show()
df_taxi.select(F.col("trip_month")).distinct().show()

df_taxi_grouped = df_taxi_subset.groupBy("payment_type")\
    .agg(F.max("fare").alias("max_fare"),
         F.min("fare").alias("min_fare"),
         F.avg("fare").alias("avg_fare"),
         F.count("fare").alias("total_trips"))\
    .orderBy(F.desc("total_trips"))

df_taxi_grouped.show(truncate=False)

df_taxi_trip = df_taxi.groupBy("payment_type","trip_month")\
    .agg(F.sum("fare").alias("trip_fare"),
         F.sum("trip_miles").alias("trip_miles"),
         F.avg("fare").alias("avg_fare"))\
    .orderBy("payment_type","trip_month")

df_taxi_trip.show(truncate=False)

df_taxi = df_taxi.withColumn("trip_duration_seconds",F.col("trip_end_time").cast("long") - F.col("trip_start_time").cast("long")) \
    .withColumn("trip_duration_minutes",F.col("trip_duration_seconds")/60)
df_taxi.show(5,truncate=False)

