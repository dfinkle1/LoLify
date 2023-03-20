from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField

class SearchMatch(FlaskForm):
    """form to search for matches"""
    search = StringField('Username')