from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from datetime import timedelta, datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import sqlite3
import random
import os
from dotenv import load_dotenv
from security import hash_password

app = Flask(__name__)
load_dotenv()
bcrypt = Bcrypt(app)

app.secret_key = os.getenv("SECRET_KEY")

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

app.permanent_session_lifetime = timedelta(minutes=10)

def generate_otp():
    return str(random.randint(100000, 999999))

# MAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)


# ================= HOME =================
@app.route('/home')
def home_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template(
        "home.html",
        products=products,
        username=session['username'],
        role=session.get('role')
    )


# ================= REGISTER (BỊ THIẾU TRƯỚC ĐÓ) =================

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "❌ Username đã tồn tại, chọn tên khác!"
        conn.close()
        hashed = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

        otp = generate_otp()

        # lưu tạm user + otp vào session
        session['otp'] = bcrypt.generate_password_hash(
            otp
        ).decode('utf-8')
        
        session['temp_user'] = {
            "username": username,
            "password": hashed,
            "email": email
        }

        # gửi email
        try:
            msg = Message(
                subject="OTP xác thực",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            msg.body = f"Mã OTP của bạn là: {otp}"
            mail.send(msg)

        except Exception as e:
            return f"Lỗi gửi mail: {str(e)}"

        # QUAN TRỌNG: chuyển sang verify
        return redirect(url_for('verify'))

    return render_template("register.html")


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():

    if request.method == 'POST':

        username = request.form['username']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return render_template(
                "login.html",
                error="❌ Tài khoản không tồn tại"
            )

        if user[4] == 1:
            return render_template(
                "login.html",
                error="🔒 Tài khoản đã bị khóa"
            )

        if bcrypt.check_password_hash(
            user[2],
            request.form['password']
        ):

            session.clear()

            session['username'] = username
            session['role'] = user[5]
            session.permanent = True

            return redirect(url_for('home_page'))

        return render_template(
            "login.html",
            error="❌ Sai mật khẩu"
        )

    return render_template("login.html")


# ================= ADMIN =================
@app.route('/admin/products')
def admin_products():

    if session.get('role') != 'admin':
        return "Không có quyền", 403

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template("admin_products.html", products=products)


# ================= ADD TO CART =================
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)

    return redirect(url_for('home_page'))


# ================= CART =================
@app.route('/cart')
def cart():

    cart_ids = session.get('cart', [])

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    products = []
    total = 0

    for pid in cart_ids:
        cursor.execute("SELECT * FROM products WHERE id=?", (pid,))
        item = cursor.fetchone()
        if item:
            products.append(item)
            total += item[2]

    conn.close()

    return render_template("cart.html", products=products, total=total)


# ================= INDEX =================
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home_page'))
    return redirect(url_for('login'))

@app.route('/verify', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def verify():

    if request.method == 'POST':

        user_otp = request.form['otp']
        otp = session.get('otp')
        user = session.get('temp_user')

        if not otp or not user:
            return "Session hết hạn"

        if not bcrypt.check_password_hash(
            session['otp'],
            user_otp
        ):
            return "Sai OTP"

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users(username, password, email, role, failed_attempts, locked)
            VALUES (?, ?, ?, ?, 0, 0)
        """, (user['username'], user['password'], user['email'], "user"))

        conn.commit()
        conn.close()

        session.clear()

        return redirect(url_for('login'))

    return render_template("verify.html")
@app.route('/admin')
def admin_home():
    return redirect(url_for('admin_products'))
@app.route('/dashboard')
def dashboard():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template(
        "dashboard.html",
        username=session['username'],
        role=session.get('role')
    )
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))
@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():

    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return "Bạn không có quyền truy cập!", 403

    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (name, price, description, image)
            VALUES (?, ?, ?, ?)
            """,
            (name, price, description, image)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('admin_products'))

    return render_template("add_product.html")
@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):

    if 'username' not in session:
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        return "Bạn không có quyền truy cập!", 403

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']

        cursor.execute(
            """
            UPDATE products
            SET name=?, price=?, description=?, image=?
            WHERE id=?
            """,
            (name, price, description, image, product_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('admin_products'))

    cursor.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    )

    product = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_product.html",
        product=product
    )
if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)