from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Albaran(db.Model):
    __tablename__ = 'albaran'
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(50), nullable=False)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Linea_Producto_Albaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_albaran = db.Column(db.Integer, db.ForeignKey('albaran.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))