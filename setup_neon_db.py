#!/usr/bin/env python
"""
Helper script to initialize and migrate the Neon PostgreSQL database.
Usage:
    python setup_neon_db.py
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ensure production or development settings point to Neon DB
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings.production')

# Load .env if present
env_file = BASE_DIR / '.env'
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        pass

def main():
    print("=" * 60)
    print("🚀 Initializing Neon PostgreSQL Database for Vercel")
    print("=" * 60)

    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ ERROR: DATABASE_URL is not set in environment or .env file!")
        sys.exit(1)

    # Mask credentials in output for security
    masked_url = db_url.split('@')[-1] if '@' in db_url else 'configured'
    print(f"📡 Target Database: ...@{masked_url}")

    import django
    django.setup()
    from django.core.management import call_command

    print("\n📦 Step 1: Applying Database Migrations...")
    try:
        call_command('migrate', interactive=False)
        print("✅ Migrations applied successfully.")
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        sys.exit(1)

    print("\n🌱 Step 2: Seeding Initial Portfolio Data...")
    try:
        if (BASE_DIR / 'initial_data.json').exists():
            call_command('loaddata', 'initial_data.json')
            print("✅ Initial data loaded from initial_data.json.")
        else:
            from seed_data import seed
            seed()
            print("✅ Initial data seeded via seed_data.py.")
    except Exception as e:
        print(f"⚠️ Note during data loading: {e}")
        try:
            from seed_data import seed
            seed()
            print("✅ Re-seeded data directly via models.")
        except Exception as seed_err:
            print(f"❌ Seeding error: {seed_err}")

    print("\n✨ Database setup complete! Your Neon PostgreSQL DB is ready for Vercel.")
    print("=" * 60)

if __name__ == '__main__':
    main()
