FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# OpenTelemetry Auto-Instrumentation Environment Variables
ENV OTEL_SERVICE_NAME="orders-service"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-collector.default.svc.cluster.local:4317"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
# For auto-instrumentation, we use the entrypoint provided by opentelemetry-instrumentation
ENV OTEL_TRACES_EXPORTER="otlp"
ENV OTEL_METRICS_EXPORTER="otlp"
ENV OTEL_LOGS_EXPORTER="otlp"
ENV OTEL_RESOURCE_ATTRIBUTES="deployment.environment=production"


CMD ["opentelemetry-instrument", "python", "app.py"]