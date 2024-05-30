from flask_wtf import FlaskForm
from wtforms import SelectMultipleField

from flask_wtf import FlaskForm
from wtforms import SelectMultipleField

class PurchaseForm(FlaskForm):
    producto = SelectMultipleField('Producto', choices=["banana", "mango", "naranja", "maracuya", "kiwi"])

class AddProductForm(FlaskForm):
    producto = SelectMultipleField('Producto', choices=["banana", "mango", "naranja", "maracuya", "kiwi"])
