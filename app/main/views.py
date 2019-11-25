from flask import render_template,request,redirect,url_for
from flask_login import login_required, current_user
from . import main
from .. import db
from .forms import PitchForm, CommentForm
from ..models import Pitches

@main.route('/')
def index():
    pitches = Pitches.query.all()
    promotion = Pitches.query.filter_by(pitch_category = 'Promotion').all() 
    pickup = Pitches.query.filter_by(pitch_category = 'Pickup-lines').all()
    product = Pitches.query.filter_by(pitch_category = 'Product').all()
    return render_template('index.html', promotion = promotion,pickup = pickup ,product = product, pitches = pitches)

    # return render_template('index.html')

@main.route('/pitch', methods = ['GET', 'POST'])
@login_required
def pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title= form.title.data
        category = form.category.data
        content = form.content.data

        new_pitch = Pitches(pitch_title=title,pitch_category= category, pitch_content= content, user= current_user)

        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    return render_template('pitch.html' ,pitch_form= form)

@main.route('/comments/<pitch_id>', methods = ['GET', 'POST'])
@login_required
def comment(pitch_id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.index'))
    return render_template('comment.html', comment_form =comment_form)

