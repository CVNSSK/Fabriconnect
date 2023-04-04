from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    colors = StringField('Colors', [validators.DataRequired()])
    discription = TextAreaField('Discription', [validators.DataRequired()])
    racklocation = TextAreaField('racklocation', [validators.DataRequired()])
    address = TextAreaField('shopaddress', [validators.DataRequired()])
    userId = IntegerField('user id', [validators.DataRequired()])
    image_1 = FileField('Image 1')
