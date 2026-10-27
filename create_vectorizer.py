import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os

data = pd.read_excel('UpdatedResumeDataSet.xlsx')
data = data[['Resume']].dropna().head(10)

def preprocess(text):
    return re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()

data['cleaned'] = data['Resume'].apply(preprocess)

vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(data['cleaned'])

os.makedirs('model', exist_ok=True)
with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ Vectorizer saved successfully as model/vectorizer.pkl")
