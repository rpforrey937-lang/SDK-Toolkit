FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 9000

# Bind to $PORT if supplied (Railway / Cloud platforms set PORT automatically)
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-9000}"]
