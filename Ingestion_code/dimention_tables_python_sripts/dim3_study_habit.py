from pyspark.sql import SparkSession

# create a SparkSession
spark = SparkSession.builder.appName("ReadCSV").getOrCreate()

# specify the file path of the CSV file
csv_file_path = "gs://asia-east2-iitprojectbigdat-60d4174c-bucket/data/Raw_src/student-mat.csv"

# define the schema for the selected columns
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
schema = StructType([
    StructField("Student_ID", StringType(), True),
    StructField("reason", StringType(), True),
    StructField("Guardian", StringType(), True),
    StructField("traveltime", StringType(), True),
    StructField("studytime", StringType(), True),
    StructField("failures", StringType(), True),
    StructField("schoolsup", StringType(), True),
    StructField("famsup", StringType(), True),
    StructField("paid", StringType(), True),
    StructField("activities", StringType(), True),
    StructField("nursery", StringType(), True),
    StructField("higher", StringType(), True),
    StructField("internet", StringType(), True)
])

# read the CSV file with selected columns and the defined schema
df1 = spark.read.csv(csv_file_path, schema=schema, header=True, usecols=["Student_ID", "reason", "Guardian", "traveltime", "studytime",
                 "failures", "schoolsup", "famsup", "paid", "activities", "nursery",
                 "higher", "internet"])


# write the selected column to a Parquet file
output_file_path = "gs://asia-east2-iitprojectbigdat-60d4174c-bucket/data/Landing/dim3_Study_habits.csv"
df1.write.csv(output_file_path)
