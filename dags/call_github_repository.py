from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import git
import logging

# Function to clone the repository from GitHub
def clone_repo():
    repo_url = "https://github.com/vipin456/pyspark_project.git"
    repo_dir = "/opt/airflow/dags/py_handles_csv"  # Path to clone the repository (Use absolute path)

    # Check if the directory already exists
    if not os.path.exists(repo_dir):
        try:
            # Clone the repository
            logging.info(f"Cloning repository from {repo_url} to {repo_dir}")
            git.Repo.clone_from(repo_url, repo_dir)
            logging.info("Repository cloned successfully.")
        except git.exc.GitCommandError as e:
            logging.error(f"Error cloning repo: {e}")
    else:
        logging.info(f"Repo already exists at {repo_dir}, skipping clone.")

# Set default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 19),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'github_python_task',
    default_args=default_args,
    schedule_interval='@daily',  # You can adjust this based on your needs
)

# Define the task to clone the repo
clone_task = PythonOperator(
    task_id='clone_github_repo',
    python_callable=clone_repo,
    dag=dag,
)

# Define a dummy task to represent the next task (e.g., running the Python script)
run_task = PythonOperator(
    task_id='run_python_script',
    python_callable=lambda: print("This is where you would run your Python script."),
    dag=dag,
)

# Set task dependencies
clone_task >> run_task  # First the repository will be cloned, then the Python script will run
