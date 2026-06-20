import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE role = ?", ("user",))

print("Số dòng bị xóa:", cursor.rowcount)

conn.commit()
conn.close()