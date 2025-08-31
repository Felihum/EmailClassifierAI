FROM python:latest

# Evita buffer no log do python
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema (necessárias pro spaCy)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY . .

# Comando padrão
CMD ["python", "run.py"]
