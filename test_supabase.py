import os
import psycopg2

# Test direct connection to Supabase
url = "postgresql://postgres.iakuzoeqdjkutpgettlx:vTo8B7KGQmoa4PqK@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

print(f"Testing connection to: {url[:50]}...")

try:
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    
    # Check which database we're connected to
    cur.execute("SELECT current_database(), current_user, version();")
    db, user, version = cur.fetchone()
    print(f"Connected to: {db} as {user}")
    print(f"PostgreSQL version: {version[:50]}...")
    
    # List all tables in public schema
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    
    if tables:
        print(f"\nFound {len(tables)} tables:")
        for t in tables:
            print(f"  - {t[0]}")
    else:
        print("\nNo tables found in public schema!")
        print("Creating test table to verify write access...")
        cur.execute("CREATE TABLE IF NOT EXISTS test_connection (id serial PRIMARY KEY, created_at timestamp DEFAULT NOW());")
        conn.commit()
        print("Test table created successfully!")
        cur.execute("DROP TABLE test_connection;")
        conn.commit()
        print("Test table dropped.")
    
    cur.close()
    conn.close()
    print("\nConnection test PASSED!")
    
except Exception as e:
    print(f"Connection FAILED: {e}")
