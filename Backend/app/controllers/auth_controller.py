from app.services.cognito_service import CognitoService


class AuthController:
    def __init__(self):
        self.cognito_service = CognitoService()

    def register(self, email, password):
        result = self.cognito_service.register_user(email, password)
        if 'error' in result:
            return {'status': 'fail', 'message': result['error']}
        return {'status': 'success', 'message': 'User registered successfully'}

    def login(self, email, password):
        result = self.cognito_service.login_user(email, password)
        if 'error' in result:
            if result['error'] == 'NEW_PASSWORD_REQUIRED':
                return {'status': 'fail', 'message': 'New password required', 'session': result['session']}
            return {'status': 'fail', 'message': result['error']}
        return {'status': 'success', 'message': 'Login successful', 'token': result['AuthenticationResult']['IdToken']}

    def complete_new_password(self, email, new_password, session):
        result = self.cognito_service.complete_new_password(
            email, new_password, session)
        if 'error' in result:
            return {'status': 'fail', 'message': result['error']}
        return {'status': 'success', 'message': 'Password updated successfully', 'token': result['AuthenticationResult']['IdToken']}
