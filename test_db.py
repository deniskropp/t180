import mysql.connector

config = {
    'host': '127.0.0.1',
    'port': 4448,
    'user': 'root',
    'password': '',
    'database': 'db'
}

try:
    conn = mysql.connector.connect(**config)
    print("Connected successfully")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    for (table,) in cursor:
        print(f"Table: {table}")
    
    cursor.execute("SELECT * FROM main LIMIT 1")
    rows = cursor.fetchall()
    print(f"Rows in main: {len(rows)}")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
