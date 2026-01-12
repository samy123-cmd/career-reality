import os
import sqlite3
import psycopg2

# Source: Local SQLite
sqlite_path = 'db.sqlite3'

# Target: Supabase PostgreSQL
pg_url = 'postgresql://postgres.iakuzoeqdjkutpgettlx:vTo8B7KGQmoa4PqK@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres'

print("Connecting to databases...")

# Connect to SQLite
sqlite_conn = sqlite3.connect(sqlite_path)
sqlite_conn.row_factory = sqlite3.Row

# Connect to PostgreSQL
pg_conn = psycopg2.connect(pg_url)
pg_cursor = pg_conn.cursor()

def copy_table_smart(table_name):
    """Copy all columns from SQLite to PostgreSQL"""
    sqlite_cursor = sqlite_conn.cursor()
    
    # Get data from SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    if not rows:
        print(f"  {table_name}: No data")
        return 0
    
    # Get column names from SQLite
    columns = [description[0] for description in sqlite_cursor.description]
    
    # Clear existing data in PostgreSQL
    try:
        pg_cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE")
        pg_conn.commit()
    except Exception as e:
        pg_conn.rollback()
        try:
            pg_cursor.execute(f"DELETE FROM {table_name}")
            pg_conn.commit()
        except:
            pg_conn.rollback()
    
    # Insert into PostgreSQL
    columns_str = ', '.join([f'"{c}"' for c in columns])
    placeholders = ', '.join(['%s'] * len(columns))
    
    success = 0
    for row in rows:
        values = list(row)
        try:
            pg_cursor.execute(
                f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})',
                values
            )
            success += 1
        except Exception as e:
            pg_conn.rollback()
            print(f"    Skip row: {str(e)[:80]}")
    
    pg_conn.commit()
    
    # Reset sequence
    try:
        pg_cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), COALESCE(MAX(id), 1)) FROM {table_name};")
        pg_conn.commit()
    except:
        pg_conn.rollback()
    
    print(f"  {table_name}: {success}/{len(rows)} rows copied")
    return success

print("\nCopying data in order...")

# Order matters due to foreign keys
tables_in_order = [
    'django_site',
    'content_category',
    'content_author',
    'content_article',
]

total = 0
for table in tables_in_order:
    try:
        count = copy_table_smart(table)
        total += count
    except Exception as e:
        print(f"  Error with {table}: {e}")

print(f"\nTotal: {total} rows copied")

# Cleanup
sqlite_conn.close()
pg_conn.close()

print("\nDone! Refresh https://www.careerreality.in to see your content.")
