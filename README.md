# ETL Data Pipeline Automation

A complete, production-ready ETL (Extract, Transform, Load) data pipeline automation project using Python, Pandas, MySQL, and Apache Airflow. This project demonstrates best practices for building scalable data pipelines.

## 📋 Project Overview

This project implements an automated ETL pipeline that:
- **Extracts** sales data from CSV files
- **Transforms** and cleans the data (removes nulls, duplicates, standardizes columns)
- **Loads** processed data into a MySQL database
- **Schedules** execution using Apache Airflow (daily runs)
- **Logs** all operations for monitoring and debugging

## 🛠️ Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.10+ | Core programming language |
| **Pandas** | 2.0.3 | Data manipulation and analysis |
| **MySQL** | 8.0 | Data storage |
| **Apache Airflow** | 2.6.3 | Workflow orchestration |
| **mysql-connector** | 8.0.33 | MySQL connectivity |
| **python-dotenv** | 1.0.0 | Environment variable management |

## 📁 Project Architecture

```
etl-data-pipeline-automation/
│
├── data/
│   └── sales_data.csv                  # Source CSV data
│
├── scripts/
│   ├── extract.py                      # Data extraction module
│   ├── transform.py                    # Data transformation module
│   └── load.py                         # Data loading module
│
├── airflow/
│   └── etl_dag.py                      # Airflow DAG definition
│
├── logs/
│   └── etl.log                         # Pipeline execution logs
│
├── main.py                             # Main execution script
├── config.py                           # Configuration management
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (not in repo)
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- MySQL Server 8.0 or higher
- Git

### 1. Installation

#### Clone the repository
```bash
cd etl-data-pipeline-automation
```

#### Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

### 2. MySQL Setup

#### Option A: Using MySQL Command Line

```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE etl_pipeline_db;

# Create user (optional)
CREATE USER 'etl_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON etl_pipeline_db.* TO 'etl_user'@'localhost';
FLUSH PRIVILEGES;

exit;
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Create new database: `etl_pipeline_db`
3. Create new user with appropriate privileges

### 3. Configuration

Create `.env` file in project root:

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=etl_pipeline_db
```

Or modify `config.py` directly:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'etl_pipeline_db'
```

## 🏃 Running the Project

### Option 1: Manual Execution (Recommended for Testing)

```bash
# Ensure virtual environment is activated
python main.py
```

**Expected Output:**
```
============================================================
ETL DATA PIPELINE AUTOMATION
============================================================

INFO - Starting ETL Pipeline - 2024-XX-XX XX:XX:XX
[STEP 1/4] EXTRACT PHASE
✓ Successfully extracted 20 rows
[STEP 2/4] TRANSFORM PHASE
✓ Successfully transformed data
[STEP 3/4] VALIDATION PHASE
✓ Data validation passed
[STEP 4/4] LOAD PHASE
✓ Successfully loaded data to MySQL

============================================================
STATUS: ✓ PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

### Option 2: Apache Airflow Execution

#### Initialize Airflow Database

```bash
# Set Airflow home (Windows)
set AIRFLOW_HOME=%cd%\airflow

# Set Airflow home (macOS/Linux)
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize Airflow database
airflow db init
```

#### Start Airflow Services

```bash
# In terminal 1: Start Airflow Scheduler
airflow scheduler

# In terminal 2: Start Airflow Web UI
airflow webserver --port 8080
```

#### Access Airflow UI

1. Open browser: `http://localhost:8080`
2. Default credentials: `airflow` / `airflow`
3. Find DAG: `etl_pipeline`
4. Enable DAG (toggle switch)
5. Trigger DAG manually or wait for scheduled execution

#### DAG Details

- **DAG ID**: `etl_pipeline`
- **Schedule**: Daily at 00:00 UTC (midnight)
- **Retries**: 1
- **Retry Delay**: 5 minutes
- **Tasks**: 
  - `extract_task` - Extracts data from CSV
  - `transform_task` - Cleans and transforms data
  - `load_task` - Loads data to MySQL
