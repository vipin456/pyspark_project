from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 18),  # यह पहले से सही है
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'my_first_dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(minutes=5),  # हर 5 मिनट में चलाने के लिए
    catchup=False,  # ताकि missed runs ना हों
) as dag:

    # Define task1 function
    def run_task1():
        print("Task 1 is running")

    task1 = PythonOperator(
        task_id='task1',
        python_callable=run_task1,
    )

    # Define task2 function
    def run_task2():
        print("Task 2 is running")

    task2 = PythonOperator(
        task_id='task2',
        python_callable=run_task2,
    )

    # Set task dependencies
    task1 >> task2
