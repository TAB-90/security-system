import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN address TEXT")

conn.commit()
conn.close()

print("DONE - Added columns successfully")