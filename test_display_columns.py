"""
Test script to add display_columns configuration to FIN001 report
"""
import json
from database import get_db_connection

def test_display_columns():
    """Update FIN001 to test display column filtering"""
    try:
        print("Testing display column functionality...")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # First, get current RPT_PARAMS
            cursor.execute("""
                SELECT RPT_PARAMS FROM RPT_REPORT_MASTER 
                WHERE RPT_ID = 'FIN001'
            """)
            
            result = cursor.fetchone()
            if not result:
                print("FIN001 not found!")
                return False
                
            current_params = result[0]
            if hasattr(current_params, 'read'):
                current_params = current_params.read()
            
            if current_params:
                # Parse existing params
                params_config = json.loads(current_params)
                print(f"Current config found with {len(params_config.get('parameters', []))} parameters")
                
                # Add display columns configuration - show only key business columns
                params_config['display_columns'] = [
                    'ABAL_MAIN_ACNT_CODE',
                    'MAIN_ACNT_NAME', 
                    'SUB_ACNT_NAME',
                    'DIVN_NAME',
                    'OP_BAL',
                    'CLO_BAL'
                ]
                
                # Add column headers for better display
                params_config['column_headers'] = {
                    'ABAL_MAIN_ACNT_CODE': 'Account Code',
                    'MAIN_ACNT_NAME': 'Account Name',
                    'SUB_ACNT_NAME': 'Sub Account',  
                    'DIVN_NAME': 'Division',
                    'OP_BAL': 'Opening Balance',
                    'CLO_BAL': 'Closing Balance'
                }
                
                # Update the database
                new_params = json.dumps(params_config, indent=2)
                
                cursor.execute("""
                    UPDATE RPT_REPORT_MASTER 
                    SET RPT_PARAMS = :new_params
                    WHERE RPT_ID = 'FIN001'
                """, {'new_params': new_params})
                
                conn.commit()
                
                print("SUCCESS: Updated FIN001 with display column configuration:")
                print("   Display columns: 6 key business columns")
                print("   Column headers: User-friendly names")
                print("")
                print("Now test by running the FIN001 report at:")
                print("http://127.0.0.1:5000/reports/FIN001/T030101")
                print("")
                print("Expected result: Report should show only 6 columns instead of all 25")
                
                return True
            else:
                print("No RPT_PARAMS found for FIN001")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def reset_display_columns():
    """Reset FIN001 to show all columns"""
    try:
        print("Resetting FIN001 to show all columns...")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get current RPT_PARAMS
            cursor.execute("""
                SELECT RPT_PARAMS FROM RPT_REPORT_MASTER 
                WHERE RPT_ID = 'FIN001'
            """)
            
            result = cursor.fetchone()
            if not result:
                print("FIN001 not found!")
                return False
                
            current_params = result[0]
            if hasattr(current_params, 'read'):
                current_params = current_params.read()
            
            if current_params:
                # Parse existing params
                params_config = json.loads(current_params)
                
                # Reset display columns to empty (show all)
                params_config['display_columns'] = []
                params_config['hidden_columns'] = []
                
                # Update the database
                new_params = json.dumps(params_config, indent=2)
                
                cursor.execute("""
                    UPDATE RPT_REPORT_MASTER 
                    SET RPT_PARAMS = :new_params
                    WHERE RPT_ID = 'FIN001'
                """, {'new_params': new_params})
                
                conn.commit()
                
                print("SUCCESS: Reset FIN001 to show all columns")
                return True
            else:
                print("No RPT_PARAMS found for FIN001")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_display_columns()
    else:
        test_display_columns()