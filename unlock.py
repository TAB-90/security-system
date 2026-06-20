import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE users
SET failed_attempts = 0,
    locked = 0
WHERE username = 'ecoapp'
""")

conn.commit()
conn.close()

print("Đã mở khóa ecoapp")