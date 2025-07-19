import os
import sys
from datetime import datetime, timedelta

from airflow.operators.python import PythonOperator

from airflow import DAG

# Adjust sys.path so Airflow can import your modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.embed.build_faiss_index import build_faiss_index
from src.etl.bbc_etl import run_etl
from src.scraper.scrape_bbc_tech import \
    run_scrape  #  need to add run_scrape() function there

default_args = {
    'owner': 'bigdata',
    'depends_on_past': False,
    
    'start_date': datetime(2025, 7, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'data_scrape_to_rag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['bigdata', 'rag', 'scrape', 'etl', 'embedding'],
) as dag:

    scrape_task = PythonOperator(
        task_id='scrape_bbc_tech',
        python_callable=run_scrape,
    )

    etl_task = PythonOperator(
        task_id='run_etl',
        python_callable=run_etl,
    )

    embed_task = PythonOperator(
        task_id='build_faiss_index',
        python_callable=build_faiss_index,
    )

    scrape_task >> etl_task >> embed_task
