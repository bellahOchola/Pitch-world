from . import db 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique = True, index= True)
    pass_secure= db.Column(db.String(255))
    pitch = db.relationship('Pitches',backref = 'user',lazy = "dynamic")
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password) 

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Pitches(db.Model):
    ___tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True)
    pitch_id = db.Column(db.Integer)
    pitch_title = db.Column(db.String)
    pitch_category = db.Column(db.String)
    pitch_content = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='user',lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls,id):
        pitch = Pitches.query.filter_by(pitch_id=id).all()
        return pitch


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    comment = db.Column(db.Text(),nullable = False)
    # pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'),nullable = False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()

        return comments

    
    def __repr__(self):
        return f'comment:{self.comment}'

class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote