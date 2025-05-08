from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def init_telemetry(service_name):
    resource = Resource.create(attributes={"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

    RequestsInstrumentor().instrument()