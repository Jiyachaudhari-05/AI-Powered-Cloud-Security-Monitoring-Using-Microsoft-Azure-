import json
import requests
import datetime
import hashlib
import hmac
import base64

# Replace with your values
WORKSPACE_ID = ""
SHARED_KEY = ""
LOG_TYPE = "DjangoLoginActivity"

# Create a sample log entry
log_data = [{
    "time": datetime.datetime.utcnow().isoformat() + "Z",
    "level": "INFO",
    "message": "Test log: User 'jiya' logged in from 127.0.0.1",
    "status_code": "200",
    "user": "jiya",
    "ip_address": "127.0.0.1"
}]

body = json.dumps(log_data)
content_length = len(body)
method = "POST"
content_type = "application/json"
resource = "/api/logs"
rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

# Create signature
string_to_hash = f"{method}\n{content_length}\n{content_type}\n{rfc1123date}\n{resource}"
decoded_key = base64.b64decode(SHARED_KEY)
hashed_string = hmac.new(decoded_key, string_to_hash.encode('utf-8'), hashlib.sha256).digest()
signature = base64.b64encode(hashed_string).decode()

headers = {
    "Content-Type": content_type,
    "Authorization": f"SharedKey {WORKSPACE_ID}:{signature}",
    "Log-Type": LOG_TYPE,
    "x-ms-date": rfc1123date,
    "time-generated-field": "time"
}

# Send data to Azure
url = f"https://{WORKSPACE_ID}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
response = requests.post(url, headers=headers, data=body)

print("Response Code:", response.status_code)
print("Response Text:", response.text)
