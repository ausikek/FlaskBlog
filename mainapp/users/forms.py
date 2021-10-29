from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (PasswordField, StringField, SubmitField,
                     ValidationError, BooleanField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user
from mainapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.')

    def validate_email(self, email):

        emailcopy = User.query.filter_by(email=email.data).first()
        if emailcopy:
            raise ValidationError('That email is taken.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken.')


class ReqResetEmail(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Email Reset')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That account does not exist')


class ReqResetPassword(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Request Password Reset')
