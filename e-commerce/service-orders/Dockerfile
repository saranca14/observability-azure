FROM python:3.9-slim-buster
WORKDIR /app
RUN pip install --no-cache-dir opentelemetry-distro
RUN opentelemetry-bootstrap --action=install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY templates/ templates/
ENV OTEL_SERVICE_NAME="orders-service"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-collector.default.svc.cluster.local:4317"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
ENV OTEL_TRACES_EXPORTER="otlp"
ENV OTEL_METRICS_EXPORTER="otlp"
ENV OTEL_LOGS_EXPORTER="otlp"
ENV OTEL_RESOURCE_ATTRIBUTES="deployment.environment=production"
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
CMD ["opentelemetry-instrument", "python", "app.py"]