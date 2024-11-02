import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SignupForm, LoginForm, PredictionForm
from dotenv import load_dotenv
import joblib  
import pymysql

load_dotenv()
pymysql.install_as_MySQLdb()

app = Flask(__name__)
__tablename__ = 'users' 
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class User(db.Model):
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
    if form.validate_on_submit():
        prediction = predict_admission(
            form.gre_score.data, 
            form.toefl_score.data, 
            form.university_rating.data,
            form.sop.data, 
            form.lor.data, 
            form.cgpa.data, 
            form.research.data
        )
        return render_template('prediction.html', form=form, prediction=prediction)

    return render_template('prediction.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


def predict_admission(gre, toefl, rating, sop, lor, cgpa, research):
    
    gre = float(gre)
    toefl = float(toefl)
    rating = int(rating)
    sop = float(sop)
    lor = float(lor)
    cgpa = float(cgpa)
    research = 1 if research == 'Yes' else 0 

    input_data = pd.DataFrame({
        'GRE Score': [gre],
        'TOEFL Score': [toefl],
        'University Rating': [rating],
        'SOP': [sop],
        'LOR ': [lor], 
        'CGPA': [cgpa],
        'Research': [research]  
    })

    try:
        prediction = model.predict(input_data)
        return f"Predicted chance of getting admission: {prediction[0] * 100:.2f}%"
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error in prediction. Please try again."

if __name__ == '__main__':
    app.run(debug=True)  
