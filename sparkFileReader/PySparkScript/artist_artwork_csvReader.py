from pyspark.sql import SparkSession
from PySparkBigdata.sparkFileReader.Config.artistConfig import artist_schema
from PySparkBigdata.sparkFileReader.Config.artworkConfig import artwork_schema
import os, sys, argparse
from pyspark.sql.functions import col, regexp_replace, regexp_extract, concat_ws
python_path=sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['JAVA_HOME'] = r"C:\Users\Lenovo\.jdks\corretto-1.8.0_462"
#os.environ['HADOOP_HOME'] = r"C:\pyspark_install\hadoop3.0.0"
#os.environ['PATH'] = r"C:\pyspark_install\hadoop3.0.0\bin"
spark=SparkSession.builder \
    .appName("Spark Artist and Artwork CSV File Reader") \
    .config("spark.hadoop.fs.permissions.umask-mode", "000") \
    .master("local[*]") \
    .getOrCreate()
# Read Artist CSV file
parser = argparse.ArgumentParser(description='Artist and Artwork CSV File Reader')
parser.add_argument('--artist_csv_file_path', type=str, required=True, help='Path to the Artist CSV file')
parser.add_argument('--artwork_csv_file_path', type=str, required=True, help='Path to the Artwork CSV file')
args = parser.parse_args()
artist_csv_file_path = args.artist_csv_file_path
artwork_csv_file_path = args.artwork_csv_file_path
artistDF = spark.read.option("header", "true") \
    .schema(artist_schema) \
    .csv(artist_csv_file_path)
artistDF = artistDF.withColumn("gender",regexp_replace(col("gender"),r"[()\[\]{};:<>?\/\\|`~!@#$%^&*+=]", ""))
artistDF.show(5,truncate=False)
artistDF.printSchema()
artworkDF = spark.read.option("header", "true") \
    .schema(artwork_schema) \
    .csv(artwork_csv_file_path)
artworkDF.show(5,truncate=False)
artworkDF = artworkDF.withColumn("gender",regexp_replace(col("gender"),r"[()\[\]{};:<>?\/\\|`~!@#$%^&*+=]", ""))\
    .withColumn("Nationality",regexp_replace(col("Nationality"),r"[()\[\]{};:<>?\/\\|`~!@#$%^&*+=]", ""))\
    .withColumn("ArtistBio",concat_ws(" - ",regexp_extract(col("ArtistBio"), r"^([^,]+)", 1),regexp_extract(col("ArtistBio"), r",\s*(.*)", 1)))
artwork_new_DF = artworkDF.drop("URL","ImageURL","OnView")
artwork_new_DF.printSchema()
artwork_new_DF = artwork_new_DF.fillna({"BeginDate":9999,"EndDate":9999,"Date":9999,"Circumference (cm)":0.0,"Diameter (cm)":0.0,"Height (cm)":0.0,"Length (cm)":0.0,"Weight (kg)":0.0,"Seat Height (cm)":0.0})
artwork_new_DF = artwork_new_DF.withColumn("Dimensions",regexp_extract(col("Dimensions"),r"\(([^)]*)\)", 1))
artwork_new_DF.show(5,truncate=False)
artwork_new_DF.filter((col("Artist") == 'Otto Wagner') & (col("Title").contains('Stool'))).show(truncate=False)
artwork_new_DF.printSchema()
artwork_new_DF.createOrReplaceTempView("artwork_temp_view")
artistDF.createOrReplaceTempView("artist_temp_view")
# Join Artist and Artwork DataFrames
joinedDF = spark.sql("""
select a.ConstituentID, a.ArtistBio, a.Nationality,
    b.Title, b.Date, b.Medium, b.Dimensions from artist_temp_view a
    join artwork_temp_view b
    on a.ConstituentID = b.ConstituentID
""")
joinedDF.show(5,truncate=False)
joinedDF.printSchema()
# joinedDF.write.mode("overwrite").option("header","true")\
#    .csv(r"sparkFileReader\OutputResource\artist_artwork_output")
spark.stop()