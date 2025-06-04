from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def init_telemetry(service_name):
    resource = Resource.create(attributes={"service.name": service_name})

    # Set up the OTLP exporter for traces
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))
    
    # Set up the OTLP exporter for metrics
    metrics_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4318/v1/metrics")
    metric_reader = PeriodicExportingMetricReader(metrics_exporter, export_interval_millis=100)
    m_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(m_provider)

    RequestsInstrumentor().instrument()