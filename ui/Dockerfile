# Image de l'interface Streamlit (séparée de l'API : elle ne parle qu'à l'API en HTTP).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY ui/requirements.txt .
RUN pip install -r requirements.txt

COPY ui/streamlit_app.py .

RUN useradd --create-home appuser
USER appuser

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
