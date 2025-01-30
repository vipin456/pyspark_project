from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from git import Repo
import os
import sys
from datetime import datetime

# Function to clone the repository
def clone_repo():
    # GitHub repository URL
    repo_url = 'https://github.com/vipin456/py_handles_csv.git'
    
    # Update repo_dir to your local system's desired path for the cloned repository
    repo_dir = r'C:\Users\vipin_sharma\python\airflow_docker\py_handles_csv'  # Set the local path

    # Check if repository already exists locally
    if not os.path.exists(repo_dir):
        print(f'Cloning repository from {repo_url}...')
        Repo.clone_from(repo_url, repo_dir)  # Clone the repository
    else:
        print(f'Repository already exists at {repo_dir}.')  # If repo already exists

    # Now you can import your script after cloning
    sys.path.insert(0, repo_dir)  # Add the repo directory to sys.path for importing modules

    from ascrape import ascrape  # Import class from the cloned repo
    scraper = ascrape()

    # Download the CSV file from GitHub using its raw URL
    csv_url = 'https://github.com/vipin456/py_handles_csv/blob/main/employee_data1.csv'
    response = requests.get(csv_url)
    
    if response.status_code == 200:
        # Save the content of the file locally
        csv_file_path = r'C:\Users\vipin_sharma\python\airflow_docker\employee_data1.csv'
        with open(csv_file_path, 'wb') as file:
            file.write(response.content)
        print(f'CSV file downloaded and saved to {csv_file_path}')
        # Now use the local path to process the CSV file
        scraper.read_csv_file(csv_file_path)
    else:
        print(f"Failed to download the file. HTTP Status code: {response.status_code}")


# Define your Airflow DAG
dag = DAG(
    'git_clone_and_scrape_dag',
    description='A simple DAG to clone GitHub repo and run scraping',
    schedule_interval=None,  # Run manually
    start_date=datetime(2025, 1, 1),
    catchup=False
)

# Define the PythonOperator to call the function
clone_repo_task = PythonOperator(
    task_id='clone_repo_task',
    python_callable=clone_repo,
    dag=dag,
)
