#Traces

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize tracer provider and exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export spans to an OTLP backend (e.g., OpenTelemetry Collector)
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector-endpoint")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Manually instrumenting a function
def handle_request():
    with tracer.start_as_current_span("http_request") as span:
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", "/api/data")
        try:
            # Simulate an HTTP request (e.g., make a real HTTP call here)
            response = {"data": "some data"}
            span.set_attribute("http.status_code", 200)
            span.set_status(Status(StatusCode.OK))
        except Exception as e:
            # In case of an error, mark the span with a failed status
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
        return response

# Calling the function
response = handle_request()


#Application logic below







#Metrics

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Initialize MeterProvider and exporter
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)

# Set up OTLP metric exporter to export metrics
otlp_metric_exporter = OTLPMetricExporter(endpoint="your-otel-collector-endpoint")
metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
metrics.get_meter_provider().add_metric_reader(metric_reader)

# Create a counter metric for request count
request_counter = meter.create_counter(
    name="requests_total",
    description="Total number of HTTP requests",
    unit="1",
)

# Manually instrumenting the code to count requests
def handle_request():
    # Increment the counter when a request is handled
    request_counter.add(1, attributes={"http.method": "GET", "http.url": "/api/data"})

    # Simulate handling the request
    response = {"data": "some data"}
    return response

# Calling the function
handle_request()


