import pandas as pd
import re
import pickle
import os

# Load your Excel file
data = pd.read_excel('UpdatedResumeDataSet.xlsx')
data = data[['Resume']].dropna().head(10)

# Clean the text
def preprocess(text):
    return re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()

data['cleaned'] = data['Resume'].apply(preprocess)

# Save properly as resume_model.pkl
os.makedirs('model', exist_ok=True)
with open('model/resume_model.pkl', 'wb') as f:
    pickle.dump(data, f)

print("✅ resume_model.pkl created successfully.")
print("Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")
