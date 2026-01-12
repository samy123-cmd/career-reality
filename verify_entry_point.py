
import os
import sys
import django

# Add current directory to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import api.index...")
    from api.index import app
    print("SUCCESS: api.index.app imported successfully.")
    print("This confirms Django is correctly initialized via the Vercel entry point.")
except Exception as e:
    print(f"FAILED: {e}")
