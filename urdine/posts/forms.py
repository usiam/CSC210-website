from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    content = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Post')
