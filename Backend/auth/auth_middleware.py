from flask import request, jsonify
import jwt


class AuthMiddleware:
    @staticmethod
    def auth_required(f):
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token is missing!"}), 403
            try:
                # Decodificar o token JWT
                jwt.decode(token, options={"verify_signature": False})
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired!"}), 403
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token!"}), 403
            return f(*args, **kwargs)
        return wrapper
