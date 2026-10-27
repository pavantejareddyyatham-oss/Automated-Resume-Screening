import os
import pandas as pd

file_path = "UpdatedResumeDataSet.xlsx"

# Step 1: Check if file exists
if os.path.exists(file_path):
    print(f"✅ File found: {file_path}")
else:
    print(f"❌ File NOT found: {file_path}")

# Step 2: Try reading the file
try:
    df = pd.read_excel(file_path)
    print("✅ Excel file read successfully")
    print("📄 First 5 rows:")
    print(df.head())
except Exception as e:
    print("❌ Error reading Excel file:", e)
