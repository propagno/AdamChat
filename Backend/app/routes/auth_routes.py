from flask import Blueprint, request, jsonify
from ..controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__)
auth_controller = AuthController()


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    result = auth_controller.login(data['email'], data['password'])
    return jsonify(result)


@auth_bp.route('/auth/complete_new_password', methods=['POST'])
def complete_new_password():
    data = request.get_json()
    result = auth_controller.complete_new_password(
        data['email'], data['new_password'], data['session'])
    return jsonify(result)
