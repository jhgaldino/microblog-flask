from flask import Flask
from .extensions import db, bcrypt, login_manager, migrate
from .routes import main_bp
from .config import Config
from .models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa as extensões
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configura o login_view para redirecionar usuários não autenticados
    login_manager.login_view = 'main.login'  # Nome da função de login no Blueprint 'main'

    # Registra os Blueprints
    app.register_blueprint(main_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
