from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Create a SparkSession
spark = SparkSession.builder.appName("Ingestion Job").getOrCreate()

# Define the schema of the data
schema = StructType([
    StructField("Student_ID", IntegerType(), True),
    StructField("G1", IntegerType(), True),
    StructField("G2", IntegerType(), True),
    StructField("G3", IntegerType(), True),
    StructField("absences", IntegerType(), True)
])

# Read the source data file
source_file_path = "gs://iitj_bigdataproject_pgd_dev/Landing/student-mat.csv"
source_data = spark.read.csv(source_file_path, header=True, schema=schema)

# Select the required columns
required_cols = ["Student_ID", "G1", "G2", "G3", "absences"]
selected_data = source_data.select(*required_cols)

# Write the selected data to the target location
target_file_path = "gs://iitj_bigdataproject_pgd_dev/Staging/fact_Student_Performance.csv"
selected_data.write.csv(target_file_path, header=True, mode="overwrite")

# Stop the SparkSession
spark.stop()

