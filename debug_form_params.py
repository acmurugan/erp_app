#!/usr/bin/env python3
"""
Debug script to check what parameters the form system actually sends vs what TTL202 expects
"""

import json

def debug_form_parameters():
    """Debug what parameters come from the form vs what TTL202 expects"""
    
    print("=== FORM PARAMETER FORMAT DEBUG ===")
    
    # Simulate what comes from the web form (likely from RPT_PARAMS in database)
    # This is what the form sends based on the parameter names in the database
    form_params_from_web = {
        'from_cust_anly_02': '0',
        'to_cust_anly_02': 'ZZZZZ', 
        'from_item_anly_12': '0',
        'to_item_anly_12': 'ZZZZZZ',
        'from_cust_code': '0',
        'to_cust_code': 'ZZZZ',
        'from_item_code': '0', 
        'to_item_code': 'ZZZZZ',
        'from_date': '01/01/2024',
        'to_date': '31/12/2024',
        'from_locn_code': '0',
        'to_locn_code': 'ZZZZZZZ'
        # NOTE: comp_code and user_id should come from session, not form
    }
    
    print("Parameters that come from the WEB FORM:")
    for key, value in form_params_from_web.items():
        print(f"  {key}: {value}")
    
    print(f"\nTotal form parameters: {len(form_params_from_web)}")
    
    # What TTL202.py expects and how it maps them
    print("\n=== TTL202.PY PARAMETER MAPPING ===")
    
    # Simulate session data (this should be added by the system)
    session_data = {
        'comp_code': 'TTM',  # From user session
        'user_id': 'SYSTEM'  # From user session  
    }
    
    print("Session variables (added by system):")
    for key, value in session_data.items():
        print(f"  {key}: {value}")
    
    # Combined parameters (form + session)
    combined_params = {**form_params_from_web, **session_data}
    
    print(f"\nCOMBINED PARAMETERS (form + session): {len(combined_params)} total")
    for key, value in combined_params.items():
        print(f"  {key}: {value}")
    
    # Test TTL202 parameter extraction
    print("\n=== TTL202 PARAMETER EXTRACTION TEST ===")
    
    # This is exactly what TTL202.py does
    from_cust_anly_02 = combined_params.get('from_cust_anly_02', '0')
    to_cust_anly_02 = combined_params.get('to_cust_anly_02', 'ZZZZZ')
    from_item_anly_12 = combined_params.get('from_item_anly_12', '0')
    to_item_anly_12 = combined_params.get('to_item_anly_12', 'ZZZZZZ')
    from_cust_code = combined_params.get('from_cust_code', '0')
    to_cust_code = combined_params.get('to_cust_code', 'ZZZZ')
    from_item_code = combined_params.get('from_item_code', '0')
    to_item_code = combined_params.get('to_item_code', 'ZZZZZ')
    from_date = combined_params.get('from_date', '01/01/2024')
    to_date = combined_params.get('to_date', '31/12/2024')
    from_locn_code = combined_params.get('from_locn_code', '0')
    to_locn_code = combined_params.get('to_locn_code', 'ZZZZZZZ')
    comp_code = combined_params.get('comp_code', 'TTM')
    user_id = combined_params.get('user_id', 'SYSTEM')
    
    print("Extracted values:")
    print(f"  from_cust_anly_02: {from_cust_anly_02}")
    print(f"  to_cust_anly_02: {to_cust_anly_02}")
    print(f"  from_item_anly_12: {from_item_anly_12}")
    print(f"  to_item_anly_12: {to_item_anly_12}")
    print(f"  from_cust_code: {from_cust_code}")
    print(f"  to_cust_code: {to_cust_code}")
    print(f"  from_item_code: {from_item_code}")
    print(f"  to_item_code: {to_item_code}")
    print(f"  from_date: {from_date}")
    print(f"  to_date: {to_date}")
    print(f"  from_locn_code: {from_locn_code}")
    print(f"  to_locn_code: {to_locn_code}")
    print(f"  comp_code: {comp_code}")
    print(f"  user_id: {user_id}")
    
    # Check if any are None or missing
    all_params = [
        from_cust_anly_02, to_cust_anly_02, from_item_anly_12, to_item_anly_12,
        from_cust_code, to_cust_code, from_item_code, to_item_code,
        from_date, to_date, from_locn_code, to_locn_code, comp_code, user_id
    ]
    
    missing_params = [i for i, param in enumerate(all_params) if param is None or param == '']
    if missing_params:
        print(f"\n[ERROR] MISSING PARAMETERS: {len(missing_params)} parameters are None or empty!")
        param_names = ['from_cust_anly_02', 'to_cust_anly_02', 'from_item_anly_12', 'to_item_anly_12',
                      'from_cust_code', 'to_cust_code', 'from_item_code', 'to_item_code',
                      'from_date', 'to_date', 'from_locn_code', 'to_locn_code', 'comp_code', 'user_id']
        for idx in missing_params:
            print(f"  Missing: {param_names[idx]}")
    else:
        print(f"\n[SUCCESS] ALL PARAMETERS OK: All 14 parameters have values")
    
    print(f"\n=== POSSIBLE ISSUES ===")
    print("1. Check if the web form is sending parameters with correct names")
    print("2. Check if session variables (comp_code, user_id) are being added")  
    print("3. Check if parameter names match between form and TTL202.py")
    print("4. Check database RPT_PARAMS parameter names vs TTL202.py expectations")
    
    return combined_params

if __name__ == '__main__':
    debug_form_parameters()