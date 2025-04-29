import os
import json
import requests

# Set up Azure Anomaly Detector credentials
API_KEY = ""  # Replace with your Key 1
ENDPOINT = ""  # Replace with your Endpoint

headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": API_KEY,
}

# Sample login activity data (Replace this with actual logs from AppTraces)
data = {
    "series": [
        {"timestamp": "2024-03-27T08:00:00Z", "value": 5},
        {"timestamp": "2024-03-27T09:00:00Z", "value": 3},
        {"timestamp": "2024-03-27T10:00:00Z", "value": 50},  # Anomalous login spike
        {"timestamp": "2024-03-27T11:00:00Z", "value": 4},
    ],
    "granularity": "hourly",
}

# Send data to Azure Anomaly Detector
response = requests.post(
    f"{ENDPOINT}/anomalydetector/v1.1/timeseries/entire/detect",
    headers=headers,
    json=data,
)

# Display results
if response.status_code == 200:
    results = response.json()
    for i, is_anomaly in enumerate(results["isAnomaly"]):
        print(f"Timestamp: {data['series'][i]['timestamp']} - Anomaly: {is_anomaly}")
else:
    print(f"Error: {response.status_code}, {response.text}")
