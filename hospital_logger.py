import os
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[91m\033[1m', # Bold Red
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        original_message = record.getMessage()
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Agent tag for visual distinction
        agent_tag = getattr(record, 'agent', 'system')
        if agent_tag == 'HANDOFF':
            agent_str = f"\033[35m[{agent_tag:<12}]\033[0m" # Magenta for handoffs
        else:
            agent_str = f"[{agent_tag:<12}]"
            
        formatted_time = self.formatTime(record, self.datefmt)
        return f"{formatted_time} {color}[{record.levelname:<7}]{reset} {agent_str} {original_message}"

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "agent": getattr(record, 'agent', 'system'),
            "event": getattr(record, 'event', 'log'),
            "message": record.getMessage()
        }
        
        # Add any extra contextual fields
        for key in ['session_id', 'user_id', 'from_agent', 'to_agent']:
            if hasattr(record, key):
                log_data[key] = getattr(record, key)
                
        # Include exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)

def setup_logger(name=None):
    logger = logging.getLogger(name) # If name is None, this gets the Root Logger!
    logger.setLevel(logging.DEBUG)

    # Prevent adding handlers multiple times if imported multiple times
    if not logger.handlers:
        # 1. Console Handler (Colored, readable)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter('%(asctime)s %(message)s', datefmt='[%H:%M:%S]')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # 2. File Handler (JSON lines, rotating)
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "hospital_agent.log")
        
        # 5MB max size, keep 3 backups
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = JsonFormatter()
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Silence noisy third-party loggers
    logging.getLogger("a2a").setLevel(logging.WARNING)
    logging.getLogger("google.adk").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return logger

# Global logger instance
logger = setup_logger()

# Helper functions for structured logging
def log_agent_handoff(from_agent, to_agent, session_id=None):
    logger.info(
        f"{from_agent} → {to_agent}", 
        extra={
            "agent": "HANDOFF", 
            "event": "agent_transfer", 
            "from_agent": from_agent, 
            "to_agent": to_agent,
            "session_id": session_id
        }
    )

def log_event(level, agent, event_type, message, **kwargs):
    extra = {"agent": agent, "event": event_type}
    extra.update(kwargs)
    
    if level.upper() == "DEBUG":
        logger.debug(message, extra=extra)
    elif level.upper() == "INFO":
        logger.info(message, extra=extra)
    elif level.upper() == "WARNING":
        logger.warning(message, extra=extra)
    elif level.upper() == "ERROR":
        logger.error(message, extra=extra)
    else:
        logger.info(message, extra=extra)
