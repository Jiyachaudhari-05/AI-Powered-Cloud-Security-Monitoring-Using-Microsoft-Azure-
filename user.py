import hashlib
import hmac
import base64
import requests
import datetime
import json

WORKSPACE_ID = "b105dbe2-663d-4e18-97f9-eb6e543b6bb3"
SHARED_KEY = "hTSsLtKb6fGb3zqN04k9jCpd7LB2+6QPWysl1Z4Tbu9bNMAv0ZYvU+Vb1R48Q+n8MC7fDt1elcVG77iapAYpPQ=="

def build_signature(date, content_length, method, content_type, resource):
    x_headers = f"x-ms-date:{date}"
    string_to_hash = f"{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}"
    bytes_to_hash = bytes(string_to_hash, "utf-8")
    decoded_key = base64.b64decode(SHARED_KEY)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    return f"SharedKey {WORKSPACE_ID}:{encoded_hash}"

def send_log():
    log_type = "DjangoSecurityLogs"
    
    json_data = [{
        "TimeGenerated": datetime.datetime.utcnow().isoformat() + "Z",  # Ensure valid timestamp
        "Message": "Test log from Python",
        "EventCategory": "Authentication",
        "Status": "Success"
    }]
    
    body = json.dumps(json_data)  # Proper JSON format
    content_length = len(body)
    date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    signature = build_signature(date, content_length, "POST", "application/json", "/api/logs")

    headers = {
        "Content-Type": "application/json",
        "Authorization": signature,
        "Log-Type": log_type,  
        "x-ms-date": date,
        "time-generated-field": "TimeGenerated"  
    }

    url = f"https://{WORKSPACE_ID}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
    response = requests.post(url, headers=headers, data=body)
    print(f"Response Code: {response.status_code}")
    print(f"Response: {response.text}")

send_log()
