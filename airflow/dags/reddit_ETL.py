from os import remove
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime


output_name = datetime.now().strftime("%Y%m%d")

default_args = {
    "owner": "airflow", 
    "depends_on_past": False, 
    "retries": 1}

with DAG(
    dag_id = "reddit_ETL",
    description = "Reddit ETL Pipeline",
    schedule_interval = "10 15 * * *",
    default_args = default_args,
    start_date = days_ago(1),
    catchup = False,
    max_active_runs = 1
) as dag:

    reddit_api_extract = BashOperator(
        task_id="reddit_api_extract",
        bash_command=f"python /opt/airflow/tasks/reddit_to_csv.py {output_name}",
        dag=dag,
    )
    reddit_api_extract.doc_md = "Extract Reddit data and store as CSV"

    upload_csv_s3 = BashOperator(
        task_id="upload_csv_s3",
        bash_command=f"python /opt/airflow/tasks/csv_to_s3.py {output_name}",
        dag=dag,
    )
    upload_csv_s3.doc_md = "Upload Reddit CSV data to S3 bucket"

    s3_ingest_redshift = BashOperator(
        task_id="s3_ingest_redshift",
        bash_command=f"python /opt/airflow/tasks/s3_to_redshift.py {output_name}",
        dag=dag,
    )
    s3_ingest_redshift.doc_md = "Copy S3 CSV file to Redshift table"

reddit_api_extract >> upload_csv_s3 >> s3_ingest_redshift
