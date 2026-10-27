from flask import Flask, render_template, request, flash
import pandas as pd
import re
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Ensure model path is resolved relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
vectorizer = None
vectorizer_path = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')
if os.path.exists(vectorizer_path):
    # Try loading the vectorizer from the specified path
    try:
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
    except Exception:
        vectorizer = None

# --- Preprocessing Function ---
def preprocess_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()

def identify_resume_column(df):
    """Identify the most likely column containing resume text."""
    possible_names = ['resume', 'text', 'content', 'description', 'details']
    
    # Check for exact matches first (case-insensitive)
    for col in df.columns:
        if col.lower() in possible_names:
            return col
            
    # If no exact match, look for columns containing these words
    for col in df.columns:
        if any(name in col.lower() for name in possible_names):
            return col
            
    # If still no match, try to identify based on content
    for col in df.columns:
        try:
            # Sample a non-null value from the column
            non_null = df[col].dropna()
            if non_null.empty:
                continue
            sample = non_null.iloc[0]
        except Exception:
            continue
        if isinstance(sample, str) and len(sample) > 100:  # Assuming resume text is typically long
            return col
            
    return None

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/process', methods=['POST'])
def process():
    file = request.files.get('file')  # safe retrieval; may be None
    job_description = request.form.get('job_description', '').strip()
    
    # Get resume range parameters
    try:
        start_index = max(1, int(request.form.get('start_index', 1)))
        end_index = max(start_index, int(request.form.get('end_index', 50)))
    except ValueError:
        start_index = 1
        end_index = 50
        flash('Invalid range values. Using default range (1-50).')
    
    if file is None or not getattr(file, "filename", "") or not job_description:
        flash('Please provide both a resume dataset and a job description.')
        return render_template('index.html', result=[])

    # Validate file extension
    ext = file.filename.split('.')[-1].lower()
    if ext not in ['csv', 'xlsx', 'xls']:
        flash('Please upload a CSV or Excel file.')
        return render_template('index.html', result=[])

    try:
        # Read the file
        if ext == 'csv':
            data = pd.read_csv(file)
        else:
            data = pd.read_excel(file)

        # Show dataset size information
        total_resumes = len(data)
        if total_resumes < end_index:
            flash(f'Note: Dataset contains only {total_resumes} resumes. Adjusting end range.')
            end_index = total_resumes
        
        if start_index > total_resumes:
            flash(f'Start index exceeds dataset size. Adjusting to start from 1.')
            start_index = 1

        # Identify the resume column
        resume_column = identify_resume_column(data)
        if not resume_column:
            flash('Could not identify a column containing resume text. Please ensure your dataset has a column with resume content.')
            return render_template('index.html', result=[])

        # Clean and preprocess (using the specified range)
        data = data[[resume_column]].dropna()
        if data.empty:
            flash('No resume text found in the identified column after removing empty values.')
            return render_template('index.html', result=[])
        
        # Apply the resume range (convert to 0-based index for slicing)
        data_range = data.iloc[start_index-1:end_index].copy()
        
        if len(data_range) == 0:
            flash('No resumes found in the specified range. Please adjust your range.')
            return render_template('index.html', result=[])
            
        flash(f'Analyzing resumes {start_index} to {start_index + len(data_range) - 1} out of {total_resumes} total resumes.')
        
        # Create candidate labels based on the range
        data_range['Candidate'] = [f"Candidate {chr(65+i) if i < 26 else f'{chr(65+(i//26)-1)}{chr(65+(i%26))}'}" 
                            for i in range(len(data_range))]
        data_range['cleaned_resume'] = data_range[resume_column].apply(preprocess_text)

        # Use the submitted job description
        # If a pickled vectorizer wasn't loaded, build a local TfidfVectorizer and fit it on the corpus
        if vectorizer is None:
            local_vectorizer = TfidfVectorizer(stop_words='english')
            corpus = [preprocess_text(job_description)] + data_range['cleaned_resume'].tolist()
            local_vectorizer.fit(corpus)
            job_vector = local_vectorizer.transform([preprocess_text(job_description)])
            resume_vectors = local_vectorizer.transform(data_range['cleaned_resume'])
        else:
            job_vector = vectorizer.transform([preprocess_text(job_description)])
            resume_vectors = vectorizer.transform(data_range['cleaned_resume'])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(job_vector, resume_vectors).flatten()

        # Convert similarity scores to percentages (0-100)
        data_range['ATS_Score'] = (similarity_scores * 100).round().astype(int)
        data_range = data_range.sort_values(by='ATS_Score', ascending=False).reset_index(drop=True)
        data_range['Rank'] = data_range.index + 1

        result = data_range[['Candidate', 'ATS_Score', 'Rank']].to_dict(orient='records')
        return render_template('index.html', result=result)

    except Exception as e:
        flash(f'Error processing file: {str(e)}. Please ensure your file contains resume text data.')
        return render_template('index.html', result=[])

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('DEBUG', 'True').lower() in ('1', 'true', 'yes')
    print(f"Starting app on {host}:{port}, debug={debug}")
    app.run(host=host, port=port, debug=debug)
