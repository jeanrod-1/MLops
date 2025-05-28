FROM python:3.10-slim
WORKDIR /app
COPY api/app /app
RUN pip install fastapi uvicorn mlflow pandas scikit-learn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]