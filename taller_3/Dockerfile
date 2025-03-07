FROM apache/airflow:2.6.0


COPY requirements.txt .
# Con pip
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install jupyter==1.0.0 -U && pip install jupyterlab==3.6.1
# RUN pip install jupyter_core -U

# ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
#CMD ["api:app", "--host", "0.0.0.0", "--port", "8989"]