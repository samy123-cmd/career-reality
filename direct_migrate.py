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
pg_conn.autocommit = False

def copy_table(table_name, columns, id_column='id'):
    """Copy data from SQLite to PostgreSQL"""
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Get data from SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    if not rows:
        print(f"  {table_name}: No data")
        return 0
    
    # Clear existing data in PostgreSQL
    pg_cursor.execute(f"DELETE FROM {table_name}")
    
    # Insert into PostgreSQL
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    
    for row in rows:
        values = [row[col] for col in columns]
        try:
            pg_cursor.execute(
                f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})",
                values
            )
        except Exception as e:
            print(f"  Error inserting into {table_name}: {e}")
            pg_conn.rollback()
            return 0
    
    # Reset sequence if there's an id column
    if id_column:
        try:
            pg_cursor.execute(f"SELECT setval('{table_name}_{id_column}_seq', (SELECT COALESCE(MAX({id_column}), 1) FROM {table_name}));")
        except:
            pass
    
    pg_conn.commit()
    print(f"  {table_name}: {len(rows)} rows copied")
    return len(rows)

print("\nCopying data...")

# Copy tables in order (respecting foreign keys)
tables = [
    ('django_site', ['id', 'domain', 'name']),
    ('auth_user', ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']),
    ('content_author', ['id', 'name', 'email', 'bio', 'profile_image', 'role', 'linkedin_url', 'twitter_url', 'is_active', 'created_at', 'updated_at']),
    ('content_category', ['id', 'name', 'slug', 'description', 'order']),
    ('content_article', ['id', 'title', 'slug', 'excerpt', 'content', 'category_id', 'author_id', 'featured_image', 'is_featured', 'is_published', 'meta_title', 'meta_description', 'published_date', 'created_at', 'updated_at', 'reading_time_minutes', 'tldr', 'editorial_context']),
]

total = 0
for table_name, columns in tables:
    try:
        count = copy_table(table_name, columns)
        total += count
    except Exception as e:
        print(f"  Error with {table_name}: {e}")

print(f"\nTotal: {total} rows copied")

# Cleanup
sqlite_conn.close()
pg_conn.close()

print("\nDone! Refresh the website to see your content.")
