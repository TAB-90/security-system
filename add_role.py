import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'"
    )
    conn.commit()
    print("Đã thêm cột role")
except:
    print("Cột role đã tồn tại")

conn.close()