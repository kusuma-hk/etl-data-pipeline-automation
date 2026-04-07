# 🚀 Quick Setup Guide for Windows

This guide will help you set up and run the ETL Data Pipeline project on Windows.

## ✅ Prerequisites

Before starting, ensure you have:

1. **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
   - Check: `python --version`
   - Add Python to PATH during installation

2. **MySQL Server 8.0+** installed and running
   - Check: `mysql --version`
   - Verify running: Services → MySQL80 (or right-click services)

3. **Git** installed (optional, for version control)
   - Check: `git --version`

## 📝 Step-by-Step Setup

### Step 1: Create Virtual Environment

```cmd
# Navigate to project directory
cd c:\Users\Kushigowda\Documents\6\ MCA\ A\etl-data-pipeline-automation

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) at the start of your command line
```

### Step 2: Install Dependencies

```cmd
# Make sure virtual environment is activated
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages:
- pandas 2.0.3
- mysql-connector-python 8.0.33
- apache-airflow 2.6.3
- python-dotenv 1.0.0

### Step 3: MySQL Database Setup

#### Option A: Command Prompt (Recommended)

```cmd
# Open Command Prompt as Administrator
# Connect to MySQL
mysql -u root -p

# You'll be prompted for password (default: empty, just press Enter)
```

Then execute:

```sql
-- Create database
CREATE DATABASE etl_pipeline_db;

-- Create user (optional but recommended)
CREATE USER 'etl_user'@'localhost' IDENTIFIED BY 'mypassword123';
GRANT ALL PRIVILEGES ON etl_pipeline_db.* TO 'etl_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;

-- Exit
EXIT;
```

#### Option B: MySQL Workbench (GUI)

1. Open MySQL Workbench
2. Click "+" to create new connection
3. Fill in connection details
4. Double-click connection to open
5. Execute SQL commands:
   ```sql
   CREATE DATABASE etl_pipeline_db;
   CREATE USER 'etl_user'@'localhost' IDENTIFIED BY 'mypassword123';
   GRANT ALL PRIVILEGES ON etl_pipeline_db.* TO 'etl_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Step 4: Configure Environment

Create `.env` file in project root:

```cmd
# Open Notepad
notepad .env
```

Add content:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=etl_pipeline_db
```

**If you created MySQL user, use:**

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=etl_user
MYSQL_PASSWORD=mypassword123
MYSQL_DATABASE=etl_pipeline_db
```

Save the file (Ctrl+S).

## 🏃 Running the Pipeline

### Test 1: Verify Python Setup

```cmd
# Make sure virtual environment is active (venv) prefix
python --version
python -c "import pandas; print('Pandas OK')"
python -c "import mysql.connector; print('MySQL OK')"
```

### Test 2: Run ETL Pipeline

```cmd
# Make sure you're in project root and virtual environment is active
python main.py
```

**Expected Output:**

```
============================================================
ETL DATA PIPELINE AUTOMATION
============================================================

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

Check logs at: c:\(...)\logs\etl.log
```

### Test 3: Verify MySQL Data

```cmd
# Connect to MySQL
mysql -u root -p

# In MySQL
USE etl_pipeline_db;
SELECT COUNT(*) FROM sales_data;
SELECT * FROM sales_data LIMIT 5;

EXIT;
```

## ⚙️ Airflow Setup (Optional)

### Step 1: Initialize Airflow

```cmd
# Set Airflow home directory
set AIRFLOW_HOME=%cd%\airflow

# Initialize Airflow database
airflow db init

# Wait for completion (~1-2 minutes)
```

### Step 2: Start Airflow Services

**Terminal 1 - Start Scheduler:**

```cmd
set AIRFLOW_HOME=%cd%\airflow
airflow scheduler
```

Keep this running in the background.

**Terminal 2 - Start Web UI:**

```cmd
set AIRFLOW_HOME=%cd%\airflow
airflow webserver --port 8080
```

### Step 3: Access Airflow UI

1. Open browser: `http://localhost:8080`
2. Login with default credentials: `admin` / `admin`
3. Find DAG: **etl_pipeline**
4. Toggle the DAG to enabled (blue switch)
5. Click "Trigger DAG" to run manually
6. Click refresh to see task execution

## 🐛 Troubleshooting

### Issue: "MySQL Connection Refused"

```cmd
# Check MySQL is running (Windows Services)
# Start MySQL service
net start MySQL80

# Or use Services GUI:
# Windows → Services → MySQL80 (right-click → Start)
```

### Issue: "Module Not Found"

```cmd
# Ensure virtual environment is activated (venv) prefix
# Reinstall packages
pip install -r requirements.txt

# Or specific package
pip install mysql-connector-python
```

### Issue: ".env file not found"

```cmd
# Create .env file
type nul > .env

# Or copy from example
copy .env.example .env

# Edit with notepad
notepad .env
```

### Issue: "FileNotFoundError: CSV file not found"

```cmd
# Verify CSV file exists
dir data\sales_data.csv

# Should show file with 20 rows
```

### Issue: "Access denied for user 'root'@'localhost'"

```cmd
# Update password in .env
# Then try again
python main.py

# Or reset MySQL root password
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';
FLUSH PRIVILEGES;
```

## 📊 File Structure Verification

After setup, verify you have all files:

```
✓ data/sales_data.csv
✓ scripts/extract.py
✓ scripts/transform.py
✓ scripts/load.py
✓ scripts/__init__.py
✓ airflow/etl_dag.py
✓ config.py
✓ main.py
✓ requirements.txt
✓ .env (created by you)
✓ .env.example
✓ .gitignore
✓ README.md
```

## 🎯 Next Steps

1. **Run Pipeline**: `python main.py`
2. **Check Logs**: `logs/etl.log`
3. **Verify Data**: Check MySQL database
4. **Setup Airflow**: Follow Airflow steps above
5. **Read Full README**: See README.md for detailed info

## 📚 Helpful Commands

```cmd
# Activate virtual environment
venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Run main pipeline
python main.py

# Test extract module
python -c "from scripts.extract import extract_data; print(extract_data())"

# Check logs
type logs\etl.log

# View MySQL databases
mysql -u root -p -e "SHOW DATABASES;"

# Stop Airflow
# CTRL+C in both terminals

# Remove virtual environment (if needed)
rmdir /s /q venv
```

## ✨ Success Checklist

- [ ] Python 3.10+ installed
- [ ] MySQL Server running
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (pip list shows all packages)
- [ ] .env file created with correct credentials
- [ ] MySQL database created (etl_pipeline_db)
- [ ] ETL pipeline runs successfully (`python main.py`)
- [ ] Logs created in `logs/etl.log`
- [ ] Data inserted into MySQL database
- [ ] (Optional) Airflow DAG configured and running

---

**Questions?** Check README.md or logs/etl.log for detailed information.

**Last Updated:** January 2024
