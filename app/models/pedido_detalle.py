from app.extensions import db

class PedidoDetalle(db.Model):

    __tablename__ = "pedido_detalle"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id")
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id")
    )

    cantidad = db.Column(
        db.Integer,
        default=1
    )

    precio = db.Column(
        db.Float
    )

    producto = db.relationship(
        "Producto"
    )