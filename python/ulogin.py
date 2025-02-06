# views.py
from flask import Blueprint, render_template, request, redirect, session
import mysql.connector

views_bp = Blueprint('ulogin', __name__)

# MySQL Configuration (Move this to a separate file if needed)
# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="user_db"
)
cursor = db.cursor()

@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['username'] = user[1]  # Assuming username is the second column
            return redirect('/dashboard')
        else:
            return "Invalid email or password. <a href='/login'>Try again</a>"
    return render_template('login.html')

@views_bp.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect('/login')
