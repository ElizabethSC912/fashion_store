from flask import Blueprint
from flask import render_template
from app.models.producto import Producto
from app.models.categoria import Categoria
from flask_login import login_required
from flask_login import current_user
from flask import flash
from flask import redirect
from flask import url_for
from app.extensions import db
from app.models.carrito import Carrito
from app.models.pedido import Pedido
from app.models.pedido_detalle import PedidoDetalle

tienda_bp = Blueprint(
    "tienda",
    __name__
)


@tienda_bp.route("/")
def inicio():

    productos = Producto.query.all()
    categorias = Categoria.query.all()

    return render_template(
        "inicio.html",
        productos=productos,
        categorias=categorias
    )
    
@tienda_bp.route("/agregar-carrito/<int:id>")
@login_required
def agregar_carrito(id):

    item = Carrito.query.filter_by(
        usuario_id=current_user.id,
        producto_id=id
    ).first()

    if item:

        item.cantidad += 1

    else:

        item = Carrito(
            usuario_id=current_user.id,
            producto_id=id,
            cantidad=1
        )

        db.session.add(item)
    db.session.commit()

    return redirect(
        url_for("tienda.carrito")
    )
    
@tienda_bp.route("/carrito")
@login_required
def carrito():

    items = Carrito.query.filter_by(
        usuario_id=current_user.id
    ).all()

    return render_template(
        "carrito.html",
        items=items
    )
@tienda_bp.route("/confirmar-compra")
@login_required
def confirmar_compra():

    items = Carrito.query.filter_by(
        usuario_id=current_user.id
    ).all()

    total = 0

    for item in items:

        total += (
            item.producto.precio *
            item.cantidad
        )

    pedido = Pedido(
        usuario_id=current_user.id,
        total=total,
        estado="Pendiente"
    )

    db.session.add(pedido)
    db.session.flush()

    for item in items:
        
        item.producto.stock -= item.cantidad
        detalle = PedidoDetalle(
            pedido_id=pedido.id,
            producto_id=item.producto.id,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )

        db.session.add(detalle)
        db.session.delete(item)
    db.session.commit()

    return redirect(
        url_for("tienda.pedidos")
    )
    
@tienda_bp.route(
    "/pedidos"
)
@login_required
def pedidos():

    pedidos = Pedido.query.filter_by(
        usuario_id=current_user.id
    ).all()

    return render_template(
        "pedidos.html",
        pedidos=pedidos
    )
    
@tienda_bp.route(
    "/pedidoss/<int:id>"
)
@login_required
def detalle_pedido(id):

    pedido = Pedido.query.get_or_404(id)

    return render_template(
        "pedido_detalle.html",
        pedido=pedido
    )
    
@tienda_bp.route("/sumar-carrito/<int:id>")
@login_required
def sumar_carrito(id):

    item = Carrito.query.get_or_404(id)

    if item.cantidad < item.producto.stock:
        item.cantidad += 1
        db.session.commit()

    return redirect(
        url_for("tienda.carrito")
    )
    
@tienda_bp.route("/restar-carrito/<int:id>")
@login_required
def restar_carrito(id):

    item = Carrito.query.get_or_404(id)

    if item.cantidad > 1:
        item.cantidad -= 1

    else:

        db.session.delete(item)
    db.session.commit()

    return redirect(
        url_for("tienda.carrito")
    )
    
@tienda_bp.route("/cancelar-pedido/<int:id>")
@login_required
def cancelar_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    if pedido.usuario_id != current_user.id:
        
        flash("Acceso denegado")

        return redirect(
            url_for("tienda.pedidos")
        )
    db.session.delete(pedido)

    db.session.commit()
    flash("Pedido cancelado")
    return redirect(
        url_for("tienda.pedidos")
    )