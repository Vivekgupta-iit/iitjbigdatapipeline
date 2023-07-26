from pyspark import SparkContext
from pyspark.sql import SparkSession
import csv


sc = SparkContext.getOrCreate()
spark = SparkSession(sc)

# Define the source file path and destination file path
src_path = "gs://iitj_bigdataproject_pgd_dev/Landing/student-mat.csv"
dest_path = "gs://iitj_bigdataproject_pgd_dev/Pub/student-mat.csv"

# Load the file as an RDD
file_rdd = sc.textFile(src_path)

# Split each line by comma
csv_rdd = file_rdd.map(lambda line: line.split(","))

# Write the RDD to a CSV file
with open(dest_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(csv_rdd.collect())
