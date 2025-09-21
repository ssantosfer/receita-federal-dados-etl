FROM python:3.11-slim

# Setar diretório de trabalho
WORKDIR /app

# Copiar dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código
COPY . .

# Rodar o pipeline ao iniciar
CMD ["python", "main.py"]