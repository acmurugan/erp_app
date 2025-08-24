#!/usr/bin/env python3
"""
Check if parameter filtering is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reports.main_routes import build_dynamic_parameters
from database import get_db_connection

def test_ttl715_filtering():
    """Test TTL715 parameter filtering"""
    print("Testing TTL715 Parameter Filtering")
    print("=" * 40)
    
    try:
        # Simulate the parameter processing for TTL715
        print("Calling build_dynamic_parameters for TTL715...")
        
        with get_db_connection() as connection:
            cursor = connection.cursor()
            
            # Get the actual RPT_PARAMS from database
            cursor.execute("SELECT RPT_PARAMS FROM RPT_REPORT_MASTER WHERE RPT_ID = 'TTL715'")
            result = cursor.fetchone()
            
            if result and result[0]:
                import json
                rpt_params_str = result[0].read() if hasattr(result[0], 'read') else str(result[0])
                rpt_params = json.loads(rpt_params_str)
                
                print("Raw parameters from database:")
                for i, param in enumerate(rpt_params.get('parameters', [])):
                    visible = param.get('visible', True)
                    status = "VISIBLE" if visible else "HIDDEN"
                    print(f"  {i+1}. {param.get('name', 'Unknown')} - {status}")
                
                # Call the actual parameter filtering function
                filtered_params = build_dynamic_parameters('TTL715', {})
                
                print(f"\nFiltered parameters (should only show visible ones):")
                print(f"Total filtered parameters: {len(filtered_params)}")
                for i, param in enumerate(filtered_params):
                    print(f"  {i+1}. {param.get('name', 'Unknown')} (field: {param.get('field', 'N/A')})")
                
                # Check if "From Date" is filtered out
                from_date_found = any(param.get('field') == 'FM_DT' for param in filtered_params)
                
                if from_date_found:
                    print("\nERROR: 'From Date' (FM_DT) parameter found in filtered list!")
                    print("This means the visibility filtering is NOT working correctly.")
                    return False
                else:
                    print("\nSUCCESS: 'From Date' (FM_DT) parameter correctly filtered out!")
                    print("Visibility filtering is working correctly.")
                    return True
                
            else:
                print("No RPT_PARAMS found for TTL715")
                return False
                
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ttl715_filtering()
    
    if success:
        print("\nParameter filtering is working correctly!")
    else:
        print("\nParameter filtering needs to be fixed!")