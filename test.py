import azure.eventhub

connection_string = "Endpoint=sb://security-logs-ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YOUR_KEY"
event_hub_name = "django-logs"

try:
    client = azure.eventhub.EventHubProducerClient.from_connection_string(connection_string, eventhub_name=event_hub_name)
    print("✅ Connection successful!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
