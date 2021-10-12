from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])  # 'Username' is the label for the form
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Sign up')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    # image = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'png'])])
    submit = SubmitField('Update')


class Comment(FlaskForm):
    rating = RadioField('Rating', choices=[(1, '1 star'), (2, '2 star'), (3, '3 star'), (4, '4 star'), (5, '5 star')])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')
