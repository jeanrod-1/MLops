
# Establecemos directorio de trabajo
WORKDIR /app

# Copiamos solo los archivos necesarios
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos de la API
COPY app/ ./app/

# Exponemos el puerto por defecto de Uvicorn
EXPOSE 8000

# Comando de ejecución
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
