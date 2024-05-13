from flask_wtf import FlaskForm
from wtforms import validators, StringField

class PostForm(FlaskForm):
    title = StringField("Title", [
        validators.DataRequired(),
        validators.Length(min=4, max=200)
        ])
    
