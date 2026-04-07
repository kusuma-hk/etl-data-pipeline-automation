"""
Extract Module: Read CSV data
Handles data extraction from CSV source files
"""

import pandas as pd
import logging
import os
from config import CSV_FILE_PATH, LOG_FILE_PATH

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


def extract_data(csv_path: str = CSV_FILE_PATH) -> pd.DataFrame:
    """
    Extract data from CSV file.
    
    Args:
        csv_path (str): Path to the CSV file to extract
        
    Returns:
        pd.DataFrame: Extracted data as DataFrame
        
    Raises:
        FileNotFoundError: If CSV file does not exist
        Exception: For any other extraction errors
    """
    try:
        # Validate file exists
        if not os.path.exists(csv_path):
            logger.error(f"CSV file not found at: {csv_path}")
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        logger.info(f"Starting data extraction from: {csv_path}")
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        logger.info(f"Successfully extracted {len(df)} rows from CSV")
        logger.info(f"Columns: {list(df.columns)}")
        logger.debug(f"Data shape: {df.shape}")
        
        return df
    
    except FileNotFoundError as fe:
        logger.error(f"File error: {str(fe)}")
        raise
    except pd.errors.ParserError as pe:
        logger.error(f"CSV parsing error: {str(pe)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {str(e)}")
        raise


if __name__ == '__main__':
    # Test extraction
    try:
        data = extract_data()
        print("\n=== Extracted Data ===")
        print(data.head())
        print(f"\nTotal rows: {len(data)}")
    except Exception as e:
        print(f"Error: {e}")
