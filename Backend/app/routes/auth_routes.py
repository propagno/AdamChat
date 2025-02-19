from flask import Blueprint, request, jsonify
from app.services.cognito_service import CognitoService

auth_bp = Blueprint("auth_bp", __name__)
cognito_service = CognitoService()


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    return jsonify(cognito_service.register_user(data["email"], data["password"]))


@auth_bp.route("/auth/confirm", methods=["POST"])
def confirm():
    data = request.json
    return jsonify(cognito_service.confirm_user(data["email"], data["confirmation_code"]))


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    return jsonify(cognito_service.login_user(data["email"], data["password"]))


@auth_bp.route("/auth/forgot_password", methods=["POST"])
def forgot_password():
    data = request.json
    return jsonify(cognito_service.forgot_password(data["email"]))


@auth_bp.route("/auth/reset_password", methods=["POST"])
def reset_password():
    data = request.json
    return jsonify(cognito_service.confirm_forgot_password(data["email"], data["confirmation_code"], data["new_password"]))
