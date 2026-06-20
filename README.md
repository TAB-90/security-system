&#x20;Security System Flask



Giới thiệu



Security System Flask là dự án website bán hàng trực tuyến được xây dựng bằng Python Flask và SQLite. Hệ thống tập trung vào việc áp dụng các kỹ thuật bảo mật web cơ bản nhằm bảo vệ dữ liệu người dùng và tăng cường an toàn cho ứng dụng.



&#x20;Chức năng chính



Người dùng



\* Đăng ký tài khoản

\* Đăng nhập hệ thống

\* Xác thực OTP qua Gmail

\* Xem danh sách sản phẩm

\* Xem chi tiết sản phẩm

\* Thêm sản phẩm vào giỏ hàng

\* Quản lý phiên đăng nhập



&#x20;Quản trị viên (Admin)



\* Quản lý sản phẩm

\* Thêm sản phẩm mới

\* Chỉnh sửa sản phẩm

\* Xóa sản phẩm

\* Xem danh sách sản phẩm trong hệ thống



&#x20;Các biện pháp bảo mật



&#x20;Password Hashing



Mật khẩu người dùng được mã hóa bằng Flask-Bcrypt trước khi lưu vào cơ sở dữ liệu.



CSRF Protection



Sử dụng Flask-WTF để chống tấn công Cross Site Request Forgery (CSRF).



Rate Limiting



Sử dụng Flask-Limiter để giới hạn số lượng request nhằm giảm nguy cơ Brute Force Attack.



Session Security



\* SESSION\_COOKIE\_HTTPONLY

\* SESSION\_COOKIE\_SAMESITE

\* Giới hạn thời gian đăng nhập



&#x20;OTP Verification



Người dùng phải xác thực mã OTP gửi qua Gmail trước khi hoàn tất đăng ký.



Environment Variables



Các thông tin nhạy cảm như:



\* SECRET\_KEY

\* MAIL\_USERNAME

\* MAIL\_PASSWORD



được lưu trong file `.env` và không đưa lên GitHub.



Công nghệ sử dụng



\* Python 3

\* Flask

\* SQLite

\* Bootstrap 5

\* Flask-Bcrypt

\* Flask-Mail

\* Flask-WTF

\* Flask-Limiter

\* Python-Dotenv



&#x20;Cấu trúc dự án





security-system/

│

├── app.py

├── auth.py

├── security.py

├── requirements.txt

├── .env

├── .gitignore

│

├── static/

│   └── images/

│

├── templates/

│   ├── home.html

│   ├── login.html

│   ├── register.html

│   ├── verify.html

│   ├── cart.html

│   ├── admin\_dashboard.html

│   ├── admin\_products.html

│   └── add\_product.html

│

└── users.db



Cài đặt



1\. Clone project





git clone https://github.com/TAB-90/security-system.git

cd security-system

2\. Cài đặt thư viện





pip install -r requirements.txt

3\. Tạo file .env



SECRET\_KEY=your\_secret\_key



MAIL\_USERNAME=your\_email@gmail.com

MAIL\_PASSWORD=your\_app\_password



4\. Chạy ứng dụng



python app.py



Sau đó truy cập:

http://127.0.0.1:5000



Tác giả



Đinh Nhật Tân-23013018

Bùi Thị Hồng Tươi-23015124



Sinh viên Trường Đại học Phenikaa

Mục tiêu học tập



Dự án được thực hiện nhằm tìm hiểu và áp dụng:



\* Flask Framework

\* SQLite Database

\* Authentication \& Authorization

\* Email OTP Verification

\* Web Security

\* Git \& GitHub

\* Quản lý dự án phần mềm



