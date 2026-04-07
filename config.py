"""
Configuration file for ETL Data Pipeline
Store all database and application configurations
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MySQL Database Configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'etl_pipeline_db')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
CSV_FILE_PATH = os.path.join(DATA_DIR, 'sales_data.csv')
LOG_FILE_PATH = os.path.join(LOGS_DIR, 'etl.log')

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Airflow Configuration
AIRFLOW_HOME = os.path.join(BASE_DIR, 'airflow')
DAG_ID = 'etl_pipeline'
DEFAULT_DAG_OWNER = 'data_engineer'
DEFAULT_RETRIES = 1
DEFAULT_RETRY_DELAY_MINUTES = 5

# Table name
TABLE_NAME = 'sales_data'

if __name__ == '__main__':
    print("Configuration loaded successfully!")
    print(f"Database: {MYSQL_DATABASE}")
    print(f"CSV File: {CSV_FILE_PATH}")
    print(f"Log File: {LOG_FILE_PATH}")
