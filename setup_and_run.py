import subprocess
import sys
import os

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def main():
    print("=" * 50)
    print("Resume Screening Application Setup and Run")
    print("=" * 50)
    
    # Install dependencies
    print("\n[1/3] Installing required packages...")
    packages = ["Flask", "scikit-learn", "pandas", "openpyxl", "numpy"]
    for package in packages:
        print(f"\nInstalling {package}...")
        if not run_command(f"{sys.executable} -m pip install {package}"):
            print(f"Failed to install {package}. Please try manually: pip install {package}")
            return False
    
    # Test model loading
    print("\n[2/3] Testing model loading...")
    try:
        import pickle
        
        print("Testing vectorizer.pkl...")
        vectorizer_path = os.path.join('model', 'vectorizer.pkl')
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        print("✅ Vectorizer loaded successfully!")
        
        print("Testing resume_model.pkl...")
        model_path = os.path.join('model', 'resume_model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("✅ Resume model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        return False
    
    # Run the application
    print("\n[3/3] Starting the application...")
    print("\nThe application will start now. Please open your web browser and go to:")
    print("http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the application when you're done.")
    
    # Start the Flask application
    run_command(f"{sys.executable} app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nSetup failed. Please try running the commands manually:")
        print("1. pip install Flask scikit-learn pandas openpyxl numpy")
        print("2. python app.py")
    
    input("\nPress Enter to exit...") 