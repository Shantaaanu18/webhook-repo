
import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'pymongo']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install -r requirements.txt")
        return False
    return True

def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ MongoDB connection - OK")
        return True
    except Exception as e:
        print("❌ MongoDB connection failed")
        print(f"Error: {e}")
        print("\n🔧 To fix this:")
        print("1. Install MongoDB: https://docs.mongodb.com/manual/installation/")
        print("2. Start MongoDB service:")
        print("   - Windows: Start MongoDB service")
        print("   - macOS: brew services start mongodb-community")
        print("   - Linux: sudo systemctl start mongod")
        print("3. Or use a remote MongoDB by setting MONGODB_URI environment variable")
        return False

def main():
    print("🚀 GitHub Webhook Handler - Startup Check")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_mongodb():
        print("\n⚠️  MongoDB is required but not accessible.")
        print("The app will start but won't be able to save events.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("Starting Flask application...")
    print("=" * 50)
    
    # Start the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 