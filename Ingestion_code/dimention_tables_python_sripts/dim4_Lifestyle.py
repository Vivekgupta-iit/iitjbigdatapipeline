from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# create SparkSession
spark = SparkSession.builder.appName("IngestionJob").getOrCreate()

# define schema for selected columns
schema = StructType([
    StructField("Student ID", IntegerType(), True),
    StructField("romantic", StringType(), True),
    StructField("famrel", IntegerType(), True),
    StructField("freetime", IntegerType(), True),
    StructField("goout", IntegerType(), True),
    StructField("Dalc", IntegerType(), True),
    StructField("Walc", IntegerType(), True),
    StructField("health", IntegerType(), True)
])

# read source file into DataFrame
source_df = spark.read.option("header", True).schema(schema).csv("gs://iitj_bigdataproject_pgd_dev/Landing/student-mat.csv")

# select desired columns
selected_df = source_df.select("Student ID", "romantic", "famrel", "freetime", "goout", "Dalc", "Walc", "health")

# write selected columns to target file in GCP storage
selected_df.write.mode("overwrite").option("header", True).csv("gs://iitj_bigdataproject_pgd_dev/Staging/dim4_stu_lifestyle.csv")


