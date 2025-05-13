FROM python:3.8-slim

# Establecer directorio de trabajo
WORKDIR /code

# Copiar los requirements e instalar dependencias
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la API y el código fuente
COPY api/ .
COPY src/ /code/src

# Agregar src al PYTHONPATH
ENV PYTHONPATH="/code/src"

# Comando de ejecución
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
