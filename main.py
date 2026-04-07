"""
Main Script: Execute ETL Pipeline
Orchestrates the entire ETL process: Extract, Transform, Load
"""

import sys
import logging
from datetime import datetime
from config import LOG_FILE_PATH

# Import ETL modules
from scripts.extract import extract_data
from scripts.transform import transform_data, validate_data
from scripts.load import load_data

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


def run_etl_pipeline():
    """
    Execute complete ETL pipeline.
    
    Process:
    1. Extract data from CSV
    2. Transform and clean data
    3. Validate data
    4. Load data to MySQL database
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("=" * 60)
        logger.info(f"Starting ETL Pipeline - {datetime.now()}")
        logger.info("=" * 60)
        
        # Step 1: Extract
        logger.info("\n[STEP 1/4] EXTRACT PHASE")
        logger.info("-" * 60)
        raw_data = extract_data()
        logger.info(f"✓ Successfully extracted {len(raw_data)} rows")
        
        # Step 2: Transform
        logger.info("\n[STEP 2/4] TRANSFORM PHASE")
        logger.info("-" * 60)
        transformed_data = transform_data(raw_data)
        logger.info(f"✓ Successfully transformed data")
        
        # Step 3: Validate
        logger.info("\n[STEP 3/4] VALIDATION PHASE")
        logger.info("-" * 60)
        is_valid = validate_data(transformed_data)
        
        if not is_valid:
            logger.error("✗ Data validation failed!")
            return False
        
        logger.info("✓ Data validation passed")
        
        # Step 4: Load
        logger.info("\n[STEP 4/4] LOAD PHASE")
        logger.info("-" * 60)
        load_data(transformed_data)
        logger.info("✓ Successfully loaded data to MySQL")
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("ETL PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info(f"Total records processed: {len(transformed_data)}")
        logger.info(f"Completion time: {datetime.now()}")
        logger.info("=" * 60)
        
        return True
    
    except Exception as e:
        logger.error("\n" + "=" * 60)
        logger.error("ETL PIPELINE EXECUTION FAILED")
        logger.error("=" * 60)
        logger.error(f"Error: {str(e)}")
        logger.error("=" * 60)
        return False


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("ETL DATA PIPELINE AUTOMATION")
    print("=" * 60 + "\n")
    
    try:
        success = run_etl_pipeline()
        
        print("\n" + "=" * 60)
        if success:
            print("STATUS: ✓ PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"Check logs at: {LOG_FILE_PATH}")
            sys.exit(0)
        else:
            print("STATUS: ✗ PIPELINE FAILED")
            print("=" * 60)
            print(f"Check logs at: {LOG_FILE_PATH}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
        print("\n\n✗ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n\n✗ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
