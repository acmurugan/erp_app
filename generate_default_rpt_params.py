#!/usr/bin/env python3
"""
Auto-generate RPT_PARAMS JSON with all column names as defaults
Run a report once to get column names, then generate complete JSON config
"""

from database import get_db_connection
import json

def generate_default_column_config(report_id):
    """Generate default column configuration by running the report and getting column names"""
    
    try:
        print(f"Generating default RPT_PARAMS for {report_id}...")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get report configuration
            cursor.execute("""
                SELECT RPT_NAME, RPT_TYPE, RPT_SOURCE, RPT_PARAMS 
                FROM RPT_REPORT_MASTER 
                WHERE RPT_ID = :report_id
            """, {'report_id': report_id})
            
            result = cursor.fetchone()
            if not result:
                print(f"ERROR: Report {report_id} not found")
                return None
                
            rpt_name, rpt_type, rpt_source, existing_params = result
            
            # Parse existing parameters to keep them
            existing_config = {}
            if existing_params:
                try:
                    if hasattr(existing_params, 'read'):
                        existing_content = existing_params.read()
                    else:
                        existing_content = str(existing_params)
                    existing_config = json.loads(existing_content)
                except:
                    print("WARNING: Could not parse existing RPT_PARAMS, starting fresh")
            
            # If it's a CLASS report, try to get column names by running it
            if rpt_type == 'CLASS':
                try:
                    # Import and run the report class to get column names
                    import importlib.util
                    import os
                    
                    class_file = f"reports/classes/{rpt_source.lower().replace('report', '')}.py"
                    if os.path.exists(class_file):
                        spec = importlib.util.spec_from_file_location(rpt_source, class_file)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Get the report class
                        report_class = getattr(module, rpt_source, None)
                        if report_class:
                            # Run with default params to get columns
                            report_instance = report_class()
                            
                            # Create minimal test params
                            test_params = {
                                'M_FM_YYYYMM': '202501',
                                'M_TO_YYYYMM': '202512', 
                                'M_FM_DIVN': '0',
                                'M_TO_DIVN': 'ZZZZZZ',
                                'M_FM_DEPT': '0', 
                                'M_TO_DEPT': 'ZZZZZZ',
                                'M_FM_MAIN_AC': '0',
                                'M_TO_MAIN_AC': 'ZZZZZZ',
                                'M_FM_SUB_AC': '0',
                                'M_TO_SUB_AC': 'ZZZZZZ',
                                'comp_code': 'TTM',
                                'user_id': 'SYSTEM'
                            }
                            
                            # Try to get column structure
                            result = report_instance.execute(test_params)
                            if result and 'columns' in result:
                                columns = result['columns']
                                print(f"Found {len(columns)} columns: {columns}")
                                
                                # Generate complete JSON config
                                default_config = {
                                    "parameters": existing_config.get('parameters', []),
                                    "display_columns": [],  # Empty = show all
                                    "column_headers": {col: col.replace('_', ' ').title() for col in columns},
                                    "hidden_columns": [],   # Empty = hide none
                                    "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
                                    "global_variables": existing_config.get('global_variables', {
                                        "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
                                        "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
                                    })
                                }
                                
                                return default_config
                                
                except Exception as e:
                    print(f"Could not auto-detect columns for {report_id}: {e}")
            
            # Fallback: create basic structure
            basic_config = {
                "parameters": existing_config.get('parameters', []),
                "display_columns": [],
                "column_headers": {},
                "hidden_columns": [],
                "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
                "global_variables": existing_config.get('global_variables', {})
            }
            
            return basic_config
            
    except Exception as e:
        print(f"ERROR generating default config: {e}")
        return None

def update_rpt_params_with_defaults(report_id, config):
    """Update RPT_PARAMS with the generated default configuration"""
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            json_config = json.dumps(config, indent=2)
            
            cursor.execute("""
                UPDATE RPT_REPORT_MASTER 
                SET RPT_PARAMS = :config 
                WHERE RPT_ID = :report_id
            """, {'config': json_config, 'report_id': report_id})
            
            conn.commit()
            print(f"SUCCESS: Updated {report_id} with default RPT_PARAMS")
            print("Generated configuration:")
            print(json_config)
            
            return True
            
    except Exception as e:
        print(f"ERROR updating RPT_PARAMS: {e}")
        return False

# Example usage
if __name__ == '__main__':
    report_id = input("Enter Report ID (e.g., FIN001, TTL715): ").strip().upper()
    
    config = generate_default_column_config(report_id)
    if config:
        print("\nGenerated default configuration:")
        print(json.dumps(config, indent=2))
        
        confirm = input(f"\nUpdate {report_id} with this configuration? (y/n): ").strip().lower()
        if confirm == 'y':
            update_rpt_params_with_defaults(report_id, config)
        else:
            print("Configuration not applied.")
    else:
        print("Could not generate configuration.")