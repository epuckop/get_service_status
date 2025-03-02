import os
import json
import logging
import time
from datetime import datetime

def setup_logger(logger_config):
    """
    Set up a logger based on configuration.
    
    Args:
        logger_config (dict): Logger configuration from config file
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Ensure log directory exists
    log_dir = logger_config.get('log_dir', './logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename with current date
    log_filename = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')
    
    # Create logger
    logger = logging.getLogger('metrics_logger')
    
    # Set log level based on configuration
    log_level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    log_level = log_level_map.get(logger_config.get('level', 'INFO').upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Clear any existing handlers to prevent duplicate logging
    logger.handlers.clear()
    
    # Choose log format
    log_format = logger_config.get('log_format', 'text')
    
    if log_format == 'json':
        # JSON log formatter with Unix and ISO timestamps
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                # Get current time
                current_time = time.time()
                
                log_record = {
                    'unix_timestamp': int(current_time),
                    'iso_timestamp': datetime.fromtimestamp(current_time).isoformat(),
                    'level': record.levelname,
                    'message': record.getMessage()
                }
                return json.dumps(log_record)
        
        file_handler = logging.FileHandler(log_filename, mode='a')
        file_handler.setFormatter(JsonFormatter())
    else:
        # Standard text log formatter with Unix and ISO timestamps
        class TextFormatter(logging.Formatter):
            def format(self, record):
                # Get current time
                current_time = time.time()
                
                return (f"unix_timestamp: {int(current_time)} | "
                        f"iso_timestamp: {datetime.fromtimestamp(current_time).isoformat()} | "
                        f"{self._style._fmt % record.__dict__}")
        
        formatter = TextFormatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(log_filename, mode='a')
        file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    # Console handler for immediate visibility
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(file_handler.formatter)
    logger.addHandler(console_handler)
    
    return logger