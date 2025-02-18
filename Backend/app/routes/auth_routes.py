from flask import Blueprint, Flask, request, jsonify
# Ajuste o caminho de importação conforme necessário
from app.controllers.auth_controller import AuthController

# Criação do Blueprint
auth_bp = Blueprint('auth_bp', __name__)
auth_controller = AuthController()

# Criação do aplicativo Flask
app = Flask(__name__)

# Rota para a página inicial


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the API'})

# Rota de login


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    result = auth_controller.login(data['email'], data['password'])
    return jsonify(result)

# Rota para completar nova senha


@auth_bp.route('/auth/complete_new_password', methods=['POST'])
def complete_new_password():
    data = request.get_json()
    result = auth_controller.complete_new_password(
        data['email'], data['new_password'], data['session'])
    return jsonify(result)


# Registro do Blueprint no aplicativo Flask
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
