from flask import Blueprint, redirect, render_template, request, url_for
from models import  Producto, Albaran, db, Linea_Producto_Albaran, Factura, Factura_Producto
from forms import AddProductForm, PurchaseForm, CreateProductForm

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/productos", methods=['GET', 'POST'])
def productos():
    form = CreateProductForm()
    productos = Producto.query.all()

    if request.method == "POST":
        if form.validate_on_submit():
            new_product = Producto(
                name=form.name.data,
                stock=0,  # We set stock to 0 by default, makes no sense to add stock if no albaran has been ordered
                price=form.price.data
            )
            db.session.add(new_product)
            db.session.commit()
            print('Nuevo producto añadido correctamente')
            return redirect(url_for('main.productos'))
        else:
            print('Error al añadir el producto. Por favor, intente nuevamente.')

    return render_template("productos.html", productos=productos, form=form)



@main.route("/albaran", methods=['GET', 'POST'])
def add_stock():
    form = AddProductForm()
    data = {}
    # We iterate over the items in the request form to get the POST request value which is (product_id: Quantity)
    for key, value in request.form.items():
        if key != 'csrf_token':
            data[int(key)] = int(value)

    productos = Producto.query.all()

    if request.method == "POST" and form.validate():
        # We iterate over the quantities of each product to see if atleast one of the products have a quantity > than 0
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
                    producto.stock += quantity # increment stock

        db.session.commit()
        return redirect(url_for('main.productos'))

    return render_template("albaran.html", form=form, productos=productos)
    

@main.route("/factura", methods=['GET', 'POST'])
def create_factura():
    form = PurchaseForm()
    productos = Producto.query.all()

    data = {}
    # We iterate over the items in the request form to get the POST request value which is (product_id: Quantity)
    for key, value in request.form.items():
        if key != 'csrf_token':
            data[int(key)] = int(value)
    print(data)
    if request.method == "POST" and form.validate():
        # We iterate over the quantities of each product to see if atleast one of the products have a quantity > than 0
        check_quantity = any(quantity > 0 for quantity in data.values())

        if not check_quantity:
            print("Please select at least one product to purchase.")
            return redirect(url_for("main.create_factura"))  # Redirect back to the form

        error_occurred = False

        factura = Factura()
        db.session.add(factura)
        # flush to obtain id, to insert into the Factura_Producto. We don't commit, because if there is an error, we want to rollback
        db.session.flush() 

        for producto in productos:
            if producto.id in data:
                quantity = data[producto.id] # retrieves the quantity value associated with each product id
                if quantity > 0:
                    if producto.stock - quantity < 0:
                        print(f"Not enough stock available for {producto.name}. Please select a lower quantity.", "error")
                        error_occurred = True
                        db.session.rollback()
                        break

                    else:
                        factura_producto = Factura_Producto(id_factura=factura.id, id_producto=producto.id, cantidad=quantity)
                        db.session.add(factura_producto)
                        producto.stock -= quantity # reduce stock
                        
        if error_occurred:
            print("An error occurred during the transaction. Rolling back.")
            db.session.rollback()
            return redirect(url_for("main.create_factura"))  # Redirect back to the form
        else:
            db.session.commit()
            return redirect(url_for('main.productos'))

    return render_template("factura.html", form=form, productos=productos)
