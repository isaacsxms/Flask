from flask import Flask
from routes import main
from models import db, Producto

app = Flask(__name__)

app.config.from_object("config.DevConfig")

app.register_blueprint(main)

db.init_app(app)

# Create the database tables (if not already created)
with app.app_context():
    db.create_all()

    # Function to insert products if they don't exist
    def insert_product(name, stock, price):
        existing_product = Producto.query.filter_by(name=name).first()
        if existing_product is None:
            new_product = Producto(name=name, stock=stock, price=price)
            db.session.add(new_product)
            db.session.commit()
            print(f"Product '{name}' with stock {stock} and price {price} added to the database.")
        else:
            print(f"Product '{name}' already exists in the database.")

    # List of products to insert
    products_to_insert = [
        {"name": "banana", "stock": 0, "price": 1},
        {"name": "mango", "stock": 0, "price": 2},
        {"name": "kiwi", "stock": 0, "price": 7},
        {"name": "naranja", "stock": 0, "price": 4},
        {"name": "maracuya", "stock": 0, "price": 8},
    ]

    # Insert products
    for product in products_to_insert:
        insert_product(product["name"], product["stock"], product["price"])
