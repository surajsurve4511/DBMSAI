# check_setup.py
# Quick system check to verify installation

import sys

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'flask',
        'mysql.connector',
        'pandas',
        'numpy',
        'sklearn',
        'plotly'
    ]
    
    print("=" * 60)
    print("MediCare HMS - System Check")
    print("=" * 60)
    print("\nChecking Python version...")
    print(f"Python {sys.version}")
    
    print("\nChecking required packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"✓ {package:<20} - Installed")
        except ImportError:
            print(f"✗ {package:<20} - Missing")
            missing_packages.append(package)
    
    print("\n" + "=" * 60)
    
    if missing_packages:
        print("❌ Missing packages detected!")
        print("Please run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All packages installed successfully!")
        return True

def check_database():
    """Check database connection"""
    print("\nChecking database connection...")
    try:
        import mysql.connector
        from config import Config
        
        conn = mysql.connector.connect(**Config.DB_CONFIG)
        if conn.is_connected():
            print("✓ Database connection - OK")
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✓ Found {len(tables)} tables in database")
            cursor.close()
            conn.close()
            return True
        else:
            print("✗ Database connection - Failed")
            return False
    except Exception as e:
        print(f"✗ Database error: {str(e)}")
        print("\nPlease ensure:")
        print("  1. MySQL server is running")
        print("  2. 'hospital' database exists")
        print("  3. Credentials in config.py are correct")
        return False

def check_files():
    """Check if all required files exist"""
    import os
    
    print("\nChecking project files...")
    
    required_files = [
        'app.py',
        'config.py',
        'database.py',
        'ai_features.py',
        'requirements.txt',
        'templates/base.html',
        'templates/dashboard.html',
        'static/css/style.css',
        'static/js/script.js'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - Missing")
            missing_files.append(file)
    
    if missing_files:
        print("\n❌ Some files are missing!")
        return False
    else:
        print("\n✅ All files present!")
        return True

def main():
    """Main check function"""
    deps_ok = check_dependencies()
    files_ok = check_files()
    db_ok = check_database()
    
    print("\n" + "=" * 60)
    print("SYSTEM CHECK SUMMARY")
    print("=" * 60)
    print(f"Dependencies: {'✅ OK' if deps_ok else '❌ Failed'}")
    print(f"Project Files: {'✅ OK' if files_ok else '❌ Failed'}")
    print(f"Database: {'✅ OK' if db_ok else '❌ Failed'}")
    print("=" * 60)
    
    if deps_ok and files_ok and db_ok:
        print("\n🎉 System is ready to run!")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")
    else:
        print("\n⚠️  Please fix the issues above before running the application.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
