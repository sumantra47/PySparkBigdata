from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

spark=SparkSession.builder \
    .appName("BookXmlFileReader") \
    .master("local[2]") \
    .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.16.0") \
    .getOrCreate()

df=spark.read \
    .format("com.databricks.spark.xml") \
    .option("rootTag","catalog") \
    .option("rowTag","book") \
    .load("file:///D:/gcp_de_all/udemy_de_master_course/spark/spark_project_practise/PySparkBigdata/sparkFileReader/DataResource/books.xml")

df.printSchema()
df.show(5,truncate=False)

df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("file:///D:/gcp_de_all/udemy_de_master_course/spark/spark_project_practise/PySparkBigdata/sparkFileReader/OutputResource/books.xml")
spark.stop()