#!/usr/bin/env python3
"""
Direct fix for FIN001 parameters via admin API
This script will call the admin API to restore the correct parameters
"""

import requests
import json

# FIN001 correct configuration
fin001_config = {
    "rpt_id": "FIN001",
    "rpt_name": "Trial Balance Report",
    "rpt_desc": "Trial Balance Report with GLOBAL variable support",
    "rpt_type": "CLASS",
    "rpt_source": "FIN001",
    "rpt_params": {
        "parameters": [
            {"name": "From Period", "field": "M_FM_YYYYMM", "type": "text", "required": True, "default": "202501"},
            {"name": "To Period", "field": "M_TO_YYYYMM", "type": "text", "required": True, "default": "202512"},
            {"name": "From Division", "field": "M_FM_DIVN", "type": "text", "required": True, "default": "0"},
            {"name": "To Division", "field": "M_TO_DIVN", "type": "text", "required": True, "default": "ZZZZZZ"},
            {"name": "From Department", "field": "M_FM_DEPT", "type": "text", "required": True, "default": "0"},
            {"name": "To Department", "field": "M_TO_DEPT", "type": "text", "required": True, "default": "ZZZZZZ"},
            {"name": "From Main Account", "field": "M_FM_MAIN_AC", "type": "text", "required": True, "default": "0"},
            {"name": "To Main Account", "field": "M_TO_MAIN_AC", "type": "text", "required": True, "default": "ZZZZZZ"},
            {"name": "From Sub Account", "field": "M_FM_SUB_AC", "type": "text", "required": True, "default": "0"},
            {"name": "To Sub Account", "field": "M_TO_SUB_AC", "type": "text", "required": True, "default": "ZZZZZZ"}
        ],
        "display_columns": [],
        "column_headers": {
            "ABAL_COMP_CODE": "Company Code",
            "ABAL_ACNT_YEAR": "Account Year",
            "ABAL_MAIN_ACNT_CODE": "Main Account Code",
            "MAIN_ACNT_NAME": "Main Account Name",
            "PBC_SUB_ACNT_CODE": "PBC Sub Account Code",
            "ABAL_SUB_ACNT_CODE": "Sub Account Code",
            "SUB_ACNT_NAME": "Sub Account Name",
            "ABAL_DIVN_CODE": "Division Code",
            "DIVN_NAME": "Division Name",
            "ABAL_DEPT_CODE": "Department Code",
            "DEPT_NAME": "Department Name",
            "MONTH_BAL_01": "January Balance",
            "MONTH_BAL_02": "February Balance",
            "MONTH_BAL_03": "March Balance",
            "MONTH_BAL_04": "April Balance",
            "MONTH_BAL_05": "May Balance",
            "MONTH_BAL_06": "June Balance",
            "MONTH_BAL_07": "July Balance",
            "MONTH_BAL_08": "August Balance",
            "MONTH_BAL_09": "September Balance",
            "MONTH_BAL_10": "October Balance",
            "MONTH_BAL_11": "November Balance",
            "MONTH_BAL_12": "December Balance",
            "OP_BAL": "Opening Balance",
            "CLO_BAL": "Closing Balance"
        },
        "hidden_columns": [],
        "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
        "global_variables": {
            "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
            "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
        }
    }
}

def fix_fin001():
    """Fix FIN001 configuration via admin API"""
    url = "http://localhost:5000/reports/admin/config/FIN001"
    
    try:
        # Make the PUT request to update FIN001
        response = requests.put(url, json=fin001_config, 
                              headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("FIN001 parameters restored successfully!")
                print("FIN001 should now work correctly.")
                return True
            else:
                print(f"API returned error: {result.get('error')}")
                return False
        else:
            print(f"HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to localhost:5000")
        print("   Make sure the Flask application is running")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Fixing FIN001 parameters...")
    success = fix_fin001()
    
    if success:
        print("\nFix completed successfully!")
        print("You can now test FIN001 report - it should show the parameter form correctly.")
    else:
        print("\nFix failed. Please check the error messages above.")