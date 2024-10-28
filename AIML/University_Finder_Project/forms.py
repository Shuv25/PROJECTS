from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange,EqualTo

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
    gre_score = FloatField('GRE Score', validators=[DataRequired(), NumberRange(min=0, max=340)])
    toefl_score = FloatField('TOEFL Score', validators=[DataRequired(), NumberRange(min=0, max=120)])
    university_rating = FloatField('University Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    sop = FloatField('Statement of Purpose (SOP)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    lor = FloatField('Letter of Recommendation (LOR)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    cgpa = FloatField('CGPA', validators=[DataRequired(), NumberRange(min=0, max=10)])
    research = SelectField('Research Experience', choices=[('0', 'No'), ('1', 'Yes')], validators=[DataRequired()])
    submit = SubmitField('Predict')
