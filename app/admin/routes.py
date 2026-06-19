import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import Blueprint
from flask import render_template
from flask_login import login_required
from app.admin.utils import admin_required
from app.models.user import User
from flask import flash
from app.models.producto import Producto
from app.models.pedido import Pedido
from flask import request
from flask import redirect
from flask import url_for
from app.extensions import db
from app.models.categoria import Categoria
from app.models.producto import Producto

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)
vendedor_bp = Blueprint(
    "vendedor",
    __name__,
    url_prefix="/vendedor"
)

@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():

    total_usuarios = User.query.count()
    total_productos = Producto.query.count()
    total_pedidos = Pedido.query.count()
    ventas = Pedido.query.all()
    total_ventas = sum(
        pedido.total
        for pedido in ventas
    )

    return render_template(
        "dashboard.html",
        total_usuarios=total_usuarios,
        total_productos=total_productos,
        total_pedidos=total_pedidos,
        total_ventas=total_ventas
    )
    

@admin_bp.route("/usuarios")
@login_required
@admin_required
def usuarios():

    usuarios = User.query.all()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )

@admin_bp.route("/categorias")
@login_required
@admin_required
def categorias():
    categorias = Categoria.query.all()
    return render_template(
        "categorias.html",
        categorias=categorias
    )
@admin_bp.route(
    "/categorias/nueva",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def nueva_categoria():

    if request.method == "POST":
        categoria = Categoria(
            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"]
        )
        db.session.add(categoria)
        db.session.commit()
        return redirect(
            url_for("admin.categorias")
        )

    return render_template(
        "categoria_form.html",
        categoria=None
    )
@admin_bp.route("/categorias/editar/<int:id>",methods=["GET", "POST"])
@login_required
@admin_required
def editar_categoria(id):

    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        categoria.nombre = request.form["nombre"]
        categoria.descripcion = request.form["descripcion"]
        db.session.commit()
        return redirect(
            url_for("admin.categorias")
        )

    return render_template(
        "categoria_form.html",
        categoria=categoria
    )
    
    
@admin_bp.route("/categorias/eliminar/<int:id>")
@login_required
@admin_required
def eliminar_categoria(id):

    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()

    return redirect(
        url_for("admin.categorias")
    )
@admin_bp.route("/productos")
@login_required
@admin_required
def productos():

    productos = Producto.query.all()
    return render_template(
        "productos.html",
        productos=productos
    )
    
    
@admin_bp.route("/productos/nuevo",methods=["GET", "POST"])
@login_required
@admin_required
def nuevo_producto():

    categorias = Categoria.query.all()

    if request.method == "POST":
        imagen = request.files["imagen"]
        nombre_archivo = ""
        if imagen:
            nombre_archivo = secure_filename(
            imagen.filename
        )
        ruta = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            nombre_archivo
        )
        imagen.save(ruta)
        producto = Producto(

            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"],
            precio=request.form["precio"],
            stock=request.form["stock"],
            categoria_id=request.form["categoria_id"],
            imagen=nombre_archivo
        )

        db.session.add(producto)
        db.session.commit()
        return redirect(
            url_for("admin.productos")
        )

    return render_template(
        "producto_form.html",
        categorias=categorias
    )
    
    
@admin_bp.route("/productos/editar/<int:id>",methods=["GET", "POST"])
@login_required
@admin_required
def editar_producto(id):

    producto = Producto.query.get_or_404(id)
    categorias = Categoria.query.all()

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.descripcion = request.form["descripcion"]
        producto.precio = request.form["precio"]
        producto.stock = request.form["stock"]
        producto.categoria_id = request.form["categoria_id"]
        db.session.commit()
        return redirect(
            url_for("admin.productos")
        )

    return render_template(
        "producto_form.html",
        producto=producto,
        categorias=categorias
    )
    
    
@admin_bp.route("/productos/eliminar/<int:id>")
@login_required
@admin_required
def eliminar_producto(id):

    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    return redirect(
        url_for("admin.productos")
    )

@admin_bp.route("/pedidos")
@login_required
@admin_required
def admin_pedidos():

    pedidos = Pedido.query.all()

    return render_template(
        "admin_pedidos.html",
        pedidos=pedidos
    )
    
    
