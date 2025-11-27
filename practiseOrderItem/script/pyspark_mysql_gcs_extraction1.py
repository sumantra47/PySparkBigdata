from pyspark.sql import SparkSession
import mysql.connector
import pandas as pd
from pyspark.sql.functions import to_date
import os

spark = SparkSession.builder.appName("pyspark-mysql-gcs-extraction1").getOrCreate()

def load_env(path):
    with open(path) as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

load_env("/etc/secrets.env")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

sql_qry="""
SELECT 
count(distinct order_id) as total_order,
sum(num_items) as total_order_item,
round(avg(num_items),1) as avg_items_per_order,
date(created_at) as order_date,
status
 FROM
  `practisedevdb`.`orders` 
 where date(created_at)>='2023-03-25'
  group by date(created_at), status
  order by date(created_at);
"""

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

def extractData(sql_qry,connection):
    return pd.read_sql(sql_qry,con=connection)

def convertPandastoSparkdf(pandas_df):
    return spark.createDataFrame(pandas_df)

def writeOutputSink(df,table_name,mode):
    df.write.mode(mode).parquet("gs://practise-dev-data/"+table_name+"/")

connection = connectMysql(username, password)
pd_order_status_summary = extractData(sql_qry,connection)
closeMysqlConnection(connection)
df_order_status_summary = convertPandastoSparkdf(pd_order_status_summary)
writeOutputSink(df_order_status_summary,"order_status_summary","overwrite")

