from ..services.cognito_service import CognitoService


class AuthController:
    def __init__(self):
        self.cognito_service = CognitoService()

    def register(self, email, password):
        return self.cognito_service.register_user(email, password)

    def login(self, email, password):
        return self.cognito_service.login_user(email, password)
