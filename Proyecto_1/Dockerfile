# FROM python:3.9
FROM tensorflow/tfx:1.16.0

RUN mkdir /app
WORKDIR /app
COPY . .
# COPY . /app

# Con pip
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install apache-beam[interactive]
#==2.45.0
RUN pip install jupyter==1.0.0 -U && pip install jupyterlab==3.6.1

# RUN pip install --no-cache-dir "numpy<2"

EXPOSE 8888 6006

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
# ENTRYPOINT ["/run_jupyter.sh"]