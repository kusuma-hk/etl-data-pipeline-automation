"""
Airflow DAG: ETL Pipeline Automation
Orchestrates ETL tasks using Apache Airflow
DAG Name: etl_pipeline
Schedule: Daily at 00:00 UTC
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.decorators import apply_defaults
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.extract import extract_data
from scripts.transform import transform_data, validate_data
from scripts.load import load_data
import logging

logger = logging.getLogger(__name__)

# Default arguments for DAG
default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

# DAG definition
dag = DAG(
    dag_id='etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline for Sales Data',
    schedule_interval='0 0 * * *',  # Daily at midnight
    catchup=False,
    tags=['etl', 'sales', 'data_pipeline']
)


# Task 1: Extract Data
def extract_task():
    """Extract task: Load data from CSV file"""
    try:
        logger.info("Starting Extract Task")
        df = extract_data()
        logger.info(f"Extract task completed. Rows: {len(df)}")
        return {'status': 'success', 'rows': len(df)}
    except Exception as e:
        logger.error(f"Extract task failed: {str(e)}")
        raise


# Task 2: Transform Data
def transform_task(**context):
    """Transform task: Clean and transform data"""
    try:
        logger.info("Starting Transform Task")
        
        # Get data from previous task
        df = extract_data()
        
        # Transform data
        transformed_df = transform_data(df)
        
        # Validate data
        is_valid = validate_data(transformed_df)
        
        if not is_valid:
            raise Exception("Data validation failed")
        
        logger.info(f"Transform task completed. Rows: {len(transformed_df)}")
        
        # Push transformed data info to XCom
        context['task_instance'].xcom_push(
            key='transformed_rows',
            value=len(transformed_df)
        )
        
        return {'status': 'success', 'rows': len(transformed_df)}
    
    except Exception as e:
        logger.error(f"Transform task failed: {str(e)}")
        raise


# Task 3: Load Data
def load_task(**context):
    """Load task: Load cleaned data to MySQL database"""
    try:
        logger.info("Starting Load Task")
        
        # Get data
        df = extract_data()
        transformed_df = transform_data(df)
        
        # Load data
        load_data(transformed_df)
        
        logger.info(f"Load task completed. Rows: {len(transformed_df)}")
        
        # Push load info to XCom
        context['task_instance'].xcom_push(
            key='loaded_rows',
            value=len(transformed_df)
        )
        
        return {'status': 'success', 'rows': len(transformed_df)}
    
    except Exception as e:
        logger.error(f"Load task failed: {str(e)}")
        raise


# Create tasks
extract_operator = PythonOperator(
    task_id='extract_task',
    python_callable=extract_task,
    dag=dag,
    provide_context=True
)

transform_operator = PythonOperator(
    task_id='transform_task',
    python_callable=transform_task,
    dag=dag,
    provide_context=True
)

load_operator = PythonOperator(
    task_id='load_task',
    python_callable=load_task,
    dag=dag,
    provide_context=True
)

# Set task dependencies: extract -> transform -> load
extract_operator >> transform_operator >> load_operator

# Alternatively:
# extract_operator.set_downstream(transform_operator)
# transform_operator.set_downstream(load_operator)