- **Dependencies**: `extract → transform → load`

## 📊 Project Details

### Extract Phase (`scripts/extract.py`)

**Functionality:**
- Reads CSV file using Pandas
- Validates file existence
- Handles parsing errors
- Logs extraction metrics

**Key Function:** `extract_data(csv_path)`

```python
from scripts.extract import extract_data

df = extract_data()
print(df.head())
```

### Transform Phase (`scripts/transform.py`)

**Transformations Applied:**
1. **Standardize column names** - Convert to lowercase, strip whitespace
2. **Remove null values** - Drop rows with missing data
3. **Remove duplicates** - Drop duplicate rows
4. **Date conversion** - Convert date column to datetime
5. **Numeric conversion** - Convert quantity and price to numeric types
6. **Feature engineering** - Create `total_price = quantity × price`
7. **Data validation** - Verify data quality

**Key Functions:**
- `transform_data(df)` - Apply transformations
- `validate_data(df)` - Validate transformed data

```python
from scripts.extract import extract_data
from scripts.transform import transform_data, validate_data

raw_df = extract_data()
transformed_df = transform_data(raw_df)
is_valid = validate_data(transformed_df)
```

### Load Phase (`scripts/load.py`)

**Database Operations:**
1. Connect to MySQL server
2. Create database if not exists
3. Create table with appropriate schema
4. Insert/update data using `ON DUPLICATE KEY UPDATE`
5. Verify data insertion
6. Handle errors gracefully

**Table Schema:**
```sql
CREATE TABLE sales_data (
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
```

**Key Class:** `DatabaseManager`

```python
from scripts.load import load_data

load_data(transformed_df)
```

## 📝 Sample Data

The project includes `data/sales_data.csv` with 20 sample rows:

| order_id | product | quantity | price | date |
|----------|---------|----------|-------|------|
| 1001 | Laptop | 2 | 50000 | 2024-01-15 |
| 1002 | Mouse | 5 | 500 | 2024-01-16 |
| ... | ... | ... | ... | ... |

**Features in sample data:**
- Valid and invalid date formats
- Missing quantity values (row 1018)
- Integer and decimal quantities
- Various product types

## 🔍 Logging

All operations are logged to `logs/etl.log`:

```
2024-01-15 10:30:45 - scripts.extract - INFO - Starting data extraction from: data/sales_data.csv
2024-01-15 10:30:45 - scripts.extract - INFO - Successfully extracted 20 rows from CSV
2024-01-15 10:30:45 - scripts.transform - INFO - Starting data transformation
2024-01-15 10:30:45 - scripts.load - INFO - Connecting to MySQL server at localhost:3306
```

**Log Format:**
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Log Levels:**
- `DEBUG` - Detailed information
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages

## ❌ Error Handling

### Common Issues and Solutions

#### Issue: "FileNotFoundError: CSV file not found"
**Solution:**
- Verify `data/sales_data.csv` exists
- Check file path in `config.py`
- Use absolute paths if needed

#### Issue: "Connection refused" (MySQL)
**Solution:**
- Ensure MySQL Server is running
- Check credentials in `.env` or `config.py`
- Verify MySQL host and port
- For Windows: `net start MySQL80`

#### Issue: "Access denied for user 'root'@'localhost'"
**Solution:**
- Update MySQL password in `.env`
- Verify user permissions
- Reset MySQL password if forgotten

#### Issue: "ModuleNotFoundError: No module named 'mysql'"
**Solution:**
```bash
pip install mysql-connector-python
```

#### Issue: Airflow DAG not appearing
**Solution:**
- Verify `AIRFLOW_HOME` is set correctly
- Check DAG syntax: `airflow dags validate etl_dag.py`
- Restart scheduler and webserver

## 🧪 Testing

### Manual Testing

```bash
# Test Extract
python -c "from scripts.extract import extract_data; print(extract_data())"

# Test Transform
python -c "from scripts.extract import extract_data; from scripts.transform import transform_data; print(transform_data(extract_data()))"

# Test Load
python main.py
```

