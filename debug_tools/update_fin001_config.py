#!/usr/bin/env python3
"""
Update FIN001 configuration to remove session variables from parameter form
"""

from database import get_db_connection

def update_fin001_config():
    try:
        print('Updating FIN001 database configuration...')
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Delete existing FIN001
            cursor.execute("DELETE FROM RPT_REPORT_MASTER WHERE RPT_ID = 'FIN001'")
            print('Deleted existing FIN001 configuration')
            
            # Insert new FIN001 configuration
            cursor.execute('''
                INSERT INTO RPT_REPORT_MASTER (
                    RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, 
                    RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_ACTIVE_FLAG, 
                    RPT_CR_DT, RPT_CR_UID
                ) VALUES (
                    'FIN001', 'Trial Balance Report', 
                    'Trial Balance Report with GLOBAL variable support',
                    'CLASS', 'FIN001Report', 'HTML,PDF,EXCEL', 
                    'FINANCE', 'Y', SYSDATE, 'SYSTEM'
                )
            ''')
            print('Inserted basic FIN001 record')
            
            # Update with parameter configuration (only user input fields, no session variables)
            params_json = '''{
  "parameters": [
    {"name": "From Period", "field": "M_FM_YYYYMM", "type": "text", "required": true, "default": "202501"},
    {"name": "To Period", "field": "M_TO_YYYYMM", "type": "text", "required": true, "default": "202512"},
    {"name": "From Division", "field": "M_FM_DIVN", "type": "text", "required": true, "default": "0"},
    {"name": "To Division", "field": "M_TO_DIVN", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Department", "field": "M_FM_DEPT", "type": "text", "required": true, "default": "0"},
    {"name": "To Department", "field": "M_TO_DEPT", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Main Account", "field": "M_FM_MAIN_AC", "type": "text", "required": true, "default": "0"},
    {"name": "To Main Account", "field": "M_TO_MAIN_AC", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Sub Account", "field": "M_FM_SUB_AC", "type": "text", "required": true, "default": "0"},
    {"name": "To Sub Account", "field": "M_TO_SUB_AC", "type": "text", "required": true, "default": "ZZZZZZ"}
  ],
  "display_columns": [],
  "column_headers": {},
  "hidden_columns": [],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'''
            
            cursor.execute("UPDATE RPT_REPORT_MASTER SET RPT_PARAMS = :params WHERE RPT_ID = 'FIN001'", 
                          {'params': params_json})
            print('Updated FIN001 parameters configuration')
            
            # Commit changes
            conn.commit()
            print('Changes committed')
            
            # Verify configuration
            cursor.execute("SELECT RPT_ID, RPT_NAME, RPT_SOURCE FROM RPT_REPORT_MASTER WHERE RPT_ID = 'FIN001'")
            result = cursor.fetchone()
            if result:
                print(f'SUCCESS: FIN001 updated - ID: {result[0]}, Name: {result[1]}, Source: {result[2]}')
                
                # Also check parameters
                cursor.execute("SELECT RPT_PARAMS FROM RPT_REPORT_MASTER WHERE RPT_ID = 'FIN001'")
                params_result = cursor.fetchone()
                if params_result and params_result[0]:
                    import json
                    params_obj = json.loads(params_result[0].read() if hasattr(params_result[0], 'read') else params_result[0])
                    print(f'Parameter count: {len(params_obj.get("parameters", []))}')
                    for param in params_obj.get("parameters", []):
                        print(f'  - {param.get("name")} ({param.get("field")})')
                
            else:
                print('ERROR: FIN001 not found after update')
                
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    update_fin001_config()