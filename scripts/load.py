"""
Load Module: Load data to MySQL database
Handles database connections, table creation, and data insertion
"""

import pandas as pd
import mysql.connector
import logging
from config import (
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, 
    MYSQL_DATABASE, MYSQL_PORT, LOG_FILE_PATH, TABLE_NAME
)

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages MySQL database connections and operations.
    """
    
    def __init__(self, host: str = MYSQL_HOST, user: str = MYSQL_USER, 
                 password: str = MYSQL_PASSWORD, port: int = MYSQL_PORT):
        """
        Initialize database connection parameters.
        
        Args:
            host (str): MySQL host address
            user (str): MySQL username
            password (str): MySQL password
            port (int): MySQL port
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = MYSQL_DATABASE
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Establish connection to MySQL server.
        
        Raises:
            Exception: If connection fails
        """
        try:
            logger.info(f"Connecting to MySQL server at {self.host}:{self.port}")
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            logger.info("Successfully connected to MySQL server")
        except mysql.connector.Error as err:
            logger.error(f"Failed to connect to MySQL: {err}")
            raise
    
    def create_database(self):
        """
        Create database if not exists.
        
        Raises:
            Exception: If database creation fails
        """
        try:
            logger.info(f"Creating database '{self.database}' if not exists...")
            self.cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.database}"
            )
            self.connection.commit()
            logger.info(f"Database '{self.database}' ensured")
        except mysql.connector.Error as err:
            logger.error(f"Failed to create database: {err}")
            raise
    
    def use_database(self):
        """
        Select the target database.
        
        Raises:
            Exception: If database selection fails
        """
        try:
            logger.info(f"Switching to database '{self.database}'...")
            self.cursor.execute(f"USE {self.database}")
            logger.info(f"Successfully switched to database '{self.database}'")
        except mysql.connector.Error as err:
            logger.error(f"Failed to use database: {err}")
            raise
    
    def create_table(self, table_name: str = TABLE_NAME):
        """
        Create sales_data table if not exists.
        
        Args:
            table_name (str): Name of the table to create
            
        Raises:
            Exception: If table creation fails
        """
        try:
            logger.info(f"Creating table '{table_name}' if not exists...")
            
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL UNIQUE,
                product VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                date DATE NOT NULL,
                total_price DECIMAL(12, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logger.info(f"Table '{table_name}' ensured")
        except mysql.connector.Error as err:
            logger.error(f"Failed to create table: {err}")
            raise
    
    def insert_data(self, df: pd.DataFrame, table_name: str = TABLE_NAME):
        """
        Insert data into MySQL table.
        
        Args:
            df (pd.DataFrame): Data to insert
            table_name (str): Name of the table
            
        Raises:
            Exception: If data insertion fails
        """
        try:
            logger.info(f"Inserting {len(df)} records into table '{table_name}'...")
            
            insert_query = f"""
            INSERT INTO {table_name} 
            (order_id, product, quantity, price, date, total_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            product=VALUES(product),
            quantity=VALUES(quantity),
            price=VALUES(price),
            date=VALUES(date),
            total_price=VALUES(total_price)
            """
            
            records_inserted = 0
            for index, row in df.iterrows():
                try:
                    self.cursor.execute(insert_query, (
                        int(row['order_id']),
                        row['product'],
                        int(row['quantity']),
                        float(row['price']),
                        row['date'],
                        float(row['total_price'])
                    ))
                    records_inserted += 1
                except mysql.connector.Error as err:
                    logger.error(f"Error inserting row {index}: {err}")
                    continue
            
            self.connection.commit()
            logger.info(f"Successfully inserted {records_inserted} records")
            
            if records_inserted < len(df):
                logger.warning(f"Only {records_inserted}/{len(df)} records inserted")
        
        except Exception as e:
            logger.error(f"Failed to insert data: {str(e)}")
            raise
    
    def verify_data(self, table_name: str = TABLE_NAME) -> int:
        """
        Verify data was loaded successfully.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            int: Number of records in table
        """
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]
            logger.info(f"Table '{table_name}' now contains {count} records")
            return count
        except mysql.connector.Error as err:
            logger.error(f"Failed to verify data: {err}")
            return 0
    
    def close(self):
        """
        Close database connection.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")


def load_data(df: pd.DataFrame):
    """
    Load transformed data into MySQL database.
    
    Args:
        df (pd.DataFrame): Transformed data to load
        
    Raises:
        Exception: If loading fails
    """
    db_manager = None
    try:
        logger.info("Starting data loading process...")
        
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Connect to MySQL
        db_manager.connect()
        
        # Create database
        db_manager.create_database()
        
        # Use database
        db_manager.use_database()
        
        # Create table
        db_manager.create_table()
        
        # Insert data
        db_manager.insert_data(df)
        
        # Verify data
        record_count = db_manager.verify_data()
        
        logger.info(f"Data loading completed successfully with {record_count} records")
        
        return True
    
    except Exception as e:
        logger.error(f"Data loading failed: {str(e)}")
        raise
    
    finally:
        if db_manager:
            db_manager.close()


if __name__ == '__main__':
    # Test loading
    from scripts.extract import extract_data
    from scripts.transform import transform_data
    
    try:
        logger.info("Starting test load...")
        raw_data = extract_data()
        transformed_data = transform_data(raw_data)
        load_data(transformed_data)
        print("\n=== Loading completed successfully ===")
    except Exception as e:
        print(f"Error: {e}")
