from flask import Blueprint, request, jsonify
from ..controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    result = auth_controller.register(data['email'], data['password'])
    return jsonify(result)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    result = auth_controller.login(data['email'], data['password'])
    return jsonify(result)
