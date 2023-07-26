from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType
# Create a SparkSession
spark = SparkSession.builder.appName("ReadWriteData").getOrCreate()

# Set the GCP storage paths for source and destination
source_path = "gs://iitj_bigdataproject_pgd_dev/Landing/student-mat.csv"
dest_path = "gs://iitj_bigdataproject_pgd_dev/Staging/dim3_study_habit.csv"

# Define the schema for the data
schema = StructType([
    StructField("Student_ID", IntegerType(), True),
    StructField("reason", StringType(), True),
    StructField("guardian", StringType(), True),
    StructField("traveltime", IntegerType(), True),
    StructField("studytime", IntegerType(), True),
    StructField("failures", IntegerType(), True),
    StructField("schoolsup", StringType(), True),
    StructField("famsup", StringType(), True),
    StructField("Paid", BooleanType(), True),
    StructField("activities", BooleanType(), True),
    StructField("higher", BooleanType(), True),
    StructField("internet", BooleanType(), True)
])
 
# Read only the specified columns from the source file
df = spark.read \
  .option("header", "true") \
  .option("inferSchema", "false") \
  .option("delimiter", ",") \
  .option("nullValue", "") \
  .option("quote", "\"") \
  .option("escape", "\"") \
  .schema(schema) \
  .csv(source_path) \
  .select("Student_ID", "reason", "guardian", "traveltime", "studytime", "failures", "schoolsup", "famsup", "Paid", "activities", "higher", "internet")

# Write the data to the destination path in GCP storage
df.write \
  .mode("overwrite") \
  .option("header", "true") \
  .option("delimiter", ",") \
  .option("quote", "\"") \
  .option("escape", "\"") \
  .csv(dest_path)




