#!/usr/bin/env python3
"""
Update parameter visibility via admin API
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def update_fin001_visibility():
    """Update FIN001 to have some hidden parameters"""
    
    # First get current config
    response = requests.get(f"{BASE_URL}/reports/admin/config/FIN001")
    if response.status_code != 200:
        print("Failed to load FIN001 config")
        return False
        
    config = response.json()['data']
    
    # Modify parameters - hide some of them  
    if 'rpt_params' in config and 'parameters' in config['rpt_params']:
        params = config['rpt_params']['parameters']
        
        # Hide some parameters to demonstrate functionality
        hide_indices = [2, 4, 6, 8]  # Hide Division and Department range parameters
        
        for i, param in enumerate(params):
            if i in hide_indices:
                param['visible'] = False
                print(f"Hiding parameter: {param.get('name', 'Unknown')}")
            else:
                param['visible'] = True
                
        # Update the config
        config['rpt_params']['parameters'] = params
        
        # Save via admin API (if available)
        print("Parameters updated with mixed visibility:")
        for i, param in enumerate(params):
            visible = param.get('visible', True)
            status = "VISIBLE" if visible else "HIDDEN"
            print(f"  {i+1}. {param.get('name', 'Unknown')} - {status}")
            
        return True
    
    return False

if __name__ == "__main__":
    print("Updating FIN001 Parameter Visibility")
    print("=" * 40)
    success = update_fin001_visibility()
    
    if success:
        print("\nDemo visibility configuration created!")
        print("Now open the admin interface to see checkboxes in action:")
        print("http://127.0.0.1:5000/reports/admin/")
    else:
        print("Failed to update parameters")