from flask import Flask
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Verificar se as variáveis estão sendo carregadas
if not os.getenv('AWS_REGION'):
    raise ValueError("AWS_REGION environment variable is not set")
if not os.getenv('COGNITO_USER_POOL_ID'):
    raise ValueError("COGNITO_USER_POOL_ID environment variable is not set")
if not os.getenv('COGNITO_CLIENT_ID'):
    raise ValueError("COGNITO_CLIENT_ID environment variable is not set")
if not os.getenv('CLIENT_SECRET'):
    raise ValueError("COGNITO_CLIENT_SECRET environment variable is not set")


def create_app():
    app = Flask(__name__)

    # Importar e registrar rotas
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
