from functools import wraps
from flask import session, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'username' not in session:
            return redirect(url_for('login'))

        if session.get('role') != 'admin':
            return "Bạn không có quyền truy cập!", 403

        return f(*args, **kwargs)

    return decorated_function