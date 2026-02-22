import os
import psycopg2


def main() -> int:
    url = os.getenv("SUPABASE_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not url:
        print("Missing SUPABASE_DATABASE_URL (or DATABASE_URL).")
        print("Set it and re-run this script.")
        return 1

    print("Testing database connection...")
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT current_database(), current_user, version();")
        db, user, version = cur.fetchone()
        print(f"Connected to: {db} as {user}")
        print(f"PostgreSQL version: {version[:50]}...")

        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
        )
        tables = cur.fetchall()
        print(f"Found {len(tables)} tables in public schema.")

        cur.close()
        conn.close()
        print("Connection test PASSED!")
        return 0
    except Exception as exc:
        print(f"Connection FAILED: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
