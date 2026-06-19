from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]
        existe = User.query.filter_by(
            correo=correo
        ).first()

        if existe:

            flash("Correo ya registrado")

            return redirect(
                url_for("auth.register")
            )

        nuevo_usuario = User(
            nombre=nombre,
            correo=correo,
            password=generate_password_hash(password)
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Registro exitoso")
        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
        usuario = User.query.filter_by(
            correo=correo
        ).first()

        if usuario and check_password_hash(
            usuario.password,
            password
        ):

            login_user(usuario)
            if usuario.rol == "admin":
                return redirect(
                    url_for("admin.dashboard")
                )
            elif usuario.rol == "vendedor":
                return redirect(
                    url_for("vendedor.productos")
            )
            return redirect(
                url_for("tienda.inicio")
            )

        flash("Credenciales incorrectas")

    return render_template(
        "login.html"
    )
    

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )
    
