import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE username='ecoapp'")
cursor.execute("DELETE FROM users WHERE username='test1'")

conn.commit()
conn.close()

print("Đã xóa user")