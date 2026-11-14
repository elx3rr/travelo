"""
=============================================================================
TRAVELO - AUTOMATED MYSQL (XAMPP) DATABASE SETUP SCRIPT
=============================================================================
This script automatically:
1. Connects to your XAMPP MySQL server (localhost:3306).
2. Creates the 'travelo_db' database if it doesn't already exist.
3. Applies all Django database migrations.
4. Populates rich cultural information for Indian states & holiday packages.
5. Sets up an administrator account (admin / admin123).
=============================================================================
"""

import sys
import os
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def setup_mysql_database():
    print("\n========================================================")
    print("   [+] TRAVELO - MYSQL (XAMPP) AUTOMATED DATABASE SETUP   ")
    print("========================================================\n")

    # Step 1: Connect to MySQL server via PyMySQL
    try:
        import pymysql
    except ImportError:
        print("[!] PyMySQL is not installed. Installing pymysql globally...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql"])
        import pymysql

    mysql_host = "127.0.0.1"
    mysql_port = 3306
    mysql_user = "root"
    mysql_password = ""
    db_name = "travelo_db"

    print(f"[*] Step 1: Connecting to MySQL server at {mysql_host}:{mysql_port} (User: '{mysql_user}')...")

    try:
        conn = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            port=mysql_port,
            charset='utf8mb4'
        )
        print("[OK] Connected to MySQL successfully!")

        # Step 2: Create travelo_db if not exists
        with conn.cursor() as cursor:
            print(f"[*] Step 2: Ensuring database '{db_name}' exists...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"[OK] Database '{db_name}' is verified and ready in MySQL (XAMPP)!")
        conn.close()

    except Exception as e:
        print(f"\n[!] WARNING: Could not connect to MySQL server at {mysql_host}:{mysql_port}.")
        print(f"    Error details: {e}")
        print("\n    Please make sure MySQL is started in your XAMPP Control Panel.")
        print("    (Click 'Start' next to MySQL in XAMPP and run this script again.)\n")
        return False

    # Step 3: Run Django Migrations
    print("\n[*] Step 3: Running Django database migrations...")
    try:
        subprocess.check_call([sys.executable, "manage.py", "makemigrations"])
        subprocess.check_call([sys.executable, "manage.py", "migrate"])
        print("[OK] Migrations applied successfully to MySQL travelo_db!")
    except Exception as e:
        print(f"[!] Migration failed: {e}")
        return False

    # Step 4: Seed Initial Data
    print("\n[*] Step 4: Seeding Indian states culture & tour packages data...")
    try:
        subprocess.check_call([sys.executable, "manage.py", "seed_data"])
        print("[OK] Cultural records and tour packages seeded successfully!")
    except Exception as e:
        print(f"[!] Seeding warning: {e}")

    # Step 5: Create Superuser if needed
    print("\n[*] Step 5: Checking administrator account...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelo_project.settings')
        import django
        django.setup()
        from django.contrib.auth.models import User

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@travelo-india.com', 'admin123')
            print("[OK] Superuser created: Username: 'admin' | Password: 'admin123'")
        else:
            print("[OK] Superuser 'admin' already exists.")
    except Exception as e:
        print(f"[!] Superuser notice: {e}")

    print("\n========================================================")
    print("   SETUP COMPLETE! TRAVELO IS READY TO RUN!            ")
    print("========================================================")
    print("To start the Travelo website, simply run:")
    print("   python manage.py runserver\n")
    print("Then open your browser at: http://127.0.0.1:8000/")
    print("Admin portal:              http://127.0.0.1:8000/admin/")
    print("Central Image links:       http://127.0.0.1:8000/image-links/")
    print("========================================================\n")
    return True

if __name__ == '__main__':
    setup_mysql_database()
