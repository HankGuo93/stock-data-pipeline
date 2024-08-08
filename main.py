import os

from airflow import DAG
from airflow.utils.dates import days_ago
from scripts import load_config, fetch_data, clean_data, send_email

def main():
    default_args = {
        'owner': 'airflow',
        'start_date': days_ago(1),
    }
    dag = DAG(
        'stock_data_pipeline_test',
        default_args=default_args,
        description='An example DAG with EmailOperator',
        schedule_interval=None,
    )
    
    config = load_config('config/settings-local.cfg')

    api_key = config['API_KEY']
    data_path = config['DATA_PATH']
    cleaned_data_path = config['CLEANED_DATA_PATH']
    final_data_path = config['FINAL_DATA_PATH']
    email_recipient = config['EMAIL_RECIPIENT']

    try:
        print("Fetching data...")
        raw_data_path = fetch_data(api_key, data_path)
        print(f"Data fetched and stored at {raw_data_path}")

        print("Cleaning data...")
        cleaned_data_path = clean_data(raw_data_path, cleaned_data_path)
        print(f"Data cleaned and stored at {cleaned_data_path}")

        print("Storing data...")
        os.rename(cleaned_data_path, final_data_path)
        print(f"Data stored at {final_data_path}")

        print("Sending success notification...")
        success_email = send_email(
            task_id='send_success_email',
            to=email_recipient,
            subject='Stock Data Processing Completed',
            html_content=f'Data successfully processed and stored at: {final_data_path}',
            dag=dag
        )
        success_email
        print("Success notification sent.")
    except Exception as e:
        print("An error occurred:", str(e))
        failure_email = send_email(
            task_id='send_failure_email',
            to=email_recipient,
            subject='Stock Data Processing Failed',
            html_content=f'The stock data processing DAG has failed. Error: {str(e)}',
            dag=dag
        )
        failure_email
        print("Failure notification sent.")

if __name__ == "__main__":
    main()

