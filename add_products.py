import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

products = [
    (
        "iPhone 15",
        20000000,
        "Điện thoại Apple mới nhất",
        "https://images.unsplash.com/photo-1695048133142-1a20484d2569"
    ),
    (
        "Laptop Gaming",
        25000000,
        "Laptop hiệu năng cao",
        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
    ),
    (
        "Tai nghe Bluetooth",
        1500000,
        "Âm thanh chất lượng cao",
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
    )
]

cursor.executemany(
    """
    INSERT INTO products(name,price,description,image)
    VALUES(?,?,?,?)
    """,
    products
)

conn.commit()
conn.close()

print("Đã thêm sản phẩm")