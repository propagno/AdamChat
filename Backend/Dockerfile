# Usar uma imagem base mais leve e otimizada
FROM python:3.9-slim

# Desativar buffering para ver os logs em tempo real
ENV PYTHONUNBUFFERED=1

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias, incluindo ffmpeg para pydub
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    curl \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . .

# Copiar o arquivo JSON para o container
# O caminho do arquivo no EC2 foi fornecido, então vamos copiá-lo para dentro do container
COPY secure-bonus-450617-i7-906cd0940dc5.json /app/

# Definir a variável de ambiente com o novo caminho
ENV GOOGLE_CREDENTIALS_JSON=/app/secure-bonus-450617-i7-906cd0940dc5.json
ENV REACT_APP_API_URL=https://ad919e734038e459a9c7a8cdc8051ecf-1751982795.us-east-2.elb.amazonaws.com

# Atualizar o pip e instalar as dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pelo Flask
EXPOSE 5000

# Comando para rodar o aplicativo
CMD ["python", "run.py"]
