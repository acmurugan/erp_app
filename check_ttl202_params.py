#!/usr/bin/env python3
"""
Script to check and update TTL202 RPT_PARAMS to remove GLOBAL variables
"""

from database import get_db_connection
import json
import traceback

def check_and_update_ttl202():
    """Check current RPT_PARAMS and update to remove GLOBAL variables"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get current RPT_PARAMS
            cursor.execute("SELECT RPT_PARAMS FROM RPT_REPORT_MASTER WHERE RPT_ID = 'TTL202'")
            result = cursor.fetchone()
            
            if result and result[0]:
                print("[INFO] Found RPT_PARAMS for TTL202")
                
                # Read CLOB data
                params_data = result[0]
                if hasattr(params_data, 'read'):
                    params_data = params_data.read()
                
                print(f"[INFO] RPT_PARAMS length: {len(params_data)}")
                
                try:
                    # Parse JSON
                    json_data = json.loads(params_data)
                    
                    if 'parameters' in json_data:
                        print("[INFO] Current parameters in database:")
                        for key in json_data['parameters'].keys():
                            print(f"  - {key}")
                        
                        # Check if GLOBAL variables exist
                        global_vars = ['comp_code', 'user_id', 'M_COMP_CODE', 'M_USER_ID']
                        has_global_vars = any(key in json_data['parameters'] for key in global_vars)
                        
                        if has_global_vars:
                            print("[INFO] Found GLOBAL variables in parameters, removing them...")
                            
                            # Remove GLOBAL variables
                            for var in global_vars:
                                if var in json_data['parameters']:
                                    del json_data['parameters'][var]
                                    print(f"[INFO] Removed {var}")
                            
                            # Update parameter count
                            json_data['metadata']['parameter_count'] = len(json_data['parameters'])
                            json_data['metadata']['updated_date'] = "2024-08-22T12:00:00Z"
                            json_data['metadata']['update_reason'] = "Removed GLOBAL session variables"
                            
                            # Convert back to JSON
                            updated_json = json.dumps(json_data, indent=2)
                            
                            # Update database
                            cursor.execute("""
                                UPDATE RPT_REPORT_MASTER 
                                SET RPT_PARAMS = ? 
                                WHERE RPT_ID = 'TTL202'
                            """, (updated_json,))
                            
                            conn.commit()
                            print("[SUCCESS] Updated RPT_PARAMS - removed GLOBAL variables")
                            print(f"[INFO] New parameter count: {len(json_data['parameters'])}")
                            
                            # Show remaining parameters
                            print("[INFO] Remaining parameters:")
                            for key in json_data['parameters'].keys():
                                print(f"  - {key}")
                                
                        else:
                            print("[INFO] No GLOBAL variables found in parameters - no update needed")
                    
                except json.JSONDecodeError as e:
                    print(f"[ERROR] Could not parse RPT_PARAMS as JSON: {e}")
                    print(f"[INFO] Raw content preview: {params_data[:200]}...")
                    
            else:
                print("[WARNING] No RPT_PARAMS found for TTL202")
                
    except Exception as e:
        print(f"[ERROR] Error checking/updating TTL202 RPT_PARAMS: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    print("Starting TTL202 RPT_PARAMS check and update...")
    check_and_update_ttl202()
    print("Done!")