FROM python:3.10-slim
WORKDIR /app
COPY streamlit_ui/ /app
RUN pip install streamlit requests
CMD ["streamlit", "run", "app.py"]