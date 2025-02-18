from flask import Flask, request, jsonify
from auth.cognito_service import CognitoService
from auth.auth_middleware import AuthMiddleware

app = Flask(__name__)

# Configurações do Cognito
USER_POOL_ID = 'YOUR_USER_POOL_ID'
CLIENT_ID = 'YOUR_CLIENT_ID'

cognito_service = CognitoService(USER_POOL_ID, CLIENT_ID)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response = cognito_service.register_user(data['email'], data['password'])
    return jsonify(response), response['status']


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    response = cognito_service.login_user(data['email'], data['password'])
    return jsonify(response), response['status']


@app.route('/protected', methods=['GET'])
@AuthMiddleware.auth_required
def protected():
    return jsonify({"message": "This is a protected route"}), 200


if __name__ == '__main__':
    app.run(debug=True)
