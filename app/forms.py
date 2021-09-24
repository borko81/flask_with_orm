from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class Validate:

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('Error with username!')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('Error with email!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm, Validate):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
