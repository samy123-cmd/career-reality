import os
import sqlite3
import psycopg2

# Source: Local SQLite
sqlite_path = 'db.sqlite3'

# Target: Supabase PostgreSQL
pg_url = 'postgresql://postgres.iakuzoeqdjkutpgettlx:<YOUR_SUPABASE_PASSWORD>@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres'

print("Connecting to databases...")

# Connect to SQLite
sqlite_conn = sqlite3.connect(sqlite_path)

# Connect to PostgreSQL
pg_conn = psycopg2.connect(pg_url)
pg_cursor = pg_conn.cursor()

def convert_bool(val):
    """Convert SQLite 0/1 to PostgreSQL boolean"""
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    return bool(val)

print("\n1. Copying content_author...")
pg_cursor.execute("DELETE FROM content_author")
pg_conn.commit()

sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT * FROM content_author")
rows = sqlite_cursor.fetchall()
columns = [d[0] for d in sqlite_cursor.description]

for row in rows:
    data = dict(zip(columns, row))
    # Convert is_active to boolean
    data['is_active'] = convert_bool(data.get('is_active', True))
    
    cols = ', '.join([f'"{k}"' for k in data.keys()])
    placeholders = ', '.join(['%s'] * len(data))
    
    try:
        pg_cursor.execute(f"INSERT INTO content_author ({cols}) VALUES ({placeholders})", list(data.values()))
    except Exception as e:
        print(f"  Error: {e}")
        pg_conn.rollback()
        continue

pg_conn.commit()
print(f"  Copied {len(rows)} authors")

# Reset sequence
pg_cursor.execute("SELECT setval(pg_get_serial_sequence('content_author', 'id'), COALESCE(MAX(id), 1)) FROM content_author;")
pg_conn.commit()

print("\n2. Copying content_article...")
pg_cursor.execute("DELETE FROM content_article")
pg_conn.commit()

sqlite_cursor.execute("SELECT * FROM content_article")
rows = sqlite_cursor.fetchall()
columns = [d[0] for d in sqlite_cursor.description]

success = 0
for row in rows:
    data = dict(zip(columns, row))
    # Convert booleans
    for key in ['is_featured', 'is_published']:
        if key in data:
            data[key] = convert_bool(data.get(key, False))
    
    cols = ', '.join([f'"{k}"' for k in data.keys()])
    placeholders = ', '.join(['%s'] * len(data))
    
    try:
        pg_cursor.execute(f"INSERT INTO content_article ({cols}) VALUES ({placeholders})", list(data.values()))
        success += 1
    except Exception as e:
        print(f"  Error: {str(e)[:100]}")
        pg_conn.rollback()
        continue

pg_conn.commit()
print(f"  Copied {success}/{len(rows)} articles")

# Reset sequence
try:
    pg_cursor.execute("SELECT setval(pg_get_serial_sequence('content_article', 'id'), COALESCE(MAX(id), 1)) FROM content_article;")
    pg_conn.commit()
except:
    pass

# Verify
print("\nVerification:")
pg_cursor.execute("SELECT COUNT(*) FROM content_author")
print(f"  Authors: {pg_cursor.fetchone()[0]}")
pg_cursor.execute("SELECT COUNT(*) FROM content_category")
print(f"  Categories: {pg_cursor.fetchone()[0]}")
pg_cursor.execute("SELECT COUNT(*) FROM content_article")
print(f"  Articles: {pg_cursor.fetchone()[0]}")

sqlite_conn.close()
pg_conn.close()

print("\nDone! Refresh https://www.careerreality.in")
