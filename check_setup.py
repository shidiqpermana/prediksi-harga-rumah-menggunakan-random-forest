"""
Script untuk mengecek setup dan dependencies sebelum menjalankan aplikasi
"""

import sys
import os

def check_python_version():
    """Cek versi Python"""
    print("="*60)
    print("CHECKING PYTHON VERSION")
    print("="*60)
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8+ diperlukan!")
        return False
    else:
        print("✅ Python version OK")
        return True

def check_dependencies():
    """Cek dependencies yang diperlukan"""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'streamlit': 'streamlit',
        'joblib': 'joblib',
        'matplotlib': 'matplotlib'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install dengan: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

def check_data_files():
    """Cek file data yang diperlukan"""
    print("\n" + "="*60)
    print("CHECKING DATA FILES")
    print("="*60)
    
    required_files = ['train.csv']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All required data files found!")
        return True

def check_model_files():
    """Cek file model"""
    print("\n" + "="*60)
    print("CHECKING MODEL FILES")
    print("="*60)
    
    model_files = ['model.pkl', 'preprocessing_info.pkl']
    missing_files = []
    
    for file in model_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Warning: Model files not found!")
        print("Jalankan: python train_model.py untuk membuat model")
        return False
    else:
        print("\n✅ Model files found!")
        return True

def main():
    """Main function"""
    print("\n" + "="*60)
    print("HOUSE PRICE PREDICTION - SETUP CHECKER")
    print("="*60 + "\n")
    
    results = []
    
    # Check Python version
    results.append(check_python_version())
    
    # Check dependencies
    results.append(check_dependencies())
    
    # Check data files
    results.append(check_data_files())
    
    # Check model files
    model_exists = check_model_files()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if all(results):
        print("✅ All checks passed!")
        if not model_exists:
            print("\n⚠️  Next step: Run 'python train_model.py' to train the model")
        else:
            print("\n✅ Ready to run! Execute: streamlit run app.py")
    else:
        print("❌ Some checks failed. Please fix the errors above.")
        print("\n📝 Quick fix commands:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Train model: python train_model.py")
        print("   3. Run app: streamlit run app.py")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

