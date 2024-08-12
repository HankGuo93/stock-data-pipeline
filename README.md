# stock-data-pipeline

This repository contains an example of a data pipeline that fetches, processes, and stores stock data using Airflow and Alpha Vantage, with notifications on success or failure.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/data-pipeline-demo.git
    cd data-pipeline-demo
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Initialize and set up the pipeline environment:
    ```bash
    echo "export AIRFLOW_HOME=$(pwd)" >> ~/.bashrc
    source ~/.bashrc
    # adjust every path in airflow.cfg to your local path 
    # e.g. dags_folder = ~/airflow/dags -> dags_folder = ${AIRFLOW_HOME}/dags
    airflow db init
    airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
    ```
4. Make settings_local.cfg  
   use settings.cfg as a template

5. Start the pipeline:
    ```bash
    airflow webserver --port 8080
    airflow scheduler
    ```

5. Access the Airflow web interface at [http://localhost:8080](http://localhost:8080) and enable the `alpha_vantage_dag`.

## Configuration

- Place your Alpha Vantage API key in `config/settings.cfg`.
- Adjust file paths in the DAG script as necessary.

## Running the Pipeline

The pipeline will automatically run based on the schedule defined in the script (daily by default). You can also trigger it manually from the Airflow web interface.

## Data

Processed data files will be saved in the `data/` directory.
