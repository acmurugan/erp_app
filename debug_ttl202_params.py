#!/usr/bin/env python3
"""
Debug script to check TTL202 parameter passing and execution
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_ttl202_execution():
    """Debug TTL202 parameter passing and query execution"""
    try:
        print("=== TTL202 Parameter Debug Test ===")
        
        # Import the TTL202 class
        from reports.classes.ttl202 import TTL202Report
        
        # Test parameters - exactly as they would come from the form
        test_params = {
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
            'to_locn_code': 'ZZZZZZZ',
            'comp_code': 'TTM',  # Session variable
            'user_id': 'SYSTEM'  # Session variable
        }
        
        print("Test Parameters:")
        for key, value in test_params.items():
            print(f"  {key}: {value}")
        
        # Create report instance
        report = TTL202Report()
        print(f"\nReport created: {report.name}")
        
        # Test the parameter extraction manually
        print("\n=== Testing Parameter Extraction ===")
        from_cust_anly_02 = test_params.get('from_cust_anly_02', '0')
        to_cust_anly_02 = test_params.get('to_cust_anly_02', 'ZZZZZ')
        from_item_anly_12 = test_params.get('from_item_anly_12', '0')
        to_item_anly_12 = test_params.get('to_item_anly_12', 'ZZZZZZ')
        from_cust_code = test_params.get('from_cust_code', '0')
        to_cust_code = test_params.get('to_cust_code', 'ZZZZ')
        from_item_code = test_params.get('from_item_code', '0')
        to_item_code = test_params.get('to_item_code', 'ZZZZZ')
        from_date = test_params.get('from_date', '01/01/2024')
        to_date = test_params.get('to_date', '31/12/2024')
        from_locn_code = test_params.get('from_locn_code', '0')
        to_locn_code = test_params.get('to_locn_code', 'ZZZZZZZ')
        comp_code = test_params.get('comp_code', 'TTM')
        user_id = test_params.get('user_id', 'SYSTEM')
        
        print("Extracted Parameters:")
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
        print(f"  comp_code (session): {comp_code}")
        print(f"  user_id (session): {user_id}")
        
        # Test parameter mapping for query
        print("\n=== Testing Query Parameter Mapping ===")
        query_params = {
            # User parameters from form
            'M_FM_CUST_ANLY_02': from_cust_anly_02,
            'M_TO_CUST_ANLY_02': to_cust_anly_02,
            'FM_ITEM_ANLY_12': from_item_anly_12,
            'TO_ITEM_ANLY_12': to_item_anly_12,
            'M_FM_SUB_ACNT': from_cust_code,
            'M_TO_SUB_ACNT': to_cust_code,
            'M_FM_ITEM_CODE': from_item_code,
            'M_TO_ITEM_CODE': to_item_code,
            'M_AS_OF_DT': from_date,
            'M_TO_DT': to_date,
            'M_FM_LOCN_CODE': from_locn_code,
            'M_TO_LOCN_CODE': to_locn_code,
            # Session variables (GLOBAL variables from Forms 6i)
            'M_COMP_CODE': comp_code,
            'M_USER_ID': user_id
        }
        
        print("Query Parameter Mapping:")
        for key, value in query_params.items():
            print(f"  {key}: {value}")
        
        print(f"\nTotal query parameters: {len(query_params)}")
        
        # Try to execute (this will likely fail due to database connection)
        print("\n=== Attempting Report Execution ===")
        try:
            result = report.execute(test_params)
            print("Report execution completed successfully!")
            print(f"Result type: {type(result)}")
            if isinstance(result, dict):
                print(f"Columns: {result.get('count', 'N/A')}")
                print(f"Rows: {len(result.get('data', []))}")
        except Exception as e:
            print(f"Report execution failed: {e}")
            print("This is expected if database is not connected")
        
    except Exception as e:
        print(f"Debug test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_ttl202_execution()