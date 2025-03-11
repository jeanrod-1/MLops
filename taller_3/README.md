## Instrucciones para Ejecutar

1. **Crear directorios y variables para la ejecución:**

   ```bash
   mkdir -p ./dags ./logs ./plugins
   echo -e "AIRFLOW_UID=$(id -u)" > .env

2. **Reconstrucción de imágenes y instanciamiento de contenedores:**

   ```bash
   docker compose up airflow-init
   docker-compose up --build


3. **Iniciar sesión en Docker hub para configurar credenciales (opcional, si sale error: getting credentials - err: exit status 1, out: `):**
   ```bash
   rm ~/.docker/config.json
   echo "<PASSWORD>" | docker login -u <USER> --password-stdin

4. **Agregar la conexión de MySQL a Airflow:**

   ```bash
   docker exec -it taller_3-airflow-webserver-1 airflow connections add 'mysql_default' \
    --conn-type 'mysql' \
    --conn-host 'mysql-db' \
    --conn-schema 'airflow_db' \
    --conn-login 'airflow' \
    --conn-password 'airflow_pass' \
    --conn-port '3306'

5. **Ir a Airflow y ejecutar los DAG (http://localhost:8080):**

   ```bash
   usuario: airflow
   contraseña: airflow

6. **Probar la API específicando el modelo a usar:**

    ```bash
   curl -X GET "http://localhost:8000/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2&model_name=rf_model.joblib"
