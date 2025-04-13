# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./app ./app

# Expose FastAPI port
EXPOSE 8010

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
