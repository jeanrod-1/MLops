FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8989

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8989"]