import os
import json
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from monocle_apptrace import setup_monocle_telemetry
from monocle_apptrace.exporters.base_exporter import serialize_span

class JsonlSpanExporter(SpanExporter):
    """Custom OpenTelemetry Exporter that appends traces to a single JSONL file."""
    def __init__(self, filepath):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
    def export(self, spans):
        try:
            with open(self.filepath, 'a') as f:
                for span in spans:
                    # Serialize the standard OTel span into Monocle's rich JSON format
                    span_data = serialize_span(span)
                    f.write(json.dumps(span_data) + "\n")
            return SpanExportResult.SUCCESS
        except Exception as e:
            print(f"Error writing to JSONL: {e}")
            return SpanExportResult.FAILURE

    def shutdown(self):
        pass

def setup_logger(name="hospital_system"):
    # 1. Set up the Global Tracer Provider with our Custom JSONL Exporter
    provider = TracerProvider(resource=Resource(attributes={SERVICE_NAME: name}))
    
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    jsonl_path = os.path.join(log_dir, "traces.jsonl")
    
    jsonl_exporter = JsonlSpanExporter(jsonl_path)
    provider.add_span_processor(BatchSpanProcessor(jsonl_exporter))
    
    trace.set_tracer_provider(provider)

    # 2. Configure Monocle to natively export to Jaeger (OTLP) and suppress its multi-file generation.
    os.environ["MONOCLE_EXPORTER"] = "otlp"
    setup_monocle_telemetry(workflow_name=name)

# Automatically initialize telemetry when this module is imported by any server or UI
setup_logger()
