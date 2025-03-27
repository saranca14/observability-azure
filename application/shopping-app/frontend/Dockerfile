FROM python:3.12-slim-bookworm AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-dev curl telnet && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/

RUN opentelemetry-bootstrap -a install

ENV OTEL_SERVICE_NAME="frontend-service"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector.obs.svc.cluster.local:4317"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"
ENV OTEL_RESOURCE_ATTRIBUTES="deployment.environment=production,service.instance.id=$(hostname),application.name=e-commerce"

EXPOSE 8080

CMD ["opentelemetry-instrument", "--traces_exporter=console,otlp", "--metrics_exporter=console,otlp", "--logs_exporter=console,otlp", "python", "app.py"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health