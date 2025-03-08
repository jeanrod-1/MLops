## Instrucciones para Ejecutar

1. **Reconstrucción de imágenes y instanciamiento de contenedores:**

   ```bash
   docker compose up airflow-init
   docker-compose up --build

2. **Iniciar sesión en Docker hub para configurar credenciales (opcional, si sale error: getting credentials - err: exit status 1, out: `):**
   ```bash
   rm ~/.docker/config.json
   echo "<PASSWORD>" | docker login -u <USER> --password-stdin

3. **Ir a Airflow y ejecutar los DAX (http://localhost:8080):**

   ```bash
   usuario: airflow
   contraseña: airflow

4. **Probar la API específicando el modelo a usar:**

    ```bash
   curl -X GET "http://localhost:8000/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2&model_name=rf_model.joblib"
