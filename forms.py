from flask_wtf import FlaskForm
from wtforms import IntegerField, validators, StringField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class AddProductForm(FlaskForm):
    tomate_producto = StringField("tomateProducto", validators=[Length(min=1, max=50)])
    tomate_cantidad = IntegerField("tomateCantidad", validators=[NumberRange(min=1)])