# Dockerfile for custom exporter
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY exporter.py .

CMD ["python", "exporter.py"]