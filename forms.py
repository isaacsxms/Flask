from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class PurchaseForm(FlaskForm):
    producto = SelectMultipleField('Producto', choices=["banana", "mango", "naranja", "maracuya", "kiwi"])

class AddProductForm(FlaskForm):
    producto = SelectMultipleField('Producto', choices=["banana", "mango", "naranja", "maracuya", "kiwi"])
    # Crear la relacion entre mis choices y los datos en la tabla productos

