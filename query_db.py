import sqlite3

conn = sqlite3.connect('billing.db')
cursor = conn.cursor()

# Query all tables
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("📊 Tables:", [t[0] for t in tables])
print()

# Query each table
for table in tables:
    table_name = table[0]
    print(f"=== {table_name.upper()} ===")
    rows = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("(empty)")
    print()

conn.close()
