from flask import Blueprint, redirect, render_template, request, url_for
from models import  Producto, Albaran, db #Post
from forms import AddProductForm

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/adios")
def adios():
    return "adios"

#@main.route("/posts")
#def posts():
#    posts = Post.query.all()
#    return render_template("posts.html", posts=posts)

#@main.route("/post/<int:post_id>")
#def post(post_id):
#    post = Post.query.get_or_404(post_id)
#    return render_template("post.html", post=post)

#@main.route("/createpost", methods=["GET", "POST"])
#def add_post():
#    form = PostForm()
#    if form.validate_on_submit():
#       title = request.form.get("title")
#        post = Post(title=title)
#        db.session.add(post)
#        db.session.commit()
#        return redirect(url_for("main.home"))
#    return render_template("create_post.html", form=form)

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
    print("Entered albaran")
    form = AddProductForm()
    print(request.form)
    productos = Producto.query.all()
    print(form.producto.data)
    for producto in productos:
        
        for choice in form.producto.data:
            print('choice: ' + choice)

    if request.method == "POST":
        print("Passed validation")
        albaran = Albaran()
        #albaran.producto = #
        db.session.add(albaran)
        db.session.commit()
    
    return render_template("albaran.html", form=form, productos=productos)
    

# Routing help: https://pythongeeks.org/python-flask-app-routing/