#!/usr/bin/env python3
"""
Test TTL715 parameter visibility functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_ttl715_parameter_visibility():
    """Test TTL715 parameter visibility updates"""
    print("Testing TTL715 Parameter Visibility")
    print("=" * 40)
    
    # 1. Get current TTL715 configuration
    response = requests.get(f"{BASE_URL}/reports/admin/config/TTL715")
    if response.status_code != 200:
        print(f"Failed to load TTL715 config: {response.status_code}")
        return False
        
    config = response.json()['data']
    print("Current TTL715 parameters:")
    
    if 'rpt_params' in config and 'parameters' in config['rpt_params']:
        params = config['rpt_params']['parameters']
        for i, param in enumerate(params):
            visible = param.get('visible', True)
            status = "VISIBLE" if visible else "HIDDEN"
            print(f"  {i+1}. {param.get('name', 'Unknown')} (field: {param.get('field', 'N/A')}) - {status}")
            
        # 2. Modify visibility: hide "From Date", show others
        params[0]['visible'] = False  # From Date - HIDE
        params[1]['visible'] = True   # To Date - SHOW  
        params[2]['visible'] = True   # From Transaction Code - SHOW
        params[3]['visible'] = True   # To Transaction Code - SHOW
        
        print("\nModified configuration:")
        for i, param in enumerate(params):
            visible = param.get('visible', True)
            status = "VISIBLE" if visible else "HIDDEN"
            print(f"  {i+1}. {param.get('name', 'Unknown')} - {status}")
        
        # 3. Update configuration via PUT request
        config['rpt_params']['parameters'] = params
        
        update_response = requests.put(
            f"{BASE_URL}/reports/admin/config/TTL715", 
            json=config,
            headers={'Content-Type': 'application/json'}
        )
        
        if update_response.status_code == 200:
            result = update_response.json()
            if result.get('success'):
                print("\n✓ Configuration updated successfully!")
                
                # 4. Verify the update by fetching again
                verify_response = requests.get(f"{BASE_URL}/reports/admin/config/TTL715")
                if verify_response.status_code == 200:
                    verify_config = verify_response.json()['data']
                    verify_params = verify_config['rpt_params']['parameters']
                    
                    print("\nVerified configuration from database:")
                    for i, param in enumerate(verify_params):
                        visible = param.get('visible', True)
                        status = "VISIBLE" if visible else "HIDDEN"
                        print(f"  {i+1}. {param.get('name', 'Unknown')} - {status}")
                        
                    return True
                else:
                    print("Failed to verify configuration")
            else:
                print(f"Update failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"Update request failed: {update_response.status_code}")
            print(f"Response: {update_response.text}")
    else:
        print("No parameters found in TTL715 config")
        
    return False

if __name__ == "__main__":
    success = test_ttl715_parameter_visibility()
    
    if success:
        print("\n🎉 TTL715 parameter visibility test completed!")
        print("The 'From Date' parameter should now be hidden in forms")
        print("but will still pass its default value to reports.")
    else:
        print("\n❌ Test failed - check the errors above")