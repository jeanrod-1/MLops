## Instrucciones para Ejecutar

1. **Reconstrucción de imágenes y instanciamiento de contenedores:**

   ```bash
   docker-compose up --build -d

2. **Acceder a los servicios:**
   ```bash

3. **Ejecutar los experimentos del entrenamiento en el notebook ():**

4. **Probar la API específicando el modelo a usar:**

    ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   curl -X 'GET' 'http://localhost:8000/predict?bill_length_mm=45.0&bill_depth_mm=17.5&body_mass_g=4500'

