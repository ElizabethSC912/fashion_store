from app.extensions import db

class Pedido(db.Model):

    __tablename__ = "pedidos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    total = db.Column(
        db.Float
    )

    estado = db.Column(
        db.String(50),
        default="Pendiente"
    )

    fecha = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    detalles = db.relationship(
        "PedidoDetalle",
        backref="pedido",
        lazy=True
    )