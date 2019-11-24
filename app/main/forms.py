from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

class PitchForm(FlaskForm):
    category = StringField('Pitch category',validators=[Required()])
    title = StringField('Pitch title',validators=[Required()])
    pitch = TextAreaField('Pitch content', validators=[Required()])
    submit = SubmitField('Submit')