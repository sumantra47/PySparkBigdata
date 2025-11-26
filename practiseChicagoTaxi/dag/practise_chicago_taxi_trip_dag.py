# python
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import logging

DEFAULT_PROJECT = os.environ.get("GCP_PROJECT", "PROJECT_ID")
DEFAULT_REGION = "us-central1"
DEFAULT_CLUSTER = os.environ.get("DP_CLUSTER_NAME", "practise-chicago-taxi-trip-cluster")
# enforce minimum of 2 workers
DEFAULT_WORKERS = max(2, int(os.environ.get("DP_NUM_WORKERS", "2")))

cluster_config = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "e2-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},
    },
    "worker_config": {
        "num_instances": DEFAULT_WORKERS,
        "machine_type_uri": "e2-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},
    },
    "endpoint_config": {"enable_http_port_access": True},
    "lifecycle_config": {"idle_delete_ttl": {"seconds": 600}},
}

default_args = {"owner": "airflow", "depends_on_past": False}

with DAG(
        dag_id="practise_chicago_taxi_trip",
        default_args=default_args,
        description="practise_chicago_taxi_trip_cluster",
        schedule_interval=None,
        start_date=days_ago(1),
        catchup=False,
        tags=["dataproc", "chicago"],
) as dag:

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_practise_chicago_taxi_trip_cluster",
        project_id=DEFAULT_PROJECT,
        cluster_config=cluster_config,
        region=DEFAULT_REGION,
        cluster_name=DEFAULT_CLUSTER,
        dag=dag
    )

    submit_pyspark_job = DataprocSubmitJobOperator(
        task_id="submit_pyspark_job",
        region="us-central1",
        project_id="practise-dev",
        dag=dag,
        job={
            "reference": {"project_id": "practise-dev"},
            "placement": {"cluster_name": "practise-chicago-taxi-trip-cluster"},
            "pyspark_job": {
                "main_python_file_uri": "gs://practise-dev-data/chicagoTaxiTrips.py",
                "args": []
            },
        },
    )

    create_cluster >> submit_pyspark_job