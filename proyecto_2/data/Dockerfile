FROM python:3.9

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "data_api:app", "--host", "0.0.0.0", "--port", "80"]
