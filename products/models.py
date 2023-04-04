from shop import db,app
from flask import current_app
from datetime import datetime
import os

class Addproduct(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    sdesl = db.Column(db.Text, nullable=False)
    saddress= db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    userId = db.Column(db.Integer,nullable=False)
    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    nparr= db.Column(db.String(150), nullable=False, default='image_1.npy')

    def __repr__(self):
        return '<Post %r>' % self.name


with app.app_context():
    db.create_all()