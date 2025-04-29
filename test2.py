import requests

url = "http://127.0.0.1:8000/accounts/send-email/"
data = {
    "email": "test@example.com",
    "subject": "Test Email",
    "message": "Hello, this is a test!"
}

response = requests.post(url, json=data)  # Send POST request
print(response.json())  # Print server response
