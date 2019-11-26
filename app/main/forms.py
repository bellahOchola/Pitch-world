from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SelectField, SubmitField
from wtforms.validators import Required

class PitchForm(FlaskForm):
    category = SelectField('Category', choices=[('Pickup_lines','Pickup_lines'),('Product','Product'),('Promotion','Promotion')],validators=[Required()])
    title = StringField('Pitch title',validators=[Required()])
    content = TextAreaField('Pitch content', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    title = StringField('title',validators=[Required()])
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')