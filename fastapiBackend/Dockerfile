FROM python:3.12-slim

WORKDIR /app

# Upgrade pip securely
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies required by python packages like psycopg2 mapped to postgres
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install specific Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source maps over 
COPY . .

# Set default ports and environmental defaults
ENV PORT=8000
EXPOSE 8000

# Invoke the application server using Azure specifications
CMD ["sh", "-c", "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT}"]
