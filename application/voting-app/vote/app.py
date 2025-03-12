from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging
import atexit

from opentelemetry import trace, metrics
from opentelemetry.trace import set_tracer_provider, Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_INSTANCE_ID

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Context Propagation
from opentelemetry.propagate import inject
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


# Define OpenTelemetry Tracer
resource = Resource.create({
    SERVICE_NAME: "vote-service",  # Unique name for THIS microservice (the voting frontend)
    SERVICE_INSTANCE_ID: f"vote-service-{socket.gethostname()}",  # Unique instance ID using hostname
    "application.name": "voting-app", # Consistent application name
})

tracer_provider = TracerProvider(resource=resource)
span_exporter = OTLPSpanExporter(endpoint="otel-collector.default.svc.cluster.local:4317")
span_processor = BatchSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# Define OpenTelemetry Metrics
metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="otel-collector.default.svc.cluster.local:4317"))
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Configure logging for OpenTelemetry - generally, don't need to do this if you are using a framework's logging
# logging.basicConfig(level=logging.INFO)

# Ensure proper shutdown
def shutdown_tracer():
    span_processor.shutdown()
    tracer_provider.shutdown()

atexit.register(shutdown_tracer)


# Use a composite propagator that includes TraceContext (for general compatibility) and B3 (for Zipkin)
propagator = CompositePropagator([TraceContextTextMapPropagator(), B3MultiFormat()])

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
RedisInstrumentor().instrument()

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5, decode_responses=True) #decode_response=True for string
    return g.redis

@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote) # Use Flask's logger

        # Create a carrier dictionary to hold the context
        carrier = {}
        # Inject the current context into the carrier
        inject(carrier)

        # Add the carrier to the data being sent to Redis
        data = json.dumps({'voter_id': voter_id, 'vote': vote, 'traceparent': carrier.get('traceparent')}) #Add the trace
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=os.getenv('OPTION_A', "Cats"),
        option_b=os.getenv('OPTION_B', "Dogs"),
        hostname=socket.gethostname(),
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)