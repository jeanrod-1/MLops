## Instrucciones para Ejecutar

1. **Reconstrucción de imágenes y instanciamiento de contenedores:**

   ```bash
   docker-compose up --build -d

2. **Verificar los servicios:**
   ```bash
   MLflow: http://10.43.101.193:5000
   MinIO: http://10.43.101.193:9090
   JupyterLab: http://10.43.101.193:8888

3. **Ejecutar los experimentos del entrenamiento en el notebook (http://10.43.101.193:8888):**

4. **Probar la API específicando el modelo a usar:**

    ```bash
   curl -X 'GET' 'http://10.43.101.193:8000/predict?bill_length_mm=45.0&bill_depth_mm=17.5&body_mass_g=4500'