@admin_bp.route("/eliminar-usuario/<int:id>")
@login_required
@admin_required
def eliminar_usuario(id):

    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado")
    return redirect(
        url_for("admin.usuarios")
    )
    
    
@admin_bp.route("/vender/<int:id>")
@login_required
@admin_required
def vender(id):

    pedido = Pedido.query.get_or_404(id)
    pedido.estado = "vendido"
    db.session.commit()
    flash("Pedido vendido")

    return redirect(
        url_for("admin.admin_pedidos")
    )
    

#CAMPO VENDEDOR:
@vendedor_bp.route("/categorias")
@login_required
def categorias():

    categorias = Categoria.query.all()

    return render_template(
        "categorias.html",
        categorias=categorias
    )
    
#NUEVA CATEGORIA VENDEDOR
@vendedor_bp.route("/categorias/nueva",methods=["GET", "POST"])
@login_required
def nueva_categoria():

    if request.method == "POST":
        categoria = Categoria(
            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"]
        )
        db.session.add(categoria)
        db.session.commit()

        return redirect(
            url_for("vendedor.categorias")
        )
    return render_template(
        "categoria_form.html",
        categoria=None
    )
    
#EDITAR CATEGORIA VENDEDOR
@vendedor_bp.route("/categorias/editar/<int:id>",methods=["GET", "POST"])
@login_required
def editar_categoria(id):

    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        categoria.nombre = request.form["nombre"]
        categoria.descripcion = request.form["descripcion"]
        db.session.commit()
        return redirect(
            url_for("vendedor.categorias")
        )

    return render_template(
        "categoria_form.html",
        categoria=categoria
    )
    
#ELIMINAR CATEGORIA VENDEDOR
@vendedor_bp.route("/categorias/eliminar/<int:id>")
@login_required
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()

    return redirect(
        url_for("vendedor.categorias")
    )
    

#PRODUCTOS VENDEDOR
@vendedor_bp.route("/productos")
@login_required
def productos():
    productos = Producto.query.all()
    return render_template(
        "productos.html",
        productos=productos
    )
    
#NUEVOS PRODUCTOS VENDEDOR
@vendedor_bp.route("/productos/nuevo",methods=["GET", "POST"])
@login_required
def nuevo_producto():
    categorias = Categoria.query.all()
    if request.method == "POST":
        imagen = request.files["imagen"]
        nombre_archivo = ""

        if imagen:
            nombre_archivo = secure_filename(
            imagen.filename
        )
        ruta = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            nombre_archivo
        )
        imagen.save(ruta)
        producto = Producto(
            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"],
            precio=request.form["precio"],
            stock=request.form["stock"],
            categoria_id=request.form["categoria_id"],
            imagen=nombre_archivo
        )

        db.session.add(producto)
        db.session.commit()
        return redirect(
            url_for("vendedor.productos")
        )
    return render_template(
        "producto_form.html",
        categorias=categorias
    )
    
#EDITAR PRODUCTOS VENDEDOR
@vendedor_bp.route("/productos/editar/<int:id>",methods=["GET", "POST"])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    categorias = Categoria.query.all()

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.descripcion = request.form["descripcion"]
        producto.precio = request.form["precio"]
        producto.stock = request.form["stock"]
        producto.categoria_id = request.form["categoria_id"]
        db.session.commit()
        return redirect(
            url_for("vendedor.productos")
        )
    return render_template(
        "producto_form.html",
        producto=producto,
        categorias=categorias
    )
    
#ELIMINAR PRODUCTOS VENDEDOR
@vendedor_bp.route("/productos/eliminar/<int:id>")
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(
        url_for("vendedor.productos")
    )

#ADMINISTRAR PRODUCTOS VENDEDOR
@vendedor_bp.route("/pedidos")
@login_required
def admin_pedidos():

    pedidos = Pedido.query.all()
    return render_template(
        "admin_pedidos.html",
        pedidos=pedidos
    )
    
#VENDER PRODUCTOS 
@vendedor_bp.route("/vender/<int:id>")
@login_required
def vender(id):

    pedido = Pedido.query.get_or_404(id)
    pedido.estado = "vendido"
    db.session.commit()
    flash("Pedido vendido")
    return redirect(
        url_for("vendedor.admin_pedidos")
    )