import os
from monocle_apptrace import setup_monocle_telemetry
import logging

def setup_logger(name="hospital_system"):
    # Initialize Monocle telemetry - automatically instruments Google ADK
    setup_monocle_telemetry(workflow_name=name)
    
    # Provide a dummy python logger so the app doesn't crash on standard logger calls
    logger = logging.getLogger(name)
    return logger

# Global logger instance
logger = setup_logger()

# Dummy helper functions to prevent Streamlit from crashing
def log_agent_handoff(from_agent, to_agent, session_id=None):
    pass

def log_event(level, agent, event_type, message, **kwargs):
    pass
