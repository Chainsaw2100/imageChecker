from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    data = db.Column(db.LargeBinary)
    size = db.Column(db.Integer)
    res_h = db.Column(db.Integer)
    res_w = db.Column(db.Integer)
    form = db.Column(db.String(10))
    date_orig = db.Column(db.String(50))
    user_orig = db.Column(db.String(50))
    date_dupl = db.Column(db.String(300))
    user_dupl = db.Column(db.String(300))


    def __init__(self, name, data, size, res_h, res_w, form, date_orig,user_orig, date_dupl, user_dupl):
        
        self.name = name
        self.data = data
        self.size = size
        self.res_h = res_h
        self.res_w = res_w
        self.form = form
        self.date_orig = date_orig
        self.user_orig =user_orig
        self.date_dupl = date_dupl
        self.user_dupl =user_dupl
        

    def __repr__(self):
        return {"Name": self.name, "Size": self.size, "Res_h": self.res_h, "Res_w": self.res_w, 
        "Form": self.form, "Date_orig": self.date_orig, "User_orig": self.user_orig, "Date_dupl": self.date_dupl, "User_dupl": self.user_dupl}