import sqlite3
import psycopg2
from psycopg2.extensions import adapt
import os
from urllib.parse import urlparse

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

def migrate_table(sqlite_cur, pg_cur, table):
    """Migrate a single table from SQLite to PostgreSQL"""
    print(f"\nMigrating {table} table...")
    
    # Get SQLite schema
    sqlite_cur.execute(f"PRAGMA table_info({table})")
    columns = sqlite_cur.fetchall()
    
    # Create PostgreSQL table
    pg_columns = []
    for col in columns:
        name, type_, notnull, dflt_value, pk = col[1], col[2], col[3], col[4], col[5]
        pg_type = 'TEXT' if 'TEXT' in type_.upper() else \
                 'INTEGER' if 'INT' in type_.upper() else \
                 'BOOLEAN' if 'BOOL' in type_.upper() else \
                 'TIMESTAMP' if 'DATE' in type_.upper() else 'TEXT'
        pg_columns.append(f"{name} {pg_type}{' PRIMARY KEY' if pk else ''}")
    
    pg_cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
    pg_cur.execute(f"CREATE TABLE {table} ({', '.join(pg_columns)})")
    
    # Migrate data
    sqlite_cur.execute(f"SELECT * FROM {table}")
    rows = sqlite_cur.fetchall()
    for row in rows:
        try:
            values = [adapt(x).getquoted().decode() if x is not None else 'NULL' for x in row]
            pg_cur.execute(f"INSERT INTO {table} VALUES ({', '.join(values)})")
        except Exception as e:
            print(f"Error migrating row {row} to {table}: {e}")
    print(f"Migrated {len(rows)} rows to {table}")

def main():
    # Connect to databases
    sqlite_conn = sqlite3.connect('instance/app.db')
    sqlite_cur = sqlite_conn.cursor()
    
    pg_conn = get_postgres_conn()
    pg_cur = pg_conn.cursor()
    
    # Migrate all tables except alembic_version
    tables = ['case_study', 'contact', 'testimonial', 'user', 'video', 'post']
    
    for table in tables:
        migrate_table(sqlite_cur, pg_cur, table)
    
    # Handle alembic_version separately
    print("\nHandling alembic_version table...")
    sqlite_cur.execute("SELECT version_num FROM alembic_version")
    version = sqlite_cur.fetchone()[0]
    pg_cur.execute("CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL)")
    pg_cur.execute("INSERT INTO alembic_version (version_num) VALUES (%s)", (version,))
    
    # Commit and close
    pg_conn.commit()
    sqlite_conn.close()
    pg_conn.close()
    print("\nDatabase migration completed successfully!")

if __name__ == '__main__':
    main()