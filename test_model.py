import pickle
import os
import traceback

print("Testing model loading...")

try:
    print("Attempting to load vectorizer.pkl...")
    vectorizer_path = os.path.join('model', 'vectorizer.pkl')
    print(f"Looking for file at: {os.path.abspath(vectorizer_path)}")
    print(f"File exists: {os.path.exists(vectorizer_path)}")
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    print("✅ Vectorizer loaded successfully!")
    
    print("\nAttempting to load resume_model.pkl...")
    model_path = os.path.join('model', 'resume_model.pkl')
    print(f"Looking for file at: {os.path.abspath(model_path)}")
    print(f"File exists: {os.path.exists(model_path)}")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("✅ Resume model loaded successfully!")
    
    print("\nAll models loaded successfully! Your application should work fine.")
except Exception as e:
    print(f"❌ Error loading models: {str(e)}")
    print("Full error details:")
    traceback.print_exc()
    print("This might be why your application is not running.") 