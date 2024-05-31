from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class PurchaseForm(FlaskForm):
    producto = SelectMultipleField('Producto', choices=["banana", "mango", "naranja", "maracuya", "kiwi"])

class AddProductForm(FlaskForm):
    producto = SelectMultipleField('Producto', choices=["banana", "mango", "naranja", "maracuya", "kiwi"])

class CreateProductForm(FlaskForm):
    name = StringField('Nombre del producto', validators=[DataRequired()])
    price = IntegerField('Precio', validators=[DataRequired()])