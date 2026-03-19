FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies for the gateway service
COPY gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the gateway application code
COPY gateway/app.py .

# Railway expects apps to bind to $PORT; default to 8000 for local development
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
