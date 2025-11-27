from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from datetime import datetime

PROJECT_ID = "practise-dev"
REGION = "us-central1"
CLUSTER_NAME = "practise-spark-streaming"

PYTHON_FILE = "gs://practise-dev-data/pubSubTopicPublishTimestamp.py"

with DAG(
        "dataproc_run_gcs_to_pubsub_timestamp",
        start_date=datetime(2024, 1, 1),
        schedule_interval=None,
        catchup=False,
) as dag:

    run_python_job = DataprocSubmitJobOperator(
        task_id="run_python_job",
        project_id=PROJECT_ID,
        region=REGION,
        job={
            "placement": {
                "cluster_name": CLUSTER_NAME
            },
            "pyspark_job": {
                "main_python_file_uri": PYTHON_FILE
            }
        },
    )

    run_python_job