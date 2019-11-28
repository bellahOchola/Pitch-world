from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required, current_user
from . import main
from .. import db
from .forms import PitchForm, CommentForm, UpdateProfile
from ..models import Pitches,Comment,User

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


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    pitch = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))