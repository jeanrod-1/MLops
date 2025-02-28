FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Con UV
RUN pip install uv 
RUN uv venv
# RUN uv init fastapi-ml-project 
# RUN cd fastapi-ml-project
# RUN uv python install 3.9
# RUN uv python pin 3.9
RUN uv pip install -r requirements.txt
RUN uv pip install jupyter==1.0.0 -U && uv pip install jupyterlab==3.6.1

# Con pip
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install jupyter==1.0.0 -U && pip install jupyterlab==3.6.1


EXPOSE 8989

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8989", "-reload"]