# Service Status Monitoring and Auto-Healing Script

## Overview

This Python script provides a service monitoring and auto-healing solution. It allows you to:
- Check the status of multiple services
- Compare current service status against expected status
- Automatically attempt to recover services that are not in the expected state

## Features

- Configuration-driven service monitoring
- Logging of service statuses and recovery attempts
- Easy to extend and customize

## Prerequisites

- Python 3.7+
- Required Python packages:
  - PyYAML
  - Custom `system_service` module

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `config.yaml` file with the following structure:

```yaml
metrics_logger:
  level: INFO
  file: service_monitoring.log

services:
  - name: service1
    expected_status: running
  - name: service2
    expected_status: active
```

### Configuration Parameters

- `metrics_logger`: Logging configuration
  - `level`: Logging level (DEBUG, INFO, WARNING, ERROR)
  - `file`: Log file path

- `services`: List of services to monitor
  - `name`: Service name
  - `expected_status`: Desired service status (active or inactive)

## Usage

Run the script directly:

```bash
python main.py
```

The script will:
1. Load configuration from `config.yaml`
2. Check status of each configured service
3. Log service statuses
4. Attempt to recover services not in expected status
5. Log recovery results

## Logging

Logs are written to the file specified in the configuration, providing:
- Service status information
- Recovery attempt details
- Error messages

## Customization

- Modify `config.yaml` to add or change monitored services
- Extend `system_service` module to support more recovery mechanisms

## Error Handling

- Exits with an error if configuration file is missing or invalid
- Logs detailed error messages for failed service recoveries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.