from pyspark.sql import SparkSession
from sparkFileReader.Config.CustomerConfig import customer_schema
import os,sys,argparse


os.environ['PYSPARK_PYTHON'] = python_path
os.environ['JAVA_HOME'] = r"C:\Users\Lenovo\.jdks\corretto-1.8.0_462"

spark=SparkSession.builder \
    .appName("Spark Json File Reader") \
    .master("local[*]") \
    .getOrCreate()

# Read JSON file with predefined schema
parser = argparse.ArgumentParser(description='Json File Reader')
parser.add_argument('--json_file_path', type=str, required=True, help='Path to the JSON file')
args = parser.parse_args()
json_file_path = args.json_file_path
python_path=sys.executable
#json_file_path="D:/gcp_de_all/udemy_de_master_course/spark/spark_project_practise/PySparkBigdata/sparkFileReader/DataResource/customers.json"
df = spark.read.schema(customer_schema) \
    .option("multiline", "true") \
    .json(json_file_path)
df.show(truncate=False)
df.printSchema()
spark.stop()