from pyspark.sql import SparkSession
from PySparkBigdata.sparkFileReader.Config.ProductConfig import product_schema
from pyspark.sql.functions import col,split,current_date,date_format

import os, sys, argparse
python_path=sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['JAVA_HOME'] = r"C:\Users\Lenovo\.jdks\corretto-1.8.0_462"
spark=SparkSession.builder \
    .appName("Spark CSV File Reader") \
    .master("local[*]") \
    .getOrCreate()
# Read CSV file
parser = argparse.ArgumentParser(description='CSV File Reader')
parser.add_argument('--csv_file_path', type=str, required=True, help='Path to the CSV file')
args = parser.parse_args()
csv_file_path = args.csv_file_path

csvDF = spark.read.option("header", "true") \
    .schema(product_schema) \
    .csv(csv_file_path) \
    #.option("inferSchema", "true") \

csvDF.show(truncate=False)
#csvDF =csvDF.withColumn("product_id", col("product_id").cast("integer"))
csv_df_new = csvDF.withColumn("visitor_id_no", split(col("visitor_id"),"-").getItem(1))
csvDF.printSchema()
df_new = csvDF.filter(csvDF.event_type == 'add_to_cart').select("product_id", "event_type", "product_name")
df_new = df_new.withColumn("report_dt", date_format(current_date(), "yyyy/MM/dd"))
df_new.show(truncate=False)
csv_df_new.show(truncate=False)
spark.stop()