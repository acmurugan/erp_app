#!/usr/bin/env python3
"""
Test script to debug FIN001 API fix
"""

import requests
import json

# Test the fix with detailed debugging
url = "http://localhost:5000/reports/admin/config/FIN001"

# First, get the current config
print("=== BEFORE UPDATE ===")
response = requests.get(url)
if response.status_code == 200:
    current = response.json()
    print(f"Current parameters count: {len(current['data']['rpt_params']['parameters'])}")
    print(f"Parameters: {current['data']['rpt_params']['parameters']}")
else:
    print(f"Error getting current config: {response.status_code}")
    
# Now test the update with minimal data
test_params = {
    "rpt_id": "FIN001",
    "rpt_name": "Trial Balance Report", 
    "rpt_desc": "Trial Balance Report with GLOBAL variable support",
    "rpt_type": "CLASS",
    "rpt_source": "FIN001",
    "rpt_params": {
        "parameters": [
            {"name": "Test Parameter", "field": "TEST_FIELD", "type": "text", "required": True, "default": "test"}
        ],
        "display_columns": [],
        "column_headers": {},
        "hidden_columns": [],
        "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
        "global_variables": {
            "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
            "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
        }
    }
}

print("\n=== UPDATING ===")
print(f"Sending data: {json.dumps(test_params, indent=2)}")

response = requests.put(url, json=test_params, headers={'Content-Type': 'application/json'})
print(f"Response status: {response.status_code}")
print(f"Response text: {response.text}")

# Check if it was updated
print("\n=== AFTER UPDATE ===")
response = requests.get(url)
if response.status_code == 200:
    updated = response.json()
    print(f"Updated parameters count: {len(updated['data']['rpt_params']['parameters'])}")
    print(f"Parameters: {updated['data']['rpt_params']['parameters']}")
else:
    print(f"Error getting updated config: {response.status_code}")