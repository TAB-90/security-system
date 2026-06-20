import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(
    "DELETE FROM users WHERE username='admin'"
)

cursor.execute(
    "DELETE FROM users WHERE username='tan'"
)

conn.commit()
conn.close()

print("Đã xóa admin cũ")