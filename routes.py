from flask import Blueprint, redirect, render_template, request, url_for
from models import  Producto, Albaran, db, Linea_Producto_Albaran, Factura, Factura_Producto
from forms import AddProductForm, PurchaseForm

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/adios")
def adios():
    return "adios"

@main.route("/producto/<int:producto_id>")
def producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return render_template("producto.html", producto=producto)

@main.route("/productos") # por defecto es GET
def productos():
    productos = Producto.query.all()    
    return render_template("productos.html", productos=productos)

""" @main.route("/albaran", methods=['GET', 'POST'])
def add_stock():
    print("Inside albaran")
    form = AddProductForm()
    if request.method == "POST" and form.validate():
        for product in form:
            product_id = int(product.name)
            quantity = int(request.form.get(product.name))
            if quantity > 0:
                # Find the product by its ID
                product = Producto.query.get_or_404(product_id)
                # Update the stock quantity
                product.stock += quantity
                # Commit the changes to the database
                db.session.commit()
        return redirect(url_for('main.productos'))
    # If the form is not submitted or is invalid, render the template with the form
    products = Producto.query.all()
    return render_template("albaran.html", form=form, products=products) """

@main.route("/albaran", methods=['GET', 'POST'])
def add_stock():
    form = AddProductForm()
    data = {}
    for key, value in request.form.items():
        if key != 'csrf_token':
            data[int(key)] = int(value)

    print(data)

    productos = Producto.query.all()
    print(form.producto.data)

    if request.method == "POST" and form.validate():
        print("Passed validation")
        
        albaran = Albaran()
        db.session.add(albaran)
        db.session.commit()

        for producto in productos:
            if producto.id in data:
                quantity = data[producto.id]
                if quantity > 0:
                    print(f"Product ID: {producto.id}, Quantity: {quantity}")
                    linea_producto_albaran = Linea_Producto_Albaran(id_albaran=albaran.id, id_producto=producto.id, cantidad=quantity)
                    db.session.add(linea_producto_albaran)
                    producto.stock += quantity

        db.session.commit()

            #for choice in form.producto.choices:
            #    if choice == producto.name:
            #        print("Entered :)")

    return render_template("albaran.html", form=form, productos=productos)
    

@main.route("/factura", methods=['GET', 'POST'])
def create_factura():
    form = PurchaseForm()
    productos = Producto.query.all()

    data = {}
    for key, value in request.form.items():
        if key != 'csrf_token':
            data[int(key)] = int(value)
    print(data)
    if request.method == "POST" and form.validate():
        print("POST!!!")
        # Create a new factura entry
        factura = Factura()
        db.session.add(factura)
        db.session.commit()

        print(form.producto.data)
        # Iterate over the selected products and reduce the stock
        for producto in productos:
            if producto.id in data:
                quantity = data[producto.id]
                if quantity > 0:
                    print(f"Product ID: {producto.id}, Quantity: {quantity}")
                    factura_producto = Factura_Producto(id_factura=factura.id, id_producto=product_id, cantidad=quantity)
                    db.session.add(factura_producto)
                    producto.stock -= quantity

        db.session.commit()  # Commit changes to the database

    return render_template("factura.html", form=form, productos=productos)


