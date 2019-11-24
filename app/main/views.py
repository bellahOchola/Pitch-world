from flask import render_template,request,redirect,url_for
from flask_login import login_required, current_user
from . import main
from .. import db
from .forms import PitchForm
from ..models import Pitches

@main.route('/pitch' ,methods = ['GET', 'POST'])
@login_required
def pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title= form.title.data
        category = form.category.data
        content = form.content.data

        new_pitch = Pitches(pitch_id=pitch.id, pitch_title=title,pitch_category= category, pitch_content= content, user= current_user)

        new_pitch.save_pitch()

    return render_template('pitch.html' ,pitch_form= form)

@main.route('/')
def index():
    return render_template('index.html')