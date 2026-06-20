import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("UPDATE products SET image='iphone.jpg' WHERE id=1")
cursor.execute("UPDATE products SET image='laptop.jpg' WHERE id=2")
cursor.execute("UPDATE products SET image='headphone.jpg' WHERE id=3")

conn.commit()
conn.close()

print("Đã cập nhật ảnh")