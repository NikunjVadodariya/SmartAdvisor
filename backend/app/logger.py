"""Logging configuration for SmartAdvisor."""
import logging
import os
from datetime import datetime
from pathlib import Path
from app.config import settings


def setup_logging():
    """Configure application logging."""
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("smartadvisor")
    return logger


logger = setup_logging()

