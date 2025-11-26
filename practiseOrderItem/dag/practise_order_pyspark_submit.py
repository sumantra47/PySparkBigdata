# python
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import logging

DEFAULT_PROJECT = os.environ.get("GCP_PROJECT", "PROJECT_ID")
DEFAULT_REGION = "us-central1"
DEFAULT_CLUSTER = os.environ.get("DP_CLUSTER_NAME", "practise-orders-cluster")

default_args = {"owner": "airflow", "depends_on_past": False}

with DAG(
        dag_id="practise_order_pyspark_submit",
        default_args=default_args,
        description="practise_order_cluster",
        schedule_interval=None,
        start_date=days_ago(1),
        catchup=False,
        tags=["dataproc", "order"],
) as dag:

    submit_pyspark_job = DataprocSubmitJobOperator(
    task_id="submit_pyspark_job",
    region="us-central1",
    project_id="practise-dev",
    dag=dag,
    job={
        "reference": {"project_id": "practise-dev"},
        "placement": {"cluster_name": "practise-orders-cluster"},
        "pyspark_job": {
            "main_python_file_uri": "gs://practise-dev-data/pyspark_mysql_gcs_extraction.py",
            "args": []
        },
    },
)

submit_pyspark_job