## Instrucciones para Ejecutar

1. **Reconstrucción de imágenes y instanciamiento de contenedores:**

   ```bash
   docker-compose up --build

2. **Ir al Jupyter Lab Local con el token generado en los logs y entrenar y guardar los modelos necesarios:**

3. **Listar los modelos disponibles:**

   ```bash
   curl -X GET "http://localhost:8000/list_models"

4. **Probar la API específicando el modelo a usar:**

    ```bash
   curl -X GET "http://localhost:8000/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2&model_name=svm_model.joblib"
