FROM python:3.12-slim
# Establecemos directorio de trabajo
WORKDIR /loadtester

# Copiamos requirements
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código del loadtester
COPY main.py .

# Comando de ejecución
CMD ["python", "main.py"]
