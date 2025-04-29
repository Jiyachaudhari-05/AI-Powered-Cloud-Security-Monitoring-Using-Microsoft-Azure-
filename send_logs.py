import json
import base64
import hashlib
import hmac
import requests
import time
import os
from datetime import datetime
import logging

# Replace with your Azure Log Analytics details
WORKSPACE_ID = ""
SHARED_KEY = ""
LOG_TYPE = "DjangoLoginActivity_CL"  # Custom log type for your Django login activity
# Set up logging to log to a file
logging.basicConfig(filename='send_logs.log', level=logging.INFO)

# Log the start of the script
logging.info('Script started at {}'.format(datetime.now()))

try:
    # Your existing code logic here, for example:
    # Check login activity, send data to Azure, etc.
    
    # Example log inside the main script logic
    logging.info('Processing user login activities...')

    # Your core logic for sending logs or performing actions
    # For example:
    # send_logs_to_azure()

    logging.info('Successfully sent logs to Azure at {}'.format(datetime.now()))
    
except Exception as e:
    # Log any errors that occur
    logging.error('An error occurred at {}: {}'.format(datetime.now(), str(e)))

# Log the script completion
logging.info('Script finished at {}'.format(datetime.now()))
# Function to read logs from a file (adjust the log file path as needed)
def read_logs():
    log_file = "django_security.logs"  # Path to your log file
    if not os.path.exists(log_file):
        print("Log file not found!")
        return []

    with open(log_file, "r") as f:
        lines = f.readlines()

    logs = []
    for line in lines[-10:]:  # Send only the last 10 logs, adjust as needed
        logs.append({"LogEntry": line.strip()})

    return logs

# Function to create the authorization header for HTTP Data Collector API
def create_signature(customer_id, shared_key, date, body):
    # Build the signature string
    string_to_hash = f"POST\n{len(body)}\napplication/json\nx-ms-date:{date}\n/api/logs"
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
    decoded_key = base64.b64decode(shared_key)
    hashed_string = hmac.new(decoded_key, bytes_to_hash, hashlib.sha256)
    signature = base64.b64encode(hashed_string.digest()).decode("utf-8")
    return signature

# Function to send logs to Azure Log Analytics
def send_logs():
    logs = read_logs()
    if not logs:
        print("No new logs to send.")
        return

    # Prepare the log data
    body = json.dumps(logs)
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    signature = create_signature(WORKSPACE_ID, SHARED_KEY, date, body)

    # Prepare the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SharedKey {WORKSPACE_ID}:{signature}",
        "x-ms-date": date,
        "Log-Type": LOG_TYPE
    }

    url = f"https://{WORKSPACE_ID}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
    
    # Send the logs to Azure
    response = requests.post(url, headers=headers, data=body)
    
    # Check the response
    if response.status_code == 200:
        print("Logs sent successfully!")
    else:
        print(f"Failed to send logs. Response: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_logs()
    # Set up logging to log to a file
logging.basicConfig(filename='send_logs.log', level=logging.INFO)

# Log the start of the script
logging.info('Script started at {}'.format(datetime.now()))

try:
    # Your existing code logic here, for example:
    # Check login activity, send data to Azure, etc.
    
    # Example log inside the main script logic
    logging.info('Processing user login activities...')

    # Your core logic for sending logs or performing actions
    # For example:
    # send_logs_to_azure()

    logging.info('Successfully sent logs to Azure at {}'.format(datetime.now()))
    
except Exception as e:
    # Log any errors that occur
    logging.error('An error occurred at {}: {}'.format(datetime.now(), str(e)))

# Log the script completion
logging.info('Script finished at {}'.format(datetime.now()))
