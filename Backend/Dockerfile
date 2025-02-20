# Usar uma imagem base do Python
FROM python:3.9

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos necessários
COPY . .

# Instalar dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta do Flask
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "run.py"]
