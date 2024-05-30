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
        # Iteramos sobre las cantidades de cada producto para ver si almenos uno de los productos tienen una cantidad elevada a 0
        check_quantity = any(quantity > 0 for quantity in data.values())

        if not check_quantity:
            print("Please select at least one product to purchase.")
            return redirect(url_for("main.add_stock"))  # Redirect back to the form


        albaran = Albaran()
        db.session.add(albaran)
        db.session.commit()  # Commit the Albaran to obtain its id

        for producto in productos:
            if producto.id in data:
                quantity = data[producto.id]
                if quantity > 0:
                    print(f"Product ID: {producto.id}, Quantity: {quantity}")
                    linea_producto_albaran = Linea_Producto_Albaran(id_albaran=albaran.id, id_producto=producto.id, cantidad=quantity)
                    db.session.add(linea_producto_albaran)
                    producto.stock += quantity

        db.session.commit()
        return redirect(url_for('main.productos'))

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
        # Iteramos sobre las cantidades de cada producto para ver si almenos uno de los productos tienen una cantidad elevada a 0
        check_quantity = any(quantity > 0 for quantity in data.values())

        if not check_quantity:
            print("Please select at least one product to purchase.")
            return redirect(url_for("main.create_factura"))  # Redirect back to the form

        error_occurred = False

        factura = Factura()
        db.session.add(factura)
        db.session.flush()

        print(form.producto.data)
        for producto in productos:
            if producto.id in data:
                quantity = data[producto.id]
                if quantity > 0:
                    if producto.stock - quantity < 0:
                        print(f"Not enough stock available for {producto.name}. Please select a lower quantity.", "error")
                        error_occurred = True
                        db.session.rollback()
                        break

                    else:
                        factura_producto = Factura_Producto(id_factura=factura.id, id_producto=producto.id, cantidad=quantity)
                        db.session.add(factura_producto)
                        producto.stock -= quantity
                        
        if error_occurred:
            print("An error occurred during the transaction. Rolling back.")
            db.session.rollback()
            return redirect(url_for("main.create_factura"))  # Redirect back to the form
        else:
            db.session.commit()
            return redirect(url_for('main.productos'))

    return render_template("factura.html", form=form, productos=productos)


