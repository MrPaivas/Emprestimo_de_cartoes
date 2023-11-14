# Use a imagem base do Python
FROM python:3.8

# Define o diretório de trabalho
WORKDIR .

# Copia os arquivos necessários para o contêiner
COPY . .
RUN pip install --upgrade pip
# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta em que o aplicativo Flask será executado
EXPOSE 5000

# Comando para iniciar o aplicativo
CMD ["python", "app.py"]
