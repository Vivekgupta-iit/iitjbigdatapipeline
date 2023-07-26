from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import  DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator

default_args = {
    'depends_on_past': False   
}

CLUSTER_NAME ='cluster-d863'
REGION='us-central1'
PROJECT_ID='black-anagram-380119'
PYSPARK_URI1= f"gs://iitj_bigdataproject_pgd_dev/Script/publication.py"





CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 30},
        
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 30},
    }
}


PYSPARK_JOB1 = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {"main_python_file_uri": PYSPARK_URI1},
}


with DAG(
    'iitjpgd22_publcation',
    default_args=default_args,
    description='A simple DAG to create a Dataproc workflow',
    schedule_interval=None,
    start_date = days_ago(2)
) as dag:

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=REGION,
        cluster_name=CLUSTER_NAME,
 
    )

    Ingesion1 = DataprocSubmitJobOperator(
        task_id="pub_load", 
        job=PYSPARK_JOB1, 
        region=REGION, 
        project_id=PROJECT_ID
    )
    

    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster", 
        project_id=PROJECT_ID, 
        cluster_name=CLUSTER_NAME, 
        region=REGION
    )

    create_cluster >> Ingesion1  >> delete_cluster