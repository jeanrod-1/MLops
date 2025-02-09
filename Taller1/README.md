# Taller MLOps - Predicción de Penguins Species

## Descripción
Este proyecto realiza procesamiento de datos, entrenamiento de un modelo de clasificación y expone un API para hacer inferencias sobre datos de pingüinos.

## Requisitos
- Docker
- Python 3.9+ 


## Instrucciones para Ejecutar la API

1. **Construir la imagen Docker:**

   ```bash
   docker build -t mlo_api .

2. **Ejecutar el contenedor:**

    ```bash
   docker run -p 8989:8989 --name mlo_api_container mlo_api

3. **Probar la API:**

   culmen_lenght_mm, culmen_depth_mm y body_mass_g reciben valores float  

    ```bash
   curl -X POST "http://localhost:8989/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "culmen_length_mm": 39.1,
           "culmen_depth_mm": 18.7,
           "body_mass_g": 3750
         }'
    