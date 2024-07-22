from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import re  # Ensure the re module is imported
import uuid

app = Flask(__name__)
app.secret_key = '5022'  # Replace with your Flask secret key

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  # Replace with your MySQL root password
    database="society_management"
)

cursor = db.cursor()

# Ensure default facilities exist
default_facilities = ['Gym', 'Swimming Pool', 'Tennis Court', 'Conference Room']
for facility in default_facilities:
    cursor.execute("SELECT * FROM facilities WHERE name=%s", (facility,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO facilities (name, available) VALUES (%s, True)", (facility,))
db.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if user_type == 'user':
            cursor.execute("SELECT id, name, password, member_id FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            cursor.fetchall()  # Ensure all results are read
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                session['member_id'] = user[3]
                flash(f'Welcome, {user[1]}!', 'success')
                return redirect(url_for('home'))
        elif user_type == 'admin':
            cursor.execute("SELECT id, name, password FROM admins WHERE email=%s", (email,))
            admin = cursor.fetchone()
            cursor.fetchall()  # Ensure all results are read
            if admin and check_password_hash(admin[2], password):
                session['admin_id'] = admin[0]
                session['admin_name'] = admin[1]
                flash(f'Welcome, {admin[1]}!', 'success')
                return redirect(url_for('home'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check for existing users and admins with the same email
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()
        cursor.fetchall()  # Ensure all results are read

        cursor.execute("SELECT id FROM admins WHERE email=%s", (email,))
        existing_admin = cursor.fetchone()
        cursor.fetchall()  # Ensure all results are read
        
        if existing_user or existing_admin:
            flash('Email already registered. Please use a different email.', 'error')
        elif len(phone) < 10:
            flash('Phone number must be at least 10 digits long.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif not re.search(r'^(?=.*[a-zA-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).{6,}$', password):
            flash('Password must be at least 6 characters long and contain both letters and symbols.', 'error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
            db.commit()
            member_id = cursor.lastrowid
            cursor.execute("INSERT INTO users (name, email, phone, password, member_id) VALUES (%s, %s, %s, %s, %s)",
                           (name, email, phone, hashed_password, member_id))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('member_id', None)
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cursor.execute("SELECT id FROM members WHERE email=%s", (email,))
        existing_member = cursor.fetchone()
        cursor.fetchall()  # Ensure all results are read
        
        if existing_member:
            flash('Email already registered. Please use a different email.', 'error')
        else:
            cursor.execute("INSERT INTO members (name, email, phone, address) VALUES (%s, %s, %s, %s)", (name, email, phone, address))
            db.commit()
            member_id = cursor.lastrowid
            flash(f'Registration successful! Your Member ID is {member_id}', 'success')
            return redirect(url_for('success', member_id=member_id))
    return render_template('register.html')

@app.route('/success/<int:member_id>')
def success(member_id):
    return render_template('success.html', member_id=member_id)

@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if 'user_id' not in session:
        flash('Please log in to lodge a complaint.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        member_id = session['member_id']
        
        # Check if member_id exists in the members table
        cursor.execute("SELECT id FROM members WHERE id = %s", (member_id,))
        member_exists = cursor.fetchone()
        if not member_exists:
            flash('Member ID does not exist. Please contact support.', 'error')
            return redirect(url_for('complaints'))

        description = request.form['description']
        cursor.execute("INSERT INTO complaints (member_id, description, status) VALUES (%s, %s, %s)", (member_id, description, 'Pending'))
        db.commit()
        flash('Complaint lodged successfully!', 'success')
        return render_template('complaints.html', success=True)
    
    return render_template('complaints.html', success=False)

@app.route('/facilities', methods=['GET', 'POST'])
def facilities():
    if 'user_id' not in session:
        flash('Please log in to book a facility.', 'error')
        return redirect(url_for('login'))
    
    cursor.execute("SELECT * FROM facilities WHERE available = TRUE")
    available_facilities = cursor.fetchall()  # Fetch all results
    
    if request.method == 'POST':
        member_id = session['member_id']
        facility_id = request.form['facility_id']
        date = request.form['date']

        cursor.execute("INSERT INTO bookings (member_id, facility_id, date, status) VALUES (%s, %s, %s, %s)",
                       (member_id, facility_id, date, 'Pending'))
        db.commit()
        flash('Facility booked successfully!', 'success')
        return render_template('facilities.html', facilities=available_facilities, success=True)
    
    return render_template('facilities.html', facilities=available_facilities, success=False)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'error')
        return redirect(url_for('login'))
    
    member_id = session['member_id']
    
    # Fetch user complaints
    cursor.execute("SELECT id, description, status, response_reason FROM complaints WHERE member_id = %s", (member_id,))
    user_complaints = cursor.fetchall()  # Fetch all results
    
    # Fetch user booked facilities
    cursor.execute("SELECT facilities.name, bookings.date, bookings.status, bookings.response_reason FROM bookings JOIN facilities ON bookings.facility_id = facilities.id WHERE bookings.member_id = %s", (member_id,))
    user_bookings = cursor.fetchall()  # Fetch all results
    
    return render_template('dashboard.html', complaints=user_complaints, bookings=user_bookings)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please log in as an admin to access the admin dashboard.', 'error')
        return redirect(url_for('login'))
    
    # Fetch all complaints
    cursor.execute("SELECT id, member_id, description, status FROM complaints")
    all_complaints = cursor.fetchall()  # Fetch all results
    
    # Fetch all bookings
    cursor.execute("SELECT bookings.id, bookings.member_id, facilities.name, bookings.date, bookings.status FROM bookings JOIN facilities ON bookings.facility_id = facilities.id")
    all_bookings = cursor.fetchall()  # Fetch all results
    
    return render_template('admin_dashboard.html', complaints=all_complaints, bookings=all_bookings)

@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    # Use a secret key for secure access
    secret_key = request.args.get('key')
    if secret_key != '5022':  # Replace with your actual secret key
        abort(403)  # Forbidden access if the key is incorrect
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check for existing users and admins with the same email
        cursor.execute("SELECT id FROM admins WHERE email=%s", (email,))
        existing_admin = cursor.fetchone()
        cursor.fetchall()  # Ensure all results are read

        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()
        cursor.fetchall()  # Ensure all results are read
        
        if existing_admin or existing_user:
            flash('Email already registered. Please use a different email.', 'error')
        elif len(phone) < 10:
            flash('Phone number must be at least 10 digits long.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif not re.search(r'^(?=.*[a-zA-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).{6,}$', password):
            flash('Password must be at least 6 characters long and contain both letters and symbols.', 'error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO admins (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                           (name, email, phone, hashed_password))
            db.commit()
            flash('Admin registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('admin_signup.html', key=request.args.get('key'))

@app.route('/update_complaint_status/<int:complaint_id>', methods=['POST'])
def update_complaint_status(complaint_id):
    if 'admin_id' not in session:
        abort(403)  # Forbidden access if not logged in as admin
    
    status = request.form['status']
    reason = request.form['reason']
    
    cursor.execute("UPDATE complaints SET status=%s, response_reason=%s WHERE id=%s", (status, reason, complaint_id))
    db.commit()
    
    flash(f'Complaint ID {complaint_id} status updated to {status}.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/update_booking_status/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):
    if 'admin_id' not in session:
        abort(403)  # Forbidden access if not logged in as admin
    
    status = request.form['status']
    reason = request.form['reason']
    
    cursor.execute("UPDATE bookings SET status=%s, response_reason=%s WHERE id=%s", (status, reason, booking_id))
    db.commit()
    
    flash(f'Booking ID {booking_id} status updated to {status}.', 'success')
    return redirect(url_for('admin_dashboard'))

# New route to view user details
@app.route('/admin/user_details')
def user_details():
    if 'admin_id' not in session:
        abort(403)  # Forbidden access if not logged in as admin
    
    cursor.execute("SELECT id, name, email, phone, member_id FROM users")
    users = cursor.fetchall()
    
    return render_template('user_details.html', users=users)

# New routes to clear data
@app.route('/clear_users', methods=['POST'])
def clear_users():
    if 'admin_id' not in session:
        abort(403)  # Forbidden access if not logged in as admin
    
    cursor.execute("DELETE FROM bookings")
    cursor.execute("DELETE FROM complaints")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM members")
    cursor.execute("ALTER TABLE members AUTO_INCREMENT = 1")
    db.commit()
    
    flash('All user and member data cleared.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/clear_complaints', methods=['POST'])
def clear_complaints():
    if 'admin_id' not in session:
        abort(403)  # Forbidden access if not logged in as admin
    
    cursor.execute("DELETE FROM complaints")
    db.commit()
    
    flash('All complaints cleared.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/clear_bookings', methods=['POST'])
def clear_bookings():
    if 'admin_id' not in session:
        abort(403)  # Forbidden access if not logged in as admin
    
    cursor.execute("DELETE FROM bookings")
    db.commit()
    
    flash('All bookings cleared.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    cursor.execute("SELECT name, email, phone FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        if password:
            hashed_password = generate_password_hash(password)
            cursor.execute("UPDATE users SET name=%s, email=%s, phone=%s, password=%s WHERE id=%s", 
                           (name, email, phone, hashed_password, user_id))
        else:
            cursor.execute("UPDATE users SET name=%s, email=%s, phone=%s WHERE id=%s", 
                           (name, email, phone, user_id))
        db.commit()
        
        # Update the session variable with the new name
        session['user_name'] = name
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)


@app.route('/clear_all_data', methods=['POST'])
def clear_all_data():
    if 'admin_id' not in session:
        abort(403)  # Forbidden access if not logged in as admin
    
    cursor.execute("DELETE FROM bookings")
    cursor.execute("DELETE FROM complaints")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM members")

    cursor.execute("ALTER TABLE members AUTO_INCREMENT = 1")
    db.commit()
    
    flash('All data cleared.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
