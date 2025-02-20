# Usar uma imagem base mais leve e otimizada
FROM python:3.9-slim

# Desativar buffering para ver os logs em tempo real
ENV PYTHONUNBUFFERED=1

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . .

# Atualizar o pip e instalar as dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pelo Flask
EXPOSE 5000

# Comando para rodar o aplicativo
CMD ["python", "run.py"]
