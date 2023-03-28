from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,PasswordField
from wtforms.validators import DataRequired,Email,Length

class SearchMatch(FlaskForm):
    """form to search for matches"""
    search = StringField('Summoners',validators=[DataRequired()])

class Register(FlaskForm):
    """Create a user account"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[Length(min=6)])
    email= StringField('E-mail',validators=[DataRequired(),Email()])
    summoner_name= StringField('Summoner Name')
    image_url = StringField('(Optional) Image Url')

class Login(FlaskForm):
    """Login to a user account"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[Length(min=6)])

class EditUser(FlaskForm):
    email= StringField('E-mail',validators=[DataRequired(),Email()])
    summoner = StringField('Summoner Name')
    image_url = StringField('Image Url (Optional)')
    bio = TextAreaField('Bio (Optional)')