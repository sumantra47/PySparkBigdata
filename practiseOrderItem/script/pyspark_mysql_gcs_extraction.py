from pyspark.sql import SparkSession
import mysql.connector
import pandas as pd
from pyspark.sql.functions import to_date
import os

spark = SparkSession.builder.appName("pyspark-mysql-gcs-extraction").getOrCreate()

def load_env(path):
    with open(path) as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

load_env("/etc/secrets.env")

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

def connectMysql(username,password):
    connection = mysql.connector.connect(
        user=username,
        password=password,
        database='practisedevdb',
        host='10.1.128.3',
        port='3306'
    )
    return connection
def closeMysqlConnection(connection):
    connection.close()

qry_order= "select * from orders;"
qry_order_item= "select * from order_items;"

#extract data from mysql to pandas dataframe
def extractData(sql_qry,connection):
    return pd.read_sql(sql_qry,con=connection)
#convert pandas dataframe to spark dataframe
def convertPandastoSparkdf(pandas_df):
    return spark.createDataFrame(pandas_df)
#date transformation to add partition column
def dt_transformation(df):
    return df.withColumn("date",to_date(df.created_at)),'date'
#write spark dataframe to gcs in parquet format partitioned by date
def writeOutputSink(df,partition_column,table_name,mode):
    df.write.partitionBy(partition_column).mode(mode).parquet("gs://practise-dev-data/"+table_name+"/")

connection = connectMysql(username, password)
pd_orders = extractData(qry_order,connection)
pd_order_items = extractData(qry_order_item,connection)
closeMysqlConnection(connection)
df_orders = convertPandastoSparkdf(pd_orders)
df_order_items = convertPandastoSparkdf(pd_order_items)
df_orders,part_col1 = dt_transformation(df_orders)
df_order_items,part_col2 = dt_transformation(df_order_items)
writeOutputSink(df_orders,part_col1,"orders","overwrite")
writeOutputSink(df_order_items,part_col2,"order_items","overwrite")

