import boto3
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# CloudWatch Logs configuration
cloudwatch_logs_client = boto3.client('logs')
log_group_name = 'AdamChatAuthLogs'
log_stream_name = 'AuthStream'

# Create log group if it doesn't exist
try:
    cloudwatch_logs_client.create_log_group(logGroupName=log_group_name)
    logging.debug(f"Log group {log_group_name} created.")
except cloudwatch_logs_client.exceptions.ResourceAlreadyExistsException:
    logging.debug(f"Log group {log_group_name} already exists.")
except ClientError as e:
    logging.error(f"Error creating log group: {e}")

# Create log stream if it doesn't exist
try:
    cloudwatch_logs_client.create_log_stream(
        logGroupName=log_group_name, logStreamName=log_stream_name)
    logging.debug(f"Log stream {log_stream_name} created.")
except cloudwatch_logs_client.exceptions.ResourceAlreadyExistsException:
    logging.debug(f"Log stream {log_stream_name} already exists.")
except ClientError as e:
    logging.error(f"Error creating log stream: {e}")

sequence_token = None


def log_to_cloudwatch(message):
    global sequence_token
    timestamp = int(datetime.utcnow().timestamp() * 1000)
    log_event = {
        'logGroupName': log_group_name,
        'logStreamName': log_stream_name,
        'logEvents': [
            {
                'timestamp': timestamp,
                'message': message
            }
        ]
    }
    if sequence_token:
        log_event['sequenceToken'] = sequence_token

    try:
        response = cloudwatch_logs_client.put_log_events(**log_event)
        logging.debug(f"Log event sent to CloudWatch: {message}")
        logging.debug(f"Response from CloudWatch: {response}")
        sequence_token = response.get('nextSequenceToken')
    except ClientError as e:
        logging.error(f"Error sending log event to CloudWatch: {e}")
        if e.response['Error']['Code'] == 'InvalidSequenceTokenException':
            sequence_token = e.response['Error']['Message'].split(' ')[-1]
            log_to_cloudwatch(message)
        else:
            logging.error(f"Unexpected error: {e}")


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
            log_to_cloudwatch(f"User registered: {email}")
            return response
        except ClientError as e:
            log_to_cloudwatch(f"Registration error for {email}: {str(e)}")
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
            log_to_cloudwatch(f"Login attempt for {email}: {response}")
            if 'AuthenticationResult' in response:
                return response
            elif response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
                return {'error': 'NEW_PASSWORD_REQUIRED', 'session': response['Session']}
            else:
                return {'error': 'Authentication failed'}
        except ClientError as e:
            logging.error(f"ClientError: {e}")
            log_to_cloudwatch(f"Login error for {email}: {str(e)}")
            if e.response['Error']['Code'] == 'NotAuthorizedException':
                self.initiate_password_reset(email)
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
                    'SECRET_HASH': secret_hash,
                    'userAttributes.nickname': 'nickname'  # Adicione o atributo 'nickname' aqui
                }
            )
            logging.debug(f"Response from Cognito: {response}")
            log_to_cloudwatch(
                f"Password update attempt for {email}: {response}")
            if 'AuthenticationResult' in response:
                return response
            else:
                return {'error': 'Password update failed'}
        except ClientError as e:
            logging.error(f"ClientError: {e}")
            log_to_cloudwatch(f"Password update error for {email}: {str(e)}")
            return {'error': str(e)}

    def initiate_password_reset(self, email):
        try:
            response = self.client.forgot_password(
                ClientId=self.client_id,
                Username=email,
                SecretHash=calculate_secret_hash(
                    self.client_id, self.client_secret, email)
            )
            logging.debug(f"Password reset initiated for {email}: {response}")
            log_to_cloudwatch(
                f"Password reset initiated for {email}: {response}")
            return response
        except ClientError as e:
            logging.error(f"ClientError: {e}")
            log_to_cloudwatch(
                f"Password reset initiation error for {email}: {str(e)}")
            return {'error': str(e)}

    def confirm_password_reset(self, email, confirmation_code, new_password):
        try:
            response = self.client.confirm_forgot_password(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code,
                Password=new_password,
                SecretHash=calculate_secret_hash(
                    self.client_id, self.client_secret, email)
            )
            logging.debug(f"Password reset confirmed for {email}: {response}")
            log_to_cloudwatch(
                f"Password reset confirmed for {email}: {response}")
            return response
        except ClientError as e:
            logging.error(f"ClientError: {e}")
            log_to_cloudwatch(
                f"Password reset confirmation error for {email}: {str(e)}")
            return {'error': str(e)}
