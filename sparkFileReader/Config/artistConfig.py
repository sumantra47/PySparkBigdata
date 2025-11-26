from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

artist_schema = StructType([StructField('ConstituentID', StringType(), True), StructField('DisplayName', StringType(), True), StructField('ArtistBio', StringType(), True), StructField('Nationality', StringType(), True), StructField('Gender', StringType(), True), StructField('BeginDate', IntegerType(), True), StructField('EndDate', IntegerType(), True), StructField('Wiki QID', StringType(), True), StructField('ULAN', StringType(), True)])
