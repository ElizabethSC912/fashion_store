from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    existe = User.query.filter_by(
        correo="vendedor@gmail.com"
    ).first()

    if not existe:

        vendedor = User(
            nombre="Vendedor",
            correo="vendedor@gmail.com",
            password=generate_password_hash("123456"),
            rol="vendedor"
        )

        db.session.add(vendedor)
        db.session.commit()

        print("Vendedor creado")

    else:
        print("Ya existe")