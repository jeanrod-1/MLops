# FROM apache/airflow:2.7.1

# USER root
# COPY requirements.txt /requirements.txt
# USER airflow
# RUN pip install --no-cache-dir -r /requirements.txt

FROM apache/airflow:2.7.1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
#CMD ["api:app", "--host", "0.0.0.0", "--port", "8989"]