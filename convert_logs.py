import logging
import json
from datetime import datetime

# Setup logging configuration
logging.basicConfig(level=logging.INFO)

# Function to log errors and info into a JSON file
def log_to_json(log_data, file_path='django_security.json'):
    try:
        # Read existing data from the JSON file
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        
        # Append new log entry
        data.append(log_data)
        
        # Write updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logging.error(f"Error while writing to JSON file: {e}")

# Example logs
log_data = {
    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
    "level": "INFO",
    "message": "Watching for file changes with StatReloader"
}
log_to_json(log_data)

log_data = {
    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
    "level": "WARNING",
    "message": "Failed login attempt for xcfljx from 127.0.0.1"
}
log_to_json(log_data)

log_data = {
    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
    "level": "WARNING",
    "message": "Not Found: /favicon.ico"
}
log_to_json(log_data)

logging.info("Logs updated successfully.")
