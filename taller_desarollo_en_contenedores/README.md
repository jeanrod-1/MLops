## Instrucciones para Ejecutar

1. **Reconstrucción de imágenes y instanciamiento de contenedores:**

   ```bash
   docker-compose up --build

2. **Ir al Jupyter Lab Local con el token generado en los logs y entrenar y guardar los modelos necesarios:**

3. **Opcinal, reiniciar el servicio si no se encuentra el archivo del modelo:**

   ```bash
      docker compose restart api

4. **Probar la API:**

    ```bash
   curl "http://localhost:8000/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2"