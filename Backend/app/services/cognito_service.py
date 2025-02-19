import boto3
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv
import logging

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do Logging
logging.basicConfig(level=logging.DEBUG)

# Configuração do Cognito
AWS_REGION = os.getenv("AWS_REGION")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not all([AWS_REGION, USER_POOL_ID, CLIENT_ID, CLIENT_SECRET]):
    raise ValueError(
        "As variáveis de ambiente do Cognito não foram configuradas corretamente.")

# Instancia o cliente Cognito
cognito_client = boto3.client("cognito-idp", region_name=AWS_REGION)


def calculate_secret_hash(username):
    """Calcula o SECRET_HASH para autenticação segura"""
    message = username + CLIENT_ID
    dig = hmac.new(CLIENT_SECRET.encode(
        "utf-8"), msg=message.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


class CognitoService:
    def register_user(self, email, password):
        """Registra um novo usuário no Cognito utilizando email como username."""
        try:
            response = cognito_client.sign_up(
                ClientId=CLIENT_ID,
                Username=email,  # O email é o username
                Password=password,
                SecretHash=calculate_secret_hash(email),
                UserAttributes=[{"Name": "email", "Value": email}]
            )
            logging.info(f"Usuário registrado: {email}")
            return {"message": "Usuário registrado com sucesso. Verifique seu e-mail para confirmar a conta."}
        except ClientError as e:
            logging.error(f"Erro no registro do usuário {email}: {e}")
            return {"error": str(e)}

    def confirm_user(self, email, confirmation_code):
        """Confirma a conta do usuário via código enviado por e-mail."""
        try:
            response = cognito_client.confirm_sign_up(
                ClientId=CLIENT_ID,
                Username=email,
                ConfirmationCode=confirmation_code,
                SecretHash=calculate_secret_hash(email)
            )
            logging.info(f"Usuário confirmado: {email}")
            return {"message": "Conta confirmada com sucesso!"}
        except ClientError as e:
            logging.error(f"Erro na confirmação de {email}: {e}")
            return {"error": str(e)}

    def login_user(self, email, password):
        """Autentica um usuário e retorna o token JWT."""
        try:
            response = cognito_client.initiate_auth(
                ClientId=CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password,
                    "SECRET_HASH": calculate_secret_hash(email)
                }
            )
            logging.info(f"Usuário autenticado: {email}")
            return {
                "message": "Login bem-sucedido",
                "id_token": response["AuthenticationResult"]["IdToken"],
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"]
            }
        except ClientError as e:
            logging.error(f"Erro no login de {email}: {e}")
            return {"error": str(e)}

    def forgot_password(self, email):
        """Inicia o fluxo de recuperação de senha."""
        try:
            response = cognito_client.forgot_password(
                ClientId=CLIENT_ID,
                Username=email,
                SecretHash=calculate_secret_hash(email)
            )
            logging.info(f"Pedido de reset de senha para {email}")
            return {"message": "Código de redefinição de senha enviado por e-mail."}
        except ClientError as e:
            logging.error(f"Erro no reset de senha de {email}: {e}")
            return {"error": str(e)}

    def confirm_forgot_password(self, email, confirmation_code, new_password):
        """Confirma a redefinição de senha."""
        try:
            response = cognito_client.confirm_forgot_password(
                ClientId=CLIENT_ID,
                Username=email,
                ConfirmationCode=confirmation_code,
                Password=new_password,
                SecretHash=calculate_secret_hash(email)
            )
            logging.info(f"Senha redefinida para {email}")
            return {"message": "Senha alterada com sucesso."}
        except ClientError as e:
            logging.error(f"Erro ao redefinir senha de {email}: {e}")
            return {"error": str(e)}
