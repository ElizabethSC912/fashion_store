from app.extensions import db

class Categoria(db.Model):

    __tablename__ = "categorias"

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

    productos = db.relationship(
        "Producto",
        backref="categoria",
        lazy=True
    )