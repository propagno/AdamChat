# backend/app/__init__.py
from flask import Flask, render_template
from app.config import Config


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def home():
        return render_template('login.html')

    return app
