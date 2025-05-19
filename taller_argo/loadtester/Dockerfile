FROM python:3.12-slim
# Establecemos directorio de trabajo
WORKDIR /app

# Copiamos requirements
COPY requirements.txt .
COPY main.py .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando de ejecución
CMD ["python", "main.py"]
