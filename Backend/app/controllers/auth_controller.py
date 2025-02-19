from flask import request, jsonify
from app.services.cognito_service import CognitoService

cognito_service = CognitoService()


def login():
    data = request.json
    result = cognito_service.login(data["username"], data["password"])
    return jsonify(result)


def register():
    data = request.json
    result = cognito_service.register(data["username"], data["password"])
    return jsonify(result)
