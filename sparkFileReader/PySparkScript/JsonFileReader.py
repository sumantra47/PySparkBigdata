from pyspark.sql import SparkSession
from sparkFileReader.Config.CustomerConfig import customer_schema
import os,sys


python_path=sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['JAVA_HOME'] = r"C:\Users\Lenovo\.jdks\corretto-1.8.0_462"

spark=SparkSession.builder \
    .appName("Spark Json File Reader") \
    .master("local[*]") \
    .getOrCreate()

json_file_path="D:/gcp_de_all/udemy_de_master_course/spark/spark_project_practise/PySparkBigdata/sparkFileReader/DataResource/customers.json"
df = spark.read.schema(customer_schema) \
    .option("multiline", "true") \
    .json(json_file_path)
df.show(truncate=False)
df.printSchema()
spark.stop()