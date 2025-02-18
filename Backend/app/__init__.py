from flask import Flask, request


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Hello, World!'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Lógica de login aqui
            return 'Login route'
        else:
            return 'Login page - use POST to login'

    return app
