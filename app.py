from flask import Flask
from routes import main
from models import db

# Creamos la app
app = Flask(__name__)

# Cargamos la configuración
app.config.from_object("config.DevConfig")

# Registramos la ruta
app.register_blueprint(main)

# Inicializamos el ORM
db.init_app(app)

# Creamos la bbdd (si no está creada)
with app.app_context():
    db.create_all()