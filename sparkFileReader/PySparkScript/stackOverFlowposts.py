from pyspark.sql import SparkSession
import os, sys, argparse
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType, FloatType
from pyspark.sql.functions import year,month,day
python_path=sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['JAVA_HOME'] = r"C:\Users\Lenovo\.jdks\corretto-1.8.0_462"
spark=SparkSession.builder \
    .appName("Udemy Spark Practise") \
    .config("spark.hadoop.fs.permissions.umask-mode", "000") \
    .master("local[*]") \
    .getOrCreate()
# Read input CSV file
df= spark.read.csv(r"D:\gcp_de_all\udemy_de_master_course\spark\spark_project_practise\PySparkBigdata\sparkFileReader\DataResource\stackoverflowposts.csv",header=True,inferSchema=True)
df.show(5,truncate=False)
df.printSchema()

# Data Cleaning and Transformation
df_subset = df.select("id", "tags", "creation_date", "score", "view_count")
df_subset = df_subset.withColumn("id",df_subset["Id"].cast(IntegerType()))
df_subset = df_subset.withColumn("creation_date",df_subset["creation_date"].cast(TimestampType()))
df_subset = df_subset.withColumn("score",df_subset["Score"].cast(IntegerType()))
df_subset = df_subset.withColumn("view_count",df["view_count"].cast(IntegerType()))

df_subset.printSchema()

df_subset = df_subset.withColumn("creation_year",year(df_subset['creation_date']))
df_subset = df_subset.withColumn("creation_month",month(df_subset['creation_date']))
df_subset.show(5,truncate=False)

from pyspark.sql import functions as F
df_subset = df_subset.withColumn("post_type" , F.when(F.col("tags").like("%python%"), "Python") \
    .when(F.col("tags").like("%mysql%"), "mysql") \
    .when(F.col("tags").like("%scala%"), "scala") \
                                 .otherwise("other"))

df_subset.filter(F.col("post_type") == "Python").show(5,truncate=False)

df_tagged = df_subset.filter((F.col("post_type") == "Python") | (F.col("post_type") == "mysql"))

df_tagged = df_tagged.groupBy("post_type") \
    .agg(F.count("id").alias("total_posts"),
         F.sum("score").alias("total_score"),
         F.avg("view_count").alias("avg_view_count")) \
    .orderBy(F.desc("total_posts"))

df_tagged.show(truncate=False)