import os
import logging
import pandas as pd
import numpy as np
from flask import Flask, render_template, redirect, session, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SignupForm, LoginForm, PredictionForm
from dotenv import load_dotenv
import joblib
import pymysql

load_dotenv()
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

def load_model():
    try:
        model = joblib.load("model.joblib")
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Failed to load model: {e}")
        return None
    
model = load_model()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(form.password.data) 
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = form.username.data
        return redirect(url_for('home'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/')
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = PredictionForm()
    prediction = None  # Initialize prediction variable to None

    if form.validate_on_submit():
        prediction = predict_loan_status(
            form.person_age.data,
            form.person_income.data,
            form.person_home_ownership.data,
            form.person_emp_length.data,
            form.loan_intent.data,
            form.loan_grade.data,
            form.loan_amnt.data,
            form.loan_int_rate.data,
            form.loan_percent_income.data,
            form.cb_person_default_on_file.data,
            form.cb_person_cred_hist_length.data  # Use the corrected form field
        )
        return render_template('prediction.html', form=form, prediction=prediction)

    return render_template('prediction.html', form=form, prediction=prediction)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def predict_loan_status(age, income, home_ownership, emp_length, loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_percent_income, default_on_file, cred_hist_length):
    # Ensure all inputs are valid and handle any potential NaN values
    try:
        age = int(age) if age else 0
        income = float(income) if income else 0.0
        emp_length = int(emp_length) if emp_length else 0
        loan_amnt = float(loan_amnt) if loan_amnt else 0.0
        loan_int_rate = float(loan_int_rate) if loan_int_rate else 0.0
        loan_percent_income = float(loan_percent_income) if loan_percent_income else 0.0
        cred_hist_length = int(cred_hist_length) if cred_hist_length else 0
        
        # Create DataFrame
        input_data = pd.DataFrame({
            'person_age': [age],
            'person_income': [income],
            'person_home_ownership': [home_ownership],
            'person_emp_length': [emp_length],
            'loan_intent': [loan_intent],
            'loan_grade': [loan_grade],
            'loan_amnt': [loan_amnt],
            'loan_int_rate': [loan_int_rate],
            'loan_percent_income': [loan_percent_income],
            'cb_person_default_on_file': [default_on_file],
            'cb_person_cred_hist_length': [cred_hist_length]
        })

        # Check for NaN values in input_data
        if input_data.isnull().values.any():
            raise ValueError("Input contains NaN values.")

        # Make prediction
        prediction = model.predict(input_data)
        return f"Predicted loan status: {'Default' if prediction[0] == 1 else 'Non-Default'}"
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error in prediction. Please try again."


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
