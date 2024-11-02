from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=120)])
    submit = SubmitField('Login')

class PredictionForm(FlaskForm):
    person_age = FloatField('Age', validators=[DataRequired(), NumberRange(min=0)])
    person_income = FloatField('Annual Income', validators=[DataRequired(), NumberRange(min=0)])
    person_home_ownership = SelectField('Home Ownership', choices=[
        ('RENT', 'Rent'),
        ('OWN', 'Own'),
        ('MORTGAGE', 'Mortgage'),
        ('OTHER', 'Other')
    ], validators=[DataRequired()])
    person_emp_length = FloatField('Employment Length (in years)', validators=[DataRequired(), NumberRange(min=0)])
    loan_intent = SelectField('Loan Intent', choices=[
        ('PERSONAL', 'Personal'),
        ('EDUCATION', 'Education'),
        ('MEDICAL', 'Medical'),
        ('VENTURE', 'Venture'),
        ('HOMEIMPROVEMENT', 'Home Improvement'),
        ('DEBTCONSOLIDATION', 'Debt Consolidation')
    ], validators=[DataRequired()])
    loan_grade = SelectField('Loan Grade', choices=[
        ('D', 'D'),
        ('B', 'B'),
        ('C', 'C'),
        ('A', 'A'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G')
    ], validators=[DataRequired()])
    loan_amnt = FloatField('Loan Amount', validators=[DataRequired(), NumberRange(min=0)])
    loan_int_rate = FloatField('Interest Rate', validators=[DataRequired(), NumberRange(min=0)])
    loan_percent_income = FloatField('Percent of Income', validators=[DataRequired(), NumberRange(min=0, max=1)])
    cb_person_default_on_file = SelectField('Previous Default', choices=[
        ('Y', 'Yes'),
        ('N', 'No')
    ], validators=[DataRequired()])
    cb_person_cred_hist_length = FloatField('Credit History Length', validators=[DataRequired(), NumberRange(min=0)]) 
    submit = SubmitField('Predict')