### Data Validation

```python
from scripts.extract import extract_data
from scripts.transform import transform_data, validate_data

raw_df = extract_data()
transformed_df = transform_data(raw_df)
is_valid = validate_data(transformed_df)
print(f"Data valid: {is_valid}")
```

## 📈 Example Output

### Console Output

```
============================================================
ETL DATA PIPELINE AUTOMATION
============================================================

[STEP 1/4] EXTRACT PHASE
------------------------------------------------------------
2024-01-15 10:30:45 - scripts.extract - INFO - Successfully extracted 20 rows from CSV

[STEP 2/4] TRANSFORM PHASE
------------------------------------------------------------
2024-01-15 10:30:46 - scripts.transform - INFO - Rows before removing nulls: 20
2024-01-15 10:30:46 - scripts.transform - INFO - Rows after removing nulls: 19
2024-01-15 10:30:46 - scripts.transform - INFO - total_price column created successfully

[STEP 3/4] VALIDATION PHASE
------------------------------------------------------------
2024-01-15 10:30:46 - scripts.transform - INFO - Data validation passed successfully

[STEP 4/4] LOAD PHASE
------------------------------------------------------------
2024-01-15 10:30:47 - scripts.load - INFO - Connecting to MySQL server at localhost:3306
2024-01-15 10:30:47 - scripts.load - INFO - Database 'etl_pipeline_db' ensured
2024-01-15 10:30:47 - scripts.load - INFO - Table 'sales_data' ensured
2024-01-15 10:30:47 - scripts.load - INFO - Successfully inserted 19 records

============================================================
STATUS: ✓ PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

### MySQL Verification

```sql
-- Check records
SELECT COUNT(*) FROM sales_data;  -- Output: 19

-- View sample records
SELECT * FROM sales_data LIMIT 5;

-- Check data types
DESCRIBE sales_data;

-- Verify calculations
SELECT order_id, quantity, price, total_price 
FROM sales_data 
WHERE total_price != quantity * price;  -- Should return 0 rows
```

## 🔄 Database Configuration

### Connection String

```
Host: localhost
Port: 3306
User: root
Password: (your password)
Database: etl_pipeline_db
```

### Environment Variables

Create `.env` file for sensitive data:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=etl_pipeline_db
```

### Remote MySQL Server

To connect to remote server:

```env
MYSQL_HOST=192.168.1.100
MYSQL_USER=etl_user
MYSQL_PASSWORD=secure_password
MYSQL_DATABASE=etl_pipeline_db
```

## 🎯 Future Improvements

### Phase 2 Features
- [ ] Add data quality metrics and reports
- [ ] Implement incremental loading (only new/updated records)
- [ ] Add email notifications on pipeline failure
- [ ] Create data quality dashboards
- [ ] Implement data lineage tracking

### Phase 3 Enhancements
- [ ] Add multiple CSV source support
- [ ] Implement data partitioning by date
- [ ] Add data encryption in transit
- [ ] Create backup and recovery procedures
- [ ] Add API endpoint for data queries

### Phase 4 Optimization
- [ ] Optimize MySQL queries with indexing
- [ ] Implement parallel processing for large datasets
- [ ] Add caching mechanisms
- [ ] Monitor pipeline performance metrics
- [ ] Scale to handle petabyte-level data

### Additional Features
- [ ] Unit tests and integration tests
- [ ] CI/CD pipeline integration
- [ ] Automated schema migrations
- [ ] Data profiling and anomaly detection
- [ ] Metadata management system

---

## 🎓 Learning Resources

### Understanding ETL
- [What is ETL?](https://en.wikipedia.org/wiki/Extract,_transform,_load)
- [ETL Best Practices](https://www.talend.com/resources/etl-best-practices/)

### Python Data Processing
- [Pandas Documentation](https://pandas.pydata.org/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

### Apache Airflow
- [Airflow Documentation](https://airflow.apache.org/)
- [Airflow DAG Basics](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)

### MySQL
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQL Tutorial](https://www.w3schools.com/sql/)


