from app.extensions import db

class Carrito(db.Model):

    __tablename__ = "carrito"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id")
    )

    cantidad = db.Column(
        db.Integer,
        default=1
    )
    producto = db.relationship(
    "Producto"
    )