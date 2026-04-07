# ⚡ Quick Run (2 Minutes)

## TL;DR - Get Started Now

### 1️⃣ Setup (90 seconds)

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Configure MySQL (30 seconds)

```bash
# Open Command Prompt and run this
mysql -u root -p

# Leave password blank, press Enter
# Paste this and press Enter:
```

```sql
CREATE DATABASE etl_pipeline_db;
EXIT;
```

### 3️⃣ Run Pipeline (10 seconds)

```bash
python main.py
```

### ✅ Done!

You should see:
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
```

---

## 📋 If Something Goes Wrong

### "Connection refused"
```bash
# Start MySQL
net start MySQL80
```

### "Module not found"
```bash
pip install mysql-connector-python
```

### "CSV file not found"
- File exists at: `data/sales_data.csv`
- Check it with: `type data\sales_data.csv`

### Other issues?
See `SETUP_GUIDE.md` for detailed troubleshooting

---

## 🎯 What Happens

1. **EXTRACT** - Reads 20 rows from CSV
2. **TRANSFORM** - Cleans data, removes nulls, creates totals
3. **VALIDATE** - Verifies data quality
4. **LOAD** - Inserts cleaned data into MySQL

Result: **19 rows** in `etl_pipeline_db.sales_data` table

---

## 📝 Verify It Worked

```bash
# Check logs
type logs\etl.log

# Verify MySQL data
mysql -u root -p -e "SELECT COUNT(*) FROM etl_pipeline_db.sales_data;"
```

---

**That's it! You now have a working ETL pipeline. 🎉**

For more details: See README.md
