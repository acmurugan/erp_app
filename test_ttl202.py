#!/usr/bin/env python3
"""
Test script for TTL202 class to verify it works correctly
"""

import sys
import os

# Add the current directory to path so we can import the reports module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ttl202_class():
    """Test the TTL202 class with sample parameters"""
    try:
        print("Testing TTL202 class...")
        
        # Import the class
        from reports.classes.ttl202 import TTL202Report
        
        # Test parameters
        test_params = {
            'comp_code': 'TTM',
            'user_id': 'SYSTEM',
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
        }
        
        print("TTL202Report class imported successfully")
        print(f"Test parameters: {test_params}")
        
        # Create instance
        report = TTL202Report()
        print("TTL202Report instance created successfully")
        print(f"Report name: {report.name}")
        print(f"Report version: {report.version}")
        
        # Note: We won't actually execute the report here due to database connection issues
        # But we can verify the class structure is correct
        
        print("TTL202 class structure is valid!")
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == '__main__':
    print("Starting TTL202 class test...")
    success = test_ttl202_class()
    if success:
        print("TTL202 class test completed successfully!")
    else:
        print("TTL202 class test failed!")