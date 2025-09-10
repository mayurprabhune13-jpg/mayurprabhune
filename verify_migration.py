import os
from urllib.parse import urlparse
import psycopg2
import sqlite3

def get_postgres_conn():
    """Get PostgreSQL connection from Railway DATABASE_URL"""
    db_url = os.getenv('DATABASE_URL')
    result = urlparse(db_url)
    return psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

def get_sqlite_conn():
    """Get SQLite connection"""
    return sqlite3.connect('instance/app.db')

def verify_table(pg_cur, sqlite_cur, table):
    """Verify data for a single table"""
    print(f"\nVerifying {table}...")
    
    # Compare row counts
    pg_cur.execute(f"SELECT COUNT(*) FROM {table}")
    pg_count = pg_cur.fetchone()[0]
    
    sqlite_cur.execute(f"SELECT COUNT(*) FROM {table}")
    sqlite_count = sqlite_cur.fetchone()[0]
    
    print(f"PostgreSQL rows: {pg_count} | SQLite rows: {sqlite_count}")
    
    if pg_count != sqlite_count:
        print(f"⚠️ Row count mismatch for {table}")
        return False
    
    # Compare sample data
    pg_cur.execute(f"SELECT * FROM {table} LIMIT 1")
    pg_sample = pg_cur.fetchone()
    
    sqlite_cur.execute(f"SELECT * FROM {table} LIMIT 1")
    sqlite_sample = sqlite_cur.fetchone()
    
    print(f"PostgreSQL sample: {pg_sample}")
    print(f"SQLite sample: {sqlite_sample}")
    
    return True

def main():
    pg_conn = get_postgres_conn()
    pg_cur = pg_conn.cursor()
    
    sqlite_conn = get_sqlite_conn()
    sqlite_cur = sqlite_conn.cursor()
    
    tables = ['case_study', 'contact', 'testimonial', 'user', 'video', 'post']
    all_verified = True
    
    for table in tables:
        if not verify_table(pg_cur, sqlite_cur, table):
            all_verified = False
    
    # Verify alembic_version
    pg_cur.execute("SELECT version_num FROM alembic_version")
    pg_version = pg_cur.fetchone()[0]
    
    sqlite_cur.execute("SELECT version_num FROM alembic_version")
    sqlite_version = sqlite_cur.fetchone()[0]
    
    print(f"\nAlembic version - PostgreSQL: {pg_version} | SQLite: {sqlite_version}")
    
    if pg_version != sqlite_version:
        print("⚠️ Alembic version mismatch")
        all_verified = False
    
    pg_conn.close()
    sqlite_conn.close()
    
    if all_verified:
        print("\n✅ All tables verified successfully!")
    else:
        print("\n❌ Some tables have verification issues")

if __name__ == '__main__':
    main()