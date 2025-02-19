import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()


class Config:
    # Região da AWS (pode ser utilizada em outros serviços)
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

    # Configurações do Amazon Cognito
    COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
    COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Outras configurações podem ser adicionadas conforme necessário.

    credentials_path = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not credentials_path:
        raise ValueError(
            "A variável GOOGLE_CREDENTIALS_JSON não foi definida.")
    # Para debug, confirme o caminho
    print("GOOGLE_CREDENTIALS_JSON:", credentials_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
