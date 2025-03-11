# --- Builder Stage (for grpc_health_probe) ---
  FROM alpine/git AS builder
  RUN apk --no-cache add grpc-health-probe
  
  # --- Final Stage (Python application) ---
  FROM python:3.9-slim-buster
  
  WORKDIR /app
  
  # Install curl and telnet (for troubleshooting)
  RUN apt-get update && apt-get install -y --no-install-recommends curl telnet
  
  # Copy grpc_health_probe from the builder stage
  COPY --from=builder /usr/bin/grpc_health_probe /usr/bin/grpc_health_probe
  
  COPY requirements.txt requirements.txt
  RUN pip install --no-cache-dir -r requirements.txt
  
  COPY app.py .
  COPY templates/ templates/
  
  # --- Environment Variables ---
  ENV OTEL_SERVICE_NAME="frontend-service"
  ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-collector.e-commerce.svc.cluster.local:4317"
  ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
  # Explicitly set timeouts (important for troubleshooting)
  ENV OTEL_EXPORTER_OTLP_TIMEOUT="30"
  # Explicitly disable compression (for troubleshooting)
  ENV OTEL_EXPORTER_OTLP_COMPRESSION="none"
  # Ensure no headers are set unintentionally
  ENV OTEL_EXPORTER_OTLP_HEADERS=""
  
  ENV OTEL_RESOURCE_ATTRIBUTES="deployment.environment=production,service.instance.id=$(hostname),application.name=e-commerce"
  ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"
  # Enable OpenTelemetry SDK debug logging (VERY IMPORTANT)
  ENV OTEL_LOG_LEVEL=debug
  
  EXPOSE 80
  
  # Use a simpler, more direct command (easier to debug)
  CMD ["python", "app.py"]
  