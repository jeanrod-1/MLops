FROM python:3.9-slim

WORKDIR /app

# Copiamos el requirements desde la carpeta app
COPY app/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Ejecutamos uvicorn apuntando al archivo main.py dentro de app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"] 
