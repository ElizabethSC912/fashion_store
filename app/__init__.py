from flask import Flask
from app.models.user import User
from .config import Config
from .extensions import db
from .extensions import login_manager
from .extensions import migrate


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)

    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    from .admin.routes import vendedor_bp
    from .tienda.routes import tienda_bp

    app.register_blueprint(auth_bp)

    app.register_blueprint(admin_bp)
    
    app.register_blueprint(vendedor_bp)

    app.register_blueprint(tienda_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app