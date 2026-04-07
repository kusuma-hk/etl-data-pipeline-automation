"""
Transform Module: Data cleaning and transformation
Handles data cleaning, validation, and feature engineering
"""

import pandas as pd
import logging
from config import LOG_FILE_PATH

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


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform and clean data.
    
    Operations:
    - Remove null values
    - Remove duplicates
    - Convert date column to datetime
    - Standardize column names
    - Create total_price column
    - Data validation
    
    Args:
        df (pd.DataFrame): Raw extracted data
        
    Returns:
        pd.DataFrame: Cleaned and transformed data
        
    Raises:
        Exception: For any transformation errors
    """
    try:
        logger.info("Starting data transformation")
        original_rows = len(df)
        
        # Step 1: Convert column names to lowercase and strip whitespace
        logger.info("Standardizing column names...")
        df.columns = df.columns.str.lower().str.strip()
        logger.debug(f"Standardized columns: {list(df.columns)}")
        
        # Step 2: Remove null values
        logger.info(f"Rows before removing nulls: {len(df)}")
        df = df.dropna()
        logger.info(f"Rows after removing nulls: {len(df)}")
        
        # Step 3: Remove duplicates
        logger.info(f"Rows before removing duplicates: {len(df)}")
        df = df.drop_duplicates()
        logger.info(f"Rows after removing duplicates: {len(df)}")
        
        # Step 4: Convert date column to datetime
        logger.info("Converting date column to datetime...")
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        logger.info("Date conversion completed")
        
        # Step 5: Convert quantity and price to numeric
        logger.info("Converting quantity and price to numeric...")
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Remove any rows with null values after conversion
        df = df.dropna()
        logger.info(f"Rows after numeric conversion: {len(df)}")
        
        # Step 6: Create new column - total_price
        logger.info("Creating total_price column...")
        df['total_price'] = df['quantity'] * df['price']
        logger.info("total_price column created successfully")
        
        # Step 7: Ensure order_id is integer
        df['order_id'] = df['order_id'].astype(int)
        
        # Step 8: Reset index
        df = df.reset_index(drop=True)
        
        rows_removed = original_rows - len(df)
        logger.info(f"Data transformation completed")
        logger.info(f"Rows processed: {original_rows}, Rows removed: {rows_removed}, Final rows: {len(df)}")
        logger.debug(f"Final columns: {list(df.columns)}")
        
        return df
    
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise


def validate_data(df: pd.DataFrame) -> bool:
    """
    Validate transformed data.
    
    Args:
        df (pd.DataFrame): Transformed data to validate
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    try:
        logger.info("Starting data validation...")
        
        # Check required columns
        required_columns = ['order_id', 'product', 'quantity', 'price', 'date', 'total_price']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Missing columns: {missing_columns}")
            return False
        
        # Check for null values
        if df.isnull().any().any():
            logger.error("Found null values in data")
            return False
        
        # Check quantity and price are positive
        if (df['quantity'] <= 0).any() or (df['price'] <= 0).any():
            logger.error("Found non-positive quantity or price values")
            return False
        
        # Check total_price calculation
        if not (df['total_price'] == df['quantity'] * df['price']).all():
            logger.error("total_price calculation is incorrect")
            return False
        
        logger.info("Data validation passed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error during validation: {str(e)}")
        return False


if __name__ == '__main__':
    # Test transformation
    from scripts.extract import extract_data
    
    try:
        raw_data = extract_data()
        transformed_data = transform_data(raw_data)
        is_valid = validate_data(transformed_data)
        
        print("\n=== Transformed Data ===")
        print(transformed_data.head())
        print(f"\nData types:\n{transformed_data.dtypes}")
        print(f"\nValidation result: {'PASSED' if is_valid else 'FAILED'}")
    except Exception as e:
        print(f"Error: {e}")
