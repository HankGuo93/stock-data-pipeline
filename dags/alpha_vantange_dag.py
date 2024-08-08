import logging
import os
import time
from scripts import load_config, fetch_data, clean_data, send_email
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta


config = load_config('config/settings_local.cfg')

API_KEY = config['API_KEY']
DATA_PATH = config['DATA_PATH']
CLEANED_DATA_PATH = config['CLEANED_DATA_PATH']
FINAL_DATA_PATH = config['FINAL_DATA_PATH']
EMAIL_RECIPIENT = config['EMAIL_RECIPIENT']

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'alpha_vantage_dag',
    default_args=default_args,
    description='A DAG to fetch, clean, and store stock data from Alpha Vantage',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
)


def fetch_task():
    try:
        fetch_data(API_KEY, DATA_PATH)
        logging.info("Fetching stock data...")
    except Exception as e:
        logging.error(f"Error fetching stock data: {e}")
        raise


def clean_task():
    try:
        # 假設 clean_data 函數已經定義
        clean_data(DATA_PATH, CLEANED_DATA_PATH)
        logging.info("Cleaning stock data...")
    except Exception as e:
        logging.error(f"Error cleaning stock data: {e}")
        raise


def store_task():
    try:
        # 假設 os.rename 函數已經定義
        os.rename(CLEANED_DATA_PATH, FINAL_DATA_PATH)
        logging.info("Storing stock data...")
    except Exception as e:
        logging.error(f"Error storing stock data: {e}")
        raise


fetch_stock_data_task = PythonOperator(
    task_id='fetch_stock_data',
    python_callable=fetch_task,
    dag=dag
)

clean_stock_data_task = PythonOperator(
    task_id='clean_stock_data',
    python_callable=clean_task,
    dag=dag
)

store_stock_data_task = PythonOperator(
    task_id='store_stock_data',
    python_callable=store_task,
    dag=dag
)

success_email_task = send_email(
    task_id='send_success_email',
    to=EMAIL_RECIPIENT,
    subject='Stock data pipeline succeeded',
    html_content='<p>The stock data pipeline completed successfully.</p>',
    dag=dag
)

failure_email_task = send_email(
    task_id='send_failure_email',
    to=EMAIL_RECIPIENT,
    subject='Stock data pipeline failed',
    html_content='<p>The stock data pipeline failed.</p>',
    dag=dag
)

fetch_stock_data_task >> clean_stock_data_task >> store_stock_data_task >> success_email_task
[fetch_stock_data_task, clean_stock_data_task,
    store_stock_data_task] >> failure_email_task
