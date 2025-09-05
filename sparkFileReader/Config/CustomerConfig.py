from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType

customer_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("email", StringType(), True),
    StructField("first", StringType(), True),
    StructField("last", StringType(), True),
    StructField("company", StringType(), True),
    StructField("created_at", TimestampType(), True),
    StructField("country", StringType(), True)
])
