from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import git
import subprocess
import logging

# Function to clone the repository from GitHub
def clone_repo():
    repo_url = "https://github.com/vipin456/call_api_from_requests.git"
    repo_dir = "/opt/airflow/dags/call_api_from_requests"  # Path to clone the repository

    if not os.path.exists(repo_dir):
        try:
            logging.info(f"Cloning repository from {repo_url} to {repo_dir}")
            git.Repo.clone_from(repo_url, repo_dir)
            logging.info("Repository cloned successfully.")
        except git.exc.GitCommandError as e:
            logging.error(f"Error cloning repo: {e}")
    else:
        logging.info(f"Repo already exists at {repo_dir}, skipping clone.")

# Function to run `main.py` with parameters
def run_main_script():
    repo_dir = "/opt/airflow/dags/call_api_from_requests"
    main_script_path = os.path.join(repo_dir, "main.py")

    # Define arguments
    command = [
        "python3", main_script_path,
        "--input_file", os.path.join(repo_dir, "inputs/in.csv"),
        "--manifest", os.path.join(repo_dir, "resources/manifest.xml"),
        "--script", os.path.join(repo_dir, "scripts/extract_data_from_api.py"),
        "--dev_mode", "true",
        "--settings", os.path.join(repo_dir, "settings/settings.json")
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Script Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing script: {e.stderr}")

# Set default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 30),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'github_pyspark_task',
    default_args=default_args,
    schedule_interval='@daily',
)

# Clone repo task
clone_task = PythonOperator(
    task_id='clone_github_repo',
    python_callable=clone_repo,
    dag=dag,
)

# Run the main.py script task
run_task = PythonOperator(
    task_id='run_pyspark_script',
    python_callable=run_main_script,
    dag=dag,
)

# Define task dependencies
clone_task >> run_task
