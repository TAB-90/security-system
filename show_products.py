import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM products")

for row in cursor.fetchall():
    print(row)

conn.close()