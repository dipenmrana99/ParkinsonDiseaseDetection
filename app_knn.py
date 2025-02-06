import os
import numpy as np
from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint, send_file
import pickle
import mysql.connector
import pycountry

knn = Blueprint('knn', __name__)

app = Flask(__name__)
app.secret_key = '\xb6skT\xf9\xe1\x98\xef\xd5\xb1q\xbb\xc9^\xac\x19:S\xde\r\\\xdc$L'
model = pickle.load(open('model_knn.pkl','rb'))
scaler = pickle.load(open('scaling.pkl','rb'))

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="user_db"
)
cursor = db.cursor()

# Define a route to handle tracking of user IP addresses
@app.route('/')
def track_ip():
    # Get the visitor's IP address
    ip_address = request.remote_addr
    
    # Insert the IP address into the database
    cursor.execute("INSERT INTO visitors (ip_address) VALUES (%s)", (ip_address,))
    db.commit()
    
    # Return a response
    return render_template('login.html')

# Routes
@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM admin_credentials WHERE email=%s AND password=%s", (email, password))
        admin = cursor.fetchone()
        if admin:
            session['admin'] = True
            track_ip()  # Track admin IP address
            return redirect('/admindashboard')
        else:
            return "Invalid email or password. <a href='/adminlogin'>Try again</a>"
    return render_template('adminlogin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect('/login')

@app.route('/admindashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/adminlogin')  # Redirect if not logged in as admin

    # Execute SQL query to count rows
    cursor.execute("SELECT COUNT(*) FROM visitors")
    result = cursor.fetchone()
    row_count = result[0] if result else 0

    # Execute SQL query to count comments
    cursor.execute("SELECT COUNT(*) FROM comments")
    comment_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM test_report")
    tested = cursor.fetchone()[0]

    # Fetch user details from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template('admindashboard.html', row_count=row_count, comment_count=comment_count, tested=tested, users=users)

@app.route('/report')
def report():
    try:
        # Execute the SQL query to fetch data from users and test_report tables
        cursor.execute("""
            SELECT users.id, users.username, test_report.MDVP_Fo_Hz, test_report.MDVP_Fhi_Hz, 
                   test_report.MDVP_Flo_Hz, test_report.MDVP_Jitter_percent, test_report.MDVP_Shimmer, 
                   test_report.NHR, test_report.RPDE, test_report.DFA, test_report.spread1, 
                   test_report.spread2, test_report.D2
            FROM users
            JOIN test_report ON users.id = test_report.id;
        """)
        
        # Fetch all rows returned by the query
        data = cursor.fetchall()
        print("Fetched data:", data)  # Print fetched data for debugging
        
        # Render the template with the fetched data
        return render_template('report.html', data=data)
    except Exception as e:
        return 'Error: ' + str(e)

# Route to handle like button click
@app.route('/like', methods=['POST'])
def like():
    try:
        # Execute SQL query to update like count in the database
        cursor.execute("UPDATE likes_dislikes SET likes = likes + 1 WHERE id = 1")
        db.commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# Route to handle dislike button click
@app.route('/dislike', methods=['POST'])
def dislike():
    try:
        # Execute SQL query to update dislike count in the database
        cursor.execute("UPDATE likes_dislikes SET dislikes = dislikes + 1 WHERE id = 1")
        db.commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    
# Route to handle form submission
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if request.method == 'POST':
        # Get comment data from the form
        comment = request.form['comment']

        # Store comment data in the database
        cursor.execute("INSERT INTO comments (comment) VALUES (%s)", (comment,))
        db.commit()

        return render_template('index.html')
    
# Function to insert data into MySQL database
def insert_data(name, email):
    try:
        conn = mysql.connector.connect
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

PDF_FOLDER = r"C:\Users\Dipen Rana\Documents\project\testD\pdfs"
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        username = request.form['username']
        pdf_file = os.path.join(PDF_FOLDER, f'{username}.pdf')
        if os.path.exists(pdf_file):
            return send_file(pdf_file, as_attachment=True)
        else:
            return 'PDF not found for this username.'
    return render_template('download.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if insert_data(name, email):
            return "Data submitted successfully!"
        else:
            return "An error occurred while submitting data."

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('admin', None)
    return redirect('/login')

def insert_data(data):
    try:
        # Execute SQL query to insert data
        query = "INSERT INTO test_report (MDVP_Fo_Hz, MDVP_Fhi_Hz, MDVP_Flo_Hz, MDVP_Jitter_percent, MDVP_Shimmer, NHR, RPDE, DFA, spread1, spread2, D2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)

        # Commit changes
        db.commit()

        return True
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Print error message
        return False
    
@app.route('/edit_admin')
def edit_admin():
    # Fetch admin details from database
    cursor.execute("SELECT * FROM admin_credentials WHERE id = 1")
    admin_details = cursor.fetchone()
    
    # Fetch all available countries
    countries = [country.name for country in pycountry.countries]
    
    return render_template('edit_admin.html', admin_details=admin_details, countries=countries)


@app.route('/save_admin_details', methods=['POST'])
def save_admin_details():
    name = request.form['name']
    gender = request.form['gender']
    country = request.form['country']
    address = request.form['address']
    phone = request.form['phone']
    
    # Update admin details in the database
    cursor.execute("UPDATE admin_credentials SET Name = %s, Gender = %s, Country = %s, Address = %s, Phone = %s WHERE id = 1",
                   (name, gender, country, address, phone))
    db.commit()
    
    return 'Admin details updated successfully!'


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Extract data from form
        mdvp_fo = request.form['MDVP:Fo(Hz)']
        mdvp_fhi = request.form['MDVP:Fhi(Hz)']
        mdvp_flo = request.form['MDVP:Flo(Hz)']
        mdvp_jitter = request.form['MDVP:Jitter(%)']
        mdvp_shimmer = request.form['MDVP:Shimmer']
        nhr = request.form['NHR']
        rpde = request.form['RPDE']
        dfa = request.form['DFA']
        spread1 = request.form['spread1']
        spread2 = request.form['spread2']
        d2 = request.form['D2']
        
        # Insert data into database
        data = (mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter, mdvp_shimmer, nhr, rpde, dfa, spread1, spread2, d2)
        if insert_data(data):
            # Predict diagnosis
            int_features = [float(x) for x in request.form.values()]
            final_features = [np.array(int_features)]
            final_features = scaler.transform(final_features)
            prediction = model.predict(final_features)
            
            # Determine output message based on prediction
            if prediction == [0]:
                output = "Parkinson's Disease Not Detected"
            elif prediction == [1]:
                output = "Parkinson's Disease Detected"
            
            return render_template('index.html', prediction_text='Diagnosis Result: {}'.format(output))
        else:
            return "An error occurred while submitting data."

if __name__ == '__main__':
    app.run(debug=True)
