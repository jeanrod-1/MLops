FROM python:3.12-slim
# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la aplicación FastAPI con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]