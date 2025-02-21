# backend/run.py
from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.chat_routes import chat_bp
from app.routes.transcriber_routes import transcriber_bp
from app.routes.dashboard_routes import dashboard_bp  # Importe o dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")
    
    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(transcriber_bp)
    app.register_blueprint(dashboard_bp)  # Registre o dashboard_bp
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
