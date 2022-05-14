from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    id = IntegerField('id')
    title = StringField('title')
    year = IntegerField('year')
    genre = StringField('genre')
    description = TextAreaField('description')
    watched = BooleanField('watched')