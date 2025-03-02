import subprocess
import logging

def recover_service(service_name, current_status, required_status):
    """
    Recover a service by stopping or starting it based on current and required status.
    
    Args:
        service_name (str): Name of the service to recover
        current_status (str): Current status of the service
        required_status (str): Expected/required status of the service
    
    Returns:
        dict: Recovery result with status and message
    """
    try:
        # Normalize statuses to lowercase for consistent comparison
        current_status = current_status.lower()
        required_status = required_status.lower()
        
        # Logging the recovery attempt
        logging.info(f"Attempting to recover service {service_name}. Current status: {current_status}, Required status: {required_status}")
        
        # Determine recovery action
        if current_status != required_status:
            if required_status == 'active':
                # Start the service
                result = subprocess.run(['systemctl', 'start', service_name], 
                                        capture_output=True, 
                                        text=True, 
                                        check=True)
                return {
                    'status': 'success',
                    'message': f'Service {service_name} started successfully'
                }
            elif required_status == 'inactive':
                # Stop the service
                result = subprocess.run(['systemctl', 'stop', service_name], 
                                        capture_output=True, 
                                        text=True, 
                                        check=True)
                return {
                    'status': 'success', 
                    'message': f'Service {service_name} stopped successfully'
                }
            else:
                # Invalid required status
                return {
                    'status': 'error',
                    'message': f'Invalid required status: {required_status}'
                }
        else:
            # Service is already in the required state
            return {
                'status': 'info',
                'message': f'Service {service_name} is already in {required_status} state'
            }
    
    except subprocess.CalledProcessError as e:
        # Handle subprocess errors
        logging.error(f"Error recovering service {service_name}: {e}")
        return {
            'status': 'error',
            'message': f'Failed to recover service {service_name}. Error: {e.stderr}'
        }
    except Exception as e:
        # Handle any other unexpected errors
        logging.error(f"Unexpected error recovering service {service_name}: {e}")
        return {
            'status': 'error',
            'message': f'Unexpected error recovering service {service_name}: {str(e)}'
        }