from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#class Post(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(80), unique=True, nullable=False)

class Albaran(db.Model):
    __tablename__ = 'albaran'
    id = db.Column(db.Integer, primary_key=True)
    proveedor = db.Column(db.String(50), nullable=False)
    producto = db.Column(db.String(50), nullable=False)
    removed = db.Column(db.Boolean, nullable=False) # Querys only to removed=False, if removed it should not be query'd

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Linea_Producto_Albaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_albaran = db.Column(db.Integer, db.ForeignKey('albaran.id'))
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))