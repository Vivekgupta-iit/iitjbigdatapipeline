from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("Joining CSV Files").getOrCreate()

# Define the schema
schema = "Student_ID INT, school VARCHAR(255), sex VARCHAR(255), age INT, address VARCHAR(255), famsize VARCHAR(255), Pstatus VARCHAR(10), Medu INT, Fedu INT, Mjob VARCHAR(30), Fjob VARCHAR(30), reason VARCHAR(30), guardian VARCHAR(30), traveltime INT, studytime INT, failures INT, schoolsup VARCHAR(10), famsup VARCHAR(10), paid VARCHAR(10), activities VARCHAR(10), nursery VARCHAR(10), higher VARCHAR(10), internet VARCHAR(10), romantic VARCHAR(10), famrel INT, freetime INT, goout INT, Dalc INT, Walc INT, health INT, absences INT, G1 INT, G2 INT, G3 INT"

# Load the CSV files
df1 = spark.read.csv("gs://iitj_bigdataproject_pgd_dev/Staging/fact_Student_Performance.csv/*.csv", header=True, inferSchema=True)
df2 = spark.read.csv("gs://iitj_bigdataproject_pgd_dev/Staging/dim1_Student_demographics.csv/*.csv", header=True, inferSchema=True)
df3 = spark.read.csv("gs://iitj_bigdataproject_pgd_dev/Staging/dim2_parental_info.csv/*.csv", header=True, inferSchema=True)
df4 = spark.read.csv("gs://iitj_bigdataproject_pgd_dev/Staging/dim3_study_habit.csv/*.csv", header=True, inferSchema=True)
df5 = spark.read.csv("gs://iitj_bigdataproject_pgd_dev/Staging/dim4_stu_lifestyle.csv/*.csv", header=True, inferSchema=True)

# Create temporary views for each dataframe
df1.createOrReplaceTempView("df1")
df2.createOrReplaceTempView("df2")
df3.createOrReplaceTempView("df3")
df4.createOrReplaceTempView("df4")
df5.createOrReplaceTempView("df5")
from pyspark.sql import SparkSession


# Join the dataframes on Student_ID column
df_joined = spark.sql("""
    SELECT 
        df1.Student_ID, 
        df2.school, 
        df2.sex, 
        df2.age, 
        df2.address, 
        df2.famsize, 
        df3.Pstatus, 
        df3.Medu, 
        df3.Fedu, 
        df3.Mjob, 
        df3.Fjob, 
        df4.reason, 
        df4.guardian, 
        df4.traveltime, 
        df4.studytime, 
        df4.failures, 
        df4.schoolsup, 
        df4.famsup, 
        df4.paid, 
        df4.activities, 
        df4.nursery, 
        df4.higher, 
        df4.internet, 
        df5.romantic, 
        df5.famrel, 
        df5.freetime, 
        df5.goout, 
        df5.Dalc, 
        df5.Walc, 
        df5.health, 
        df1.absences, 
        df1.G1, 
        df1.G2, 
        df1.G3
    FROM df1 
    FULL OUTER JOIN df2 ON df1.Student_ID = df2.Student_ID 
    FULL OUTER JOIN df3 ON df1.Student_ID = df3.Student_ID 
    FULL OUTER JOIN df4 ON df1.Student_ID = df4.Student_ID 
    FULL OUTER JOIN df5 ON df1.Student_ID = df5.Student_ID
""")


# Write the dataframe to a CSV file
df_joined.write.csv("gs://iitj_bigdataproject_pgd_dev/ODS/final_marks_stu_agg.csv", header=True)

