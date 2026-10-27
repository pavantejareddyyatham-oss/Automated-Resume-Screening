import pandas as pd
import re
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_excel('UpdatedResumeDataSet.xlsx')
data = data[['Resume', 'Category']].dropna().head(10)
data['Candidate'] = [f'Candidate {chr(65 + i)}' for i in range(len(data))]

def preprocess_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()

data['cleaned_resume'] = data['Resume'].apply(preprocess_text)

vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(data['cleaned_resume'])

os.makedirs('model', exist_ok=True)

with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('model/resume_data.pkl', 'wb') as f:
    pickle.dump(data[['Candidate', 'cleaned_resume']], f)

print("✅ Pickle files created: model/vectorizer.pkl and model/resume_data.pkl")
