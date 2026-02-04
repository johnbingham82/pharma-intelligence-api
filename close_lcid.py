#!/usr/bin/env python3
import json
import requests

# Load credentials
with open('/Users/administrator/.openclaw/credentials/alpaca-paper.json') as f:
    creds = json.load(f)

base_url = creds['baseUrl']
headers = {
    'APCA-API-KEY-ID': creds['apiKey'],
    'APCA-API-SECRET-KEY': creds['secretKey']
}

# Close LCID position
print("Closing LCID position...")
response = requests.delete(f"{base_url}/v2/positions/LCID", headers=headers)

if response.status_code == 200:
    print("✅ LCID position closed successfully!")
    print(f"Response: {response.json()}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
