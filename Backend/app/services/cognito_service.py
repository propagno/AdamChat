import boto3
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def calculate_secret_hash(client_id, client_secret, username):
    message = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'),
                   msg=str(message).encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


class CognitoService:
    def __init__(self):
        region_name = os.getenv('AWS_REGION')
        user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
        client_id = os.getenv('COGNITO_CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')

        if not region_name or not user_pool_id or not client_id or not client_secret:
            raise ValueError(
                "Cognito configuration environment variables are not set")

        self.client = boto3.client('cognito-idp', region_name=region_name)
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.client_secret = client_secret

    def register_user(self, email, password):
        try:
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                ]
            )
            return response
        except ClientError as e:
            return {'error': str(e)}

    def login_user(self, email, password):
        try:
            secret_hash = calculate_secret_hash(
                self.client_id, self.client_secret, email)
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                    'SECRET_HASH': secret_hash
                }
            )
            logging.debug(f"Response from Cognito: {response}")
            if 'AuthenticationResult' in response:
                return response
            elif response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
                return {'error': 'NEW_PASSWORD_REQUIRED', 'session': response['Session']}
            else:
                return {'error': 'Authentication failed'}
        except ClientError as e:
            logging.error(f"ClientError: {e}")
            return {'error': str(e)}


def complete_new_password(self, email, new_password, session):
    try:
        secret_hash = calculate_secret_hash(
            self.client_id, self.client_secret, email)
        response = self.client.respond_to_auth_challenge(
            ClientId=self.client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            Session=session,
            ChallengeResponses={
                'USERNAME': email,
                'NEW_PASSWORD': new_password,
                'SECRET_HASH': secret_hash
            }
        )
        logging.debug(f"Response from Cognito: {response}")
        if 'AuthenticationResult' in response:
            return response
        else:
            return {'error': 'Password update failed'}
    except ClientError as e:
        logging.error(f"ClientError: {e}")
        return {'error': str(e)}
