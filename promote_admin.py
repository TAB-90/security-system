import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

username = "tan"

cursor.execute(
    "UPDATE users SET role='admin' WHERE username=?",
    (username,)
)

conn.commit()
conn.close()

print("Đã cấp quyền admin")