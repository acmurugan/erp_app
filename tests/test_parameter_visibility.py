#!/usr/bin/env python3
"""
Test parameter visibility via Flask app routes
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_admin_config():
    """Test admin configuration loading"""
    print("=== Testing Admin Configuration ===")
    
    # Test FIN001 configuration
    response = requests.get(f"{BASE_URL}/reports/admin/config/FIN001")
    if response.status_code == 200:
        config = response.json()
        print(f"FIN001 config loaded successfully")
        
        if 'data' in config and 'rpt_params' in config['data']:
            params = config['data']['rpt_params'].get('parameters', [])
            print(f"Found {len(params)} parameters:")
            for i, param in enumerate(params):
                visible = param.get('visible', True)  # Default to True if not specified
                print(f"  {i+1}. {param.get('name', 'Unknown')} - Visible: {visible}")
        else:
            print("No parameters found in config")
    else:
        print(f"Failed to load FIN001 config: {response.status_code}")
    
    print()
    
    # Test TTL202 configuration  
    response = requests.get(f"{BASE_URL}/reports/admin/config/TTL202")
    if response.status_code == 200:
        config = response.json()
        print(f"TTL202 config loaded successfully")
        
        if 'data' in config and 'rpt_params' in config['data']:
            params = config['data']['rpt_params'].get('parameters', [])
            print(f"Found {len(params)} parameters:")
            for i, param in enumerate(params):
                visible = param.get('visible', True)
                print(f"  {i+1}. {param.get('name', 'Unknown')} - Visible: {visible}")
        else:
            print("No parameters found in config")
    else:
        print(f"Failed to load TTL202 config: {response.status_code}")

if __name__ == "__main__":
    print("Testing Parameter Visibility System")
    print("=" * 50)
    test_admin_config()
    print("\nNext Steps:")
    print("1. Open http://127.0.0.1:5000/reports/admin/ in browser")
    print("2. Load FIN001 or TTL202 to see visibility checkboxes")
    print("3. Toggle checkboxes to test functionality")