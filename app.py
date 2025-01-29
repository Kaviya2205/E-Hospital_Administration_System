## 1️⃣ **app/__init__.py**

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import routes

## 2️⃣ **app/models.py**

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Admin, Doctor, Nurse, Patient

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(15), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Scheduled')

## 3️⃣ **app/routes.py**

from flask import request, jsonify
from flask_login import login_user, logout_user, login_required
from app import app, db
from app.models import User, Patient, Appointment

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        login_user(user)
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(name=data['name'], age=data['age'], gender=data['gender'], address=data['address'], contact=data['contact'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully'}), 201

@app.route('/appointments', methods=['POST'])
def schedule_appointment():
    data = request.json
    new_appointment = Appointment(patient_id=data['patient_id'], doctor=data['doctor'], date=data['date'], time=data['time'])
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment scheduled successfully'}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([{'id': a.id, 'patient_id': a.patient_id, 'doctor': a.doctor, 'date': a.date, 'time': a.time, 'status': a.status} for a in appointments])

