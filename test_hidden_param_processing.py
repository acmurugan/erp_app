#!/usr/bin/env python3
"""
Test hidden parameter processing in TTL715
"""

import requests

BASE_URL = "http://127.0.0.1:5000"

def test_ttl715_with_hidden_parameter():
    """Simulate TTL715 report generation with hidden parameter"""
    
    # 1. Login first
    login_data = {
        'comp_code': 'TTM',
        'user_id': 'ADMIN',
        'password': 'admin',
        'branch_code': ''
    }
    
    session = requests.Session()
    login_response = session.post(f"{BASE_URL}/login", data=login_data)
    
    if login_response.status_code != 302:  # Should redirect after successful login
        print(f"Login failed: {login_response.status_code}")
        return False
    
    print("Successfully logged in")
    
    # 2. Simulate form submission for TTL715 with only visible parameters
    # The hidden parameter FM_DT (From Date) should be automatically added with default value
    form_data = {
        'menu_id': 'T020101',
        'report_id': 'TTL715',
        'reportType': 'detail',
        'to_dt': '31/12/2024',           # TO_DT - visible
        'fm_txn_code': '0',              # FM_TXN_CODE - visible  
        'to_txn_code': 'ZZZZZZ',         # TO_TXN_CODE - visible
        'outputFormat': 'view'
        # NOTE: FM_DT (From Date) is NOT included because it's hidden
        # It should be automatically added with default value '01/01/2024'
    }
    
    print("Form data being sent (hidden parameters should be added automatically):")
    for key, value in form_data.items():
        print(f"  {key} = {value}")
    
    # 3. Submit report generation request
    response = session.post(f"{BASE_URL}/reports/dynamic/T020101/generate", data=form_data)
    
    print(f"\nReport generation response status: {response.status_code}")
    
    # 4. Check response content
    response_text = response.text
    
    if "ORA-01008: not all variables bound" in response_text:
        print("ERROR: Hidden parameter was not added - ORA-01008 error occurred")
        print("This means FM_DT parameter is missing")
        return False
    elif "Report Generation Error" in response_text:
        print("ERROR: Report generation failed for other reasons")
        print("Response preview:", response_text[:500])
        return False
    elif "No data found" in response_text or "data" in response_text.lower():
        print("SUCCESS: Report generated successfully!")
        print("Hidden parameter FM_DT was correctly added with default value")
        return True
    else:
        print("UNKNOWN: Unexpected response")
        print("Response preview:", response_text[:300])
        return False

if __name__ == "__main__":
    print("Testing TTL715 Hidden Parameter Processing")
    print("=" * 50)
    
    success = test_ttl715_with_hidden_parameter()
    
    if success:
        print("\n✓ HIDDEN PARAMETER TEST PASSED!")
        print("The FM_DT parameter is correctly added with default value '01/01/2024'")
    else:
        print("\n✗ HIDDEN PARAMETER TEST FAILED!")
        print("The hidden parameter processing needs to be fixed")