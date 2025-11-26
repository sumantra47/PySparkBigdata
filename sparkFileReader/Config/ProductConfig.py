from pyspark.sql.types import StructType, StructField, StringType,LongType

#1464253347272,Facebook,add_to_cart,Visitor-548011,Page-6,Chemin Du Soleil
product_schema = StructType([
    StructField("product_id", LongType(), True),
    StructField("domain_name", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("visitor_id", StringType(), True),
    StructField("page_id", StringType(), True),
    StructField("product_name", StringType(), True)
])