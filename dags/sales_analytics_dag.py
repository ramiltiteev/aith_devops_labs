from __future__ import annotations

import pendulum
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


with DAG(
    dag_id="sales_analytics_spark_pipeline",
    description="Runs sales analytics as a PySpark job on a Spark standalone cluster.",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["lab", "analytics", "spark"],
) as dag:
    SparkSubmitOperator(
        task_id="run_sales_analytics_spark_job",
        application="/opt/airflow/spark/sales_analytics_spark_job.py",
        conn_id="spark_default",
        name="sales_analytics_spark_job",
        verbose=True,
        conf={
            "spark.submit.deployMode": "client",
            "spark.driver.host": "airflow-scheduler",
            "spark.driver.bindAddress": "0.0.0.0",
            "spark.ui.port": "4040",
        },
        application_args=["--output", "/opt/airflow/reports/sales_report.json"],
    )
