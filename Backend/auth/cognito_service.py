import boto3
from botocore.exceptions import ClientError


class CognitoService:
    def __init__(self, user_pool_id, client_id, region_name='us-east-1'):
        self.client = boto3.client('cognito-idp', region_name=region_name)
        self.user_pool_id = user_pool_id
        self.client_id = client_id

    def register_user(self, email, password):
        try:
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password
            )
            return {"message": "User registered successfully", "status": 200}
        except ClientError as e:
            return {"message": str(e), "status": 400}

    def login_user(self, email, password):
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            return {
                "message": "Login successful",
                "status": 200,
                "token": response['AuthenticationResult']['IdToken']
            }
        except ClientError as e:
            return {"message": str(e), "status": 400}
