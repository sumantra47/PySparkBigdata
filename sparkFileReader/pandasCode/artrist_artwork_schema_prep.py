import pandas as pd
import json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType



#print(df.groupby('Table').count())
def get_datatype(field,description):
    field_name_lower = field.lower()
    if "id" in field_name_lower or "number" in field_name_lower:
        return "string"
    elif "date" in field_name_lower:
        return "integer" if "year" in description.lower() else "string"
    elif any(x in field_name_lower for x in ["height", "width", "weight", "length", "diameter", "circumference", "duration"]):
        return "float"
    else:
        return "string"


def extract_schema(dataframe):
    global json_output, table, group, fields, index, row, field
    json_output = []
    for table, group in df.groupby('Table'):
        fields = []
        #print(group.iterrows())
        for index, row in group.iterrows():
            #print(row)
            field = {
                "field": row['Field'],
                "datatype": get_datatype(row['Field'], row['Description']),
                "description": row['Description']
            }
            fields.append(field)

        json_output.append({
            "table": table,
            "fields": fields
        })
    return json_output

df= pd.read_csv(r"D:\gcp_de_all\udemy_de_master_course\spark\spark_project_practise\PySparkBigdata\sparkFileReader\DataResource\MoMA_data_dictionary.csv")
json_output=extract_schema(df)
#print(json_output)

with open(r"D:\gcp_de_all\udemy_de_master_course\spark\spark_project_practise\PySparkBigdata\sparkFileReader\DataResource\moma_artists_artworks_schema.json","w") as f:
    json.dump(json_output,f,indent=4)

#Create artist and artwork schema

def create_artist_artwork_schema(json_file_path):
    with open(json_file_path, 'r') as f:
        schema_data = json.load(f)

    artist_schema = StructType()
    artwork_schema = StructType()

    for table_info in schema_data:
        table_name = table_info['table']
        fields = table_info['fields']

        if table_name == 'Artists':
            for field in fields:
                field_name = field['field']
                datatype = field['datatype']
                if datatype == 'string':
                    artist_schema.add(StructField(field_name, StringType(), True))
                elif datatype == 'integer':
                    artist_schema.add(StructField(field_name, IntegerType(), True))
                elif datatype == 'float':
                    artist_schema.add(StructField(field_name, FloatType(), True))

        elif table_name == 'Artworks':
            for field in fields:
                field_name = field['field']
                datatype = field['datatype']
                if datatype == 'string':
                    artwork_schema.add(StructField(field_name, StringType(), True))
                elif datatype == 'integer':
                    artwork_schema.add(StructField(field_name, IntegerType(), True))
                elif datatype == 'float':
                    artwork_schema.add(StructField(field_name, FloatType(), True))

    return artist_schema, artwork_schema

artist_schema, artwork_schema = create_artist_artwork_schema(r"D:\gcp_de_all\udemy_de_master_course\spark\spark_project_practise\PySparkBigdata\sparkFileReader\DataResource\moma_artists_artworks_schema.json")

print("Artist Schema:")
print(artist_schema)
print("\nArtwork Schema:")
print(artwork_schema)

# Save the schemas to files if needed
with open(r"D:\gcp_de_all\udemy_de_master_course\spark\spark_project_practise\PySparkBigdata\sparkFileReader\Config\artistConfig.py",'w') as f:
    f.write("from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType\n\n")
    f.write("artist_schema = " + repr(artist_schema) + "\n")
with open(r"D:\gcp_de_all\udemy_de_master_course\spark\spark_project_practise\PySparkBigdata\sparkFileReader\Config\artworkConfig.py",'w') as f:
    f.write("from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType\n\n")
    f.write("artwork_schema = " + repr(artwork_schema) + "\n")


