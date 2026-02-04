#!/usr/bin/env python3
import json
import requests

# Load credentials
with open('/Users/administrator/.openclaw/credentials/alpaca-paper.json') as f:
    creds = json.load(f)

# Test connection
headers = {
    'APCA-API-KEY-ID': creds['apiKey'],
    'APCA-API-SECRET-KEY': creds['secretKey']
}

# Get account info
response = requests.get(
    f"{creds['baseUrl']}/v2/account",
    headers=headers
)

if response.status_code == 200:
    account = response.json()
    print("✓ Connection successful!")
    print(f"Account Status: {account['status']}")
    print(f"Cash: ${account['cash']}")
    print(f"Buying Power: ${account['buying_power']}")
    print(f"Portfolio Value: ${account['portfolio_value']}")
else:
    print(f"✗ Connection failed: {response.status_code}")
    print(response.text)
