from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField

class HiddenForm(FlaskForm):
    article = HiddenField('Article')
    
    submit = SubmitField('Submit')