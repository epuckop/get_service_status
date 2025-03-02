import subprocess

def check_service_status(service_name):
    """
    Check the status of a Linux service using systemctl.
    
    Args:
        service_name (str): Name of the service to check.
    
    Returns:
        dict: A dictionary containing service status information.
    """
    try:
        # Run systemctl status command
        result = subprocess.run(
            ['systemctl', 'status', service_name], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        # Determine service status
        if result.returncode == 0:
            status = 'active'
        elif result.returncode == 3:
            status = 'inactive'
        else:
            status = 'failed'
        
        return {
            'service_name': service_name,
            'status': status,
            'full_output': result.stdout,
            'return_code': result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {
            'service_name': service_name,
            'status': 'timeout',
            'full_output': 'Service check timed out',
            'return_code': None
        }
    
    except Exception as e:
        return {
            'service_name': service_name,
            'status': 'error',
            'full_output': str(e),
            'return_code': None
        }

