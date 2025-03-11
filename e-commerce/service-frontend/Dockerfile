FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/


ENV OTEL_SERVICE_NAME="frontend-service"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-collector.e-commerce.svc.cluster.local:4317"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
# ENV OTEL_TRACES_EXPORTER="otlp"
# ENV OTEL_METRICS_EXPORTER="otlp"
# ENV OTEL_LOGS_EXPORTER="otlp"
ENV OTEL_RESOURCE_ATTRIBUTES="deployment.environment=production,service.instance.id=$(hostname),application.name=e-commerce"
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"

EXPOSE 80

CMD ["opentelemetry-instrument", "--traces_exporter=console,otlp", "--metrics_exporter=console,otlp", "--logs_exporter=console,otlp", "python", "app.py"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/health || exit 1 # Assuming /health endpoint on port 80