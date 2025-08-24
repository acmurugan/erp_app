#!/usr/bin/env python3
"""
Direct database fix for FIN001 parameters
This script will directly update the database to restore FIN001 parameters
"""

import json
import sys
import os

# Add the current directory to the path to import the database module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_db_connection():
    """Get database connection using the app's database module"""
    try:
        from database import get_db_connection as get_db_conn
        return get_db_conn()
    except ImportError:
        print("Error: Could not import database module")
        return None
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# FIN001 correct configuration
fin001_params = {
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

def fix_fin001():
    """Fix FIN001 configuration directly in database"""
    connection = get_db_connection()
    if not connection:
        print("Error: Could not connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Convert parameters to JSON string
        rpt_params_json = json.dumps(fin001_params, indent=2)
        
        # Update query
        update_query = """
        UPDATE RPT_REPORT_MASTER 
        SET RPT_PARAMS = :rpt_params
        WHERE RPT_ID = 'FIN001'
        """
        
        cursor.execute(update_query, {'rpt_params': rpt_params_json})
        
        if cursor.rowcount > 0:
            connection.commit()
            print("FIN001 parameters restored successfully!")
            print(f"Updated {cursor.rowcount} row(s)")
            print("FIN001 should now work correctly.")
            return True
        else:
            print("No rows updated - FIN001 record may not exist")
            return False
            
    except Exception as e:
        print(f"Error updating FIN001: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Fixing FIN001 parameters directly in database...")
    success = fix_fin001()
    
    if success:
        print("\nFix completed successfully!")
        print("You can now test FIN001 report - it should show the parameter form correctly.")
    else:
        print("\nFix failed. Please check the error messages above.")