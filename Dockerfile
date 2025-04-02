FROM python:3.9

# Define o diretório de trabalho
WORKDIR /home/suspensepg/htdocs/www.suspensepg.online

# Copia todos os arquivos do diretório atual para o diretório de trabalho do container
COPY . .

# Instalar dependências (se houver um requirements.txt)
# RUN pip install -r requirements.txt

# Expondo a porta
EXPOSE 8015

# Comando para rodar o app
CMD ["python", "server.py"]
