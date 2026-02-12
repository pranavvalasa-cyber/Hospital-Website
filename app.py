from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import threading
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # In production, use environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), default='https://via.placeholder.com/150')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    problem = db.Column(db.String(500), nullable=False)
    token_number = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(20), default='Waiting') # Waiting, Consulted, Notified
    registration_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_paid = db.Column(db.Boolean, default=False)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) # In production, hash passwords!

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False) # Optional, strictly speaking feedback might be anon, but user said 'patients submit'
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    is_verified = db.Column(db.Boolean, default=True) # Staff can mark false to remove

# Global running token
current_token = 0

# Mock Notification System (Task running in background)
def check_notifications():
    while True:
        with app.app_context():
            # Logic to check wait times based on queue position
            # Since strict 'near hospital' requires GPS, we will simulate time-based logic
            # Assume 15 mins per patient consultant time
            waiting_patients = Patient.query.filter_by(status='Waiting').order_by(Patient.token_number).all()
            
            if waiting_patients:
                # Mock sending notifications logic here
                # e.g., print("Sending notification to " + patient.name)
                pass
        time.sleep(60)

# Only start the thread if we're not in reloader or if we are the reloader worker
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    notification_thread = threading.Thread(target=check_notifications)
    notification_thread.daemon = True
    notification_thread.start()

# Routes
@app.route('/')
def index():
    doctors = Doctor.query.all()
    # Get the current running token (the one being seen now)
    # If no one is seen, it might be 0 or the last one called.
    # User requirement: "current running token number".
    # We'll use a global variable or query the last 'Consulted' patient.
    last_consulted = Patient.query.filter_by(status='Consulted').order_by(Patient.id.desc()).first()
    display_token = last_consulted.token_number if last_consulted else 0
    
    # Calculate next token logic or just display
    
    return render_template('index.html', doctors=doctors, current_token=display_token)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact = request.form['contact']
        dob = request.form['dob']
        problem = request.form['problem']
        
        # Generate token
        last_patient = Patient.query.order_by(Patient.token_number.desc()).first()
        new_token = (last_patient.token_number + 1) if last_patient else 1
        
        new_patient = Patient(name=name, age=age, contact_number=contact, dob=dob, problem=problem, token_number=new_token)
        db.session.add(new_patient)
        db.session.commit()
        
        flash(f'Registration Successful! Your Token Number is {new_token}. Please wait for your turn.', 'success')
        return redirect(url_for('register'))
        
    return render_template('register.html')

@app.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        hospital_id = request.form['hospital_id']
        email = request.form['email']
        password = request.form['password']
        
        staff = Staff.query.filter_by(hospital_id=hospital_id, email=email, password=password).first()
        if staff:
            session['staff_id'] = staff.id
            return redirect(url_for('staff_dashboard'))
        else:
            flash('Invalid Credentials', 'danger')
            
    return render_template('staff_login.html')

@app.route('/staff/dashboard')
def staff_dashboard():
    if 'staff_id' not in session:
        return redirect(url_for('staff_login'))
    
    total_patients = Patient.query.count()
    paid_patients = Patient.query.filter_by(is_paid=True).count()
    waiting_patients = Patient.query.filter_by(status='Waiting').order_by(Patient.token_number).all()
    feedbacks = Feedback.query.filter_by(is_verified=True).all()
    
    return render_template('staff_dashboard.html', 
                           total=total_patients, 
                           paid=paid_patients, 
                           waiting_patients=waiting_patients,
                           feedbacks=feedbacks)

@app.route('/staff/call_next/<int:patient_id>')
def call_next(patient_id):
    if 'staff_id' not in session:
        return redirect(url_for('staff_login'))
        
    patient = Patient.query.get_or_404(patient_id)
    patient.status = 'Consulted'
    db.session.commit()
    flash(f'Called Patient Token {patient.token_number}', 'info')
    return redirect(url_for('staff_dashboard'))

@app.route('/staff/mark_paid/<int:patient_id>')
def mark_paid(patient_id):
    if 'staff_id' not in session:
        return redirect(url_for('staff_login'))
        
    patient = Patient.query.get_or_404(patient_id)
    patient.is_paid = True
    db.session.commit()
    return redirect(url_for('staff_dashboard'))
    
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        rating = request.form['rating']
        
        new_feedback = Feedback(patient_name=name, message=message, rating=rating)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))
        
    public_feedbacks = Feedback.query.filter_by(is_verified=True).all()
    return render_template('feedback.html', feedbacks=public_feedbacks)

@app.route('/staff/remove_feedback/<int:feedback_id>')
def remove_feedback(feedback_id):
    if 'staff_id' not in session:
        return redirect(url_for('staff_login'))
        
    feedback = Feedback.query.get_or_404(feedback_id)
    feedback.is_verified = False # Soft delete / hide
    db.session.commit()
    flash('Feedback removed.', 'warning')
    return redirect(url_for('staff_dashboard'))

@app.route('/logout')
def logout():
    session.pop('staff_id', None)
    return redirect(url_for('index'))

def init_db():
    with app.app_context():
        db.create_all()
        # Seed dummy data if empty
        if not Doctor.query.first():
            doctors = [
                Doctor(name="Dr. Aria Sterling", qualification="MD, Neurology", experience=12, specialization="Neurologist", image_url="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=300&h=300"),
                Doctor(name="Dr. Julian Vane", qualification="MBBS, Cardiology", experience=8, specialization="Cardiologist", image_url="https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=300&h=300"),
                Doctor(name="Dr. Elena Frost", qualification="MD, Pediatrics", experience=15, specialization="Pediatrician", image_url="https://images.unsplash.com/photo-1594824476967-48c8b964273f?auto=format&fit=crop&q=80&w=300&h=300")
            ]
            db.session.add_all(doctors)
            
            staff = Staff(hospital_id="HOSP001", email="admin@hospital.com", password="admin")
            db.session.add(staff)
            
            db.session.commit()

# Initialize database before the app starts
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
