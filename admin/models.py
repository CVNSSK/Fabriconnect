from shop import db,app
from datetime import datetime


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180),unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    role = db.Column(db.String(10),unique=False, nullable=False)

    def __repr__(self):
        return '<Admins %r>' % self.username

with app.app_context():
    db.create_all()