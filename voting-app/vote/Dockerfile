# Base stage: Uses the official Python runtime image
FROM python:3.11-slim AS base

# Add curl for healthcheck and debugging
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Set the application directory
WORKDIR /usr/local/app

# Install our requirements.txt
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Development stage
FROM base AS dev
RUN pip install watchdog
ENV FLASK_ENV=development
CMD ["python", "app.py"]

# Final production stage
FROM base AS final

# Copy our application code
COPY . .


# Expose port 80
EXPOSE 80

# Set OpenTelemetry environment variables
ENV OTEL_SERVICE_NAME=voting-app \
    OTEL_SERVICE_INSTANCE_ID=voting-service \
    OTEL_EXPORTER_OTLP_ENDPOINT=otel-collector.default.svc.cluster.local:4318 \
    OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    OTEL_EXPORTER_OTLP_INSECURE=true \
    OTEL_LOG_LEVEL=debug \
    OTEL_PYTHON_LOG_CORRELATION=true

# Run the application with Gunicorn and OpenTelemetry
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]
