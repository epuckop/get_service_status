import sys
import yaml
import logging
from system_service import service_status
from system_service.service_recovery import recover_service
from system_service.service_logger import setup_logger

def load_config(config_path='./config.yaml'):
    """
    Load configuration from YAML file.    
    Args: 
        config_path (str): Path to the configuration file    
    Returns:
        dict: Parsed configuration
    Raises:
        SystemExit: If config file is not found or cannot be parsed
    """
    try:
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
        sys.exit(1)

def main():
    # Load configuration
    config = load_config()

    # Extract logger configuration
    logger_config = config.get('metrics_logger', {})

    # Setup logger
    logger = setup_logger(logger_config)

    # Extract service configuration
    service_config = config.get('services', [])

    # Log start of service monitoring
    logger.info("Starting service monitoring")

    # Check and log status of all services from config
    for service in service_config:
        # Get current service status
        status = service_status.check_service_status(service.get('name'))
        current_service_status = status.get('status')
        
        # Log service status
        logger.info(f"Service name: {service.get('name')}, Current status: {current_service_status}, Expected status: {service.get('expected_status')}")

        # Check if service is in expected status
        if current_service_status != service.get('expected_status'):
            logger.warning(f"Service {service.get('name')} is not in expected status {service.get('expected_status')}")
            logger.info(f"Attempting to recover {service.get('name')}...")
            
            # Attempt to recover service
            recovery_result = recover_service(
                service.get('name'), 
                current_service_status, 
                service.get('expected_status')
            )
            
            # Log recovery result
            if recovery_result.get('success', False):
                logger.info(f"Recovery successful: {recovery_result.get('message')}")
            else:
                logger.error(f"Recovery failed: {recovery_result.get('message')}")

    # Log end of service monitoring
    logger.info("Service monitoring completed")

if __name__ == "__main__":
    main()