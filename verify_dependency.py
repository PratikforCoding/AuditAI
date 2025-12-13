"""
Verify all required dependencies are installed
Run this before running the main application
"""

import sys

def check_import(module_name, package_name=None):
    """Try to import a module and report status"""
    try:
        __import__(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name} - NOT INSTALLED")
        print(f"   Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 CHECKING DEPENDENCIES")
    print("=" * 60)
    
    dependencies = [
        # Core
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("pydantic_settings", "Pydantic Settings"),
        
        # Database
        ("pymongo", "PyMongo (MongoDB)"),
        
        # Security
        ("passlib", "Passlib (Password Hashing)"),
        ("jose", "Python-JOSE (JWT)"),
        ("cryptography", "Cryptography"),
        
        # Google Cloud
        ("google.cloud.compute_v1", "Google Cloud Compute"),
        ("google.cloud.storage", "Google Cloud Storage"),
        ("google.cloud.monitoring_v3", "Google Cloud Monitoring"),
        ("google.cloud.recommender_v1", "Google Cloud Recommender"),
        
        # Google AI
        ("google.generativeai", "Google Generative AI (Gemini)"),
        
        # Utilities
        ("dotenv", "Python-dotenv"),
        ("httpx", "HTTPX"),
    ]
    
    results = []
    for module, name in dependencies:
        results.append(check_import(module, name))
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    installed = sum(results)
    total = len(results)
    
    print(f"Installed: {installed}/{total}")
    
    if installed == total:
        print("\n🎉 ALL DEPENDENCIES INSTALLED!")
        print("✅ You're ready to run the application!")
        return 0
    else:
        print(f"\n❌ MISSING {total - installed} DEPENDENCIES")
        print("\nTo install missing dependencies, run:")
        print("  pip3 install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())