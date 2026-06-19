from app.extensions import db

class Producto(db.Model):

    __tablename__ = "productos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(
        db.Text
    )

    precio = db.Column(
        db.Float,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        default=0
    )

    imagen = db.Column(
        db.String(255)
    )

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id")
    )