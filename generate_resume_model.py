import pandas as pd
import re
import pickle
import os

# Load the Excel dataset
df = pd.read_excel("UpdatedResumeDataSet.xlsx")

# Clean the resume text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text))
    return text.lower().strip()

df = df[['Resume']].dropna()
df['cleaned'] = df['Resume'].apply(clean_text)

# Create 'model' folder if it doesn't exist
os.makedirs('model', exist_ok=True)

# Save the DataFrame to pickle file
with open("model/resume_model.pkl", "wb") as f:
    pickle.dump(df, f)

print("✅ resume_model.pkl created successfully.")
