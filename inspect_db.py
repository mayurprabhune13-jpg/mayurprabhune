import sqlite3

def list_tables():
    conn = sqlite3.connect('instance/app.db')
    cursor = conn.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    conn.close()
    print("Database tables:", tables)

if __name__ == '__main__':
    list_tables()