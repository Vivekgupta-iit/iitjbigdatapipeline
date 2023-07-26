from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("ReadWriteData").getOrCreate()

# Set the GCP storage paths for source and destination
source_path = "gs://iitj_bigdataproject_pgd_dev/Landing/student-mat.csv"
dest_path = "gs://iitj_bigdataproject_pgd_dev/Staging/dim2_parental_info.csv"

# Define the schema for the data
schema = "Student_ID INT, Pstatus STRING, Medu INT, Fedu INT, Mjob STRING, Fjob STRING"

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
  .select("Student_ID", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob")

# Write the data to the destination path in GCP storage
df.write \
  .mode("overwrite") \
  .option("header", "true") \
  .option("delimiter", ",") \
  .option("quote", "\"") \
  .option("escape", "\"") \
  .csv(dest_path)

  