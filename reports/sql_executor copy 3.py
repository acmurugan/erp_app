# =============================================================================
# 3. reports/sql_executor.py - SQL and TEMPLATE Report Execution
# =============================================================================

from database import get_db_connection
from .core import load_sql_from_file  # This should work based on your core.py
import re

def execute_sql_report(report_id, config, params):
    """Execute SQL report (both traditional and modular)"""
    try:
        # Get SQL query (either from database or file)
        if config.get('is_modular', False):
            sql_query = load_sql_from_file(config['sql_query'], config['type'])
        else:
            sql_query = config['sql_query']
        
        print(f"INFO SQL Query loaded, length: {len(sql_query)} characters")
        
        # Execute query
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Filter out display parameters that aren't SQL bind variables
            sql_only_params = {k: v for k, v in params.items() 
                               if k not in ['report_id', 'report_type', 'timestamp', 'period_name', 'table_prefix', 'menu_id', 'reportType', 'outputFormat']}

            print(f"STEP Executing SQL with {len(sql_only_params)} parameters (filtered from {len(params)})")
            print(f"INFO Original form parameters: {list(sql_only_params.keys())}")

            # **GLOBAL FIX: Handle case-insensitive parameter matching**
            # Find all parameters required by the SQL query
            sql_params_in_query = re.findall(r':(\w+)', sql_query)
            unique_sql_params = list(set(sql_params_in_query))
            
            print(f"INFO Parameters expected by SQL query: {unique_sql_params}")
            
            # Create a case-insensitive parameter dictionary
            final_params = {}
            
            for sql_param in unique_sql_params:
                # Try to find matching parameter (case-insensitive)
                param_found = False
                for form_param, value in sql_only_params.items():
                    if sql_param.upper() == form_param.upper():
                        final_params[sql_param] = value  # Use SQL's case for the key
                        param_found = True
                        print(f"SUCCESS Mapped: {form_param} -> :{sql_param}")
                        break
                
                if not param_found:
                    print(f"ERROR WARNING: SQL parameter '{sql_param}' not found in form data")
                    print(f"INFO Available form parameters: {list(sql_only_params.keys())}")

            print(f"SUCCESS Final mapped parameters: {list(final_params.keys())}")
            print(f"CHART/INFO Parameter values being sent to Oracle:")
            for key, value in final_params.items():
                print(f"   :{key} = '{value}'")

            # Use the properly mapped parameters
            cursor.execute(sql_query, final_params)
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            result = {
                'count': len(rows),
                'columns': columns,
                'data': rows,
                'query': str(sql_query)[:200] + "..." if len(str(sql_query)) > 200 else str(sql_query),
                'parameters': params,  # Keep all parameters for report display
                'report_id': report_id,
                'is_modular': config.get('is_modular', False),
                'report_type': config.get('type', 'SQL')
            }
            
            print(f"SUCCESS SQL query executed successfully. Rows: {len(rows)}")
            return result
            
    except Exception as e:
        print(f"ERROR Error executing SQL report: {e}")
        print(f"INFO Report ID: {report_id}")
        print(f"INFO Config: {config}")
        print(f"INFO Parameters: {params}")
        raise