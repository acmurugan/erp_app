# =============================================================================
# 5. reports/procedure_executor.py - PROCEDURE Report Execution
# =============================================================================

import oracledb
from database import get_db_connection
import traceback

def get_display_columns(rpt_params_json, all_columns):
    """
    Filter columns based on display_columns configuration.
    Converts display columns list and column headers into a consistent format.
    
    Args:
        rpt_params_json (dict): RPT_PARAMS JSON containing display/hidden columns and headers
        all_columns (list): All available column names from query result
    
    Returns:
        tuple: (filtered_columns, column_headers_dict)
               filtered_columns: list of columns to display
               column_headers_dict: mapping of column_name -> display_header
    """
    try:
        print(f"INFO get_display_columns() called")
        print(f"INFO RPT_PARAMS type: {type(rpt_params_json)}")
        print(f"INFO Available columns ({len(all_columns)}): {all_columns}")
        
        if not rpt_params_json or not isinstance(rpt_params_json, dict):
            print(f"WARNING No valid RPT_PARAMS found, returning all columns")
            return all_columns, {}
        
        display_columns = rpt_params_json.get('display_columns', [])
        hidden_columns = rpt_params_json.get('hidden_columns', [])
        column_headers = rpt_params_json.get('column_headers', {})
        
        print(f"CONFIG Display columns: {display_columns}")
        print(f"CONFIG Hidden columns: {hidden_columns}")
        print(f"CONFIG Column headers: {len(column_headers)} mappings")
        
        # If display_columns is empty, show all columns except hidden ones
        if not display_columns:
            print(f"LOGIC No display_columns specified, using all columns minus hidden")
            filtered_columns = [col for col in all_columns if col not in hidden_columns]
            print(f"RESULT After hiding {len(hidden_columns)} columns: {len(filtered_columns)} remaining")
        else:
            print(f"LOGIC Using display_columns filter")
            # Filter to only show columns in display_columns (and that exist in results)
            filtered_columns = [col for col in all_columns if col in display_columns]
            print(f"RESULT After display filter: {len(filtered_columns)} columns selected")
        
        print(f"SUCCESS Final filtered columns: {filtered_columns}")
        return filtered_columns, column_headers
        
    except Exception as e:
        print(f"ERROR Error in get_display_columns: {e}")
        print(f"INFO Falling back to all columns")
        return all_columns, {}

def execute_procedure_report(report_id, config, params):
    """Execute procedure-based reports with Oracle stored procedures"""
    try:
        print(f"TOOL Executing procedure-based report: {config['sql_query']}")
        
        procedure_name = config['sql_query']
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if procedure exists
            if not check_procedure_exists(cursor, procedure_name):
                return {
                    'count': 1,
                    'columns': ['Status', 'Message', 'Procedure'],
                    'data': [['ERROR', 'Stored procedure not found', procedure_name.upper()]],
                    'query': f"Procedure lookup: {procedure_name}",
                    'parameters': params,
                    'report_id': report_id,
                    'is_modular': True,
                    'report_type': 'PROCEDURE'
                }
            
            # Try different execution methods
            for method in ['function_cursor', 'procedure_out_cursor', 'simple_procedure', 'plsql_block']:
                try:
                    result = execute_procedure_method(cursor, procedure_name, params, method, report_id, config)
                    if result:
                        return result
                except Exception as e:
                    print(f"WARNING Method {method} failed: {e}")
                    continue
            
            # All methods failed
            return {
                'count': 1,
                'columns': ['Status', 'Error', 'Procedure'],
                'data': [['ERROR', 'All execution methods failed', procedure_name]],
                'query': f"Multiple execution attempts failed: {procedure_name}",
                'parameters': params,
                'report_id': report_id,
                'is_modular': True,
                'report_type': 'PROCEDURE'
            }
        
    except Exception as e:
        print(f"ERROR Error executing procedure report: {e}")
        error_trace = traceback.format_exc()
        return {
            'count': 1,
            'columns': ['Status', 'Error', 'Traceback'],
            'data': [['ERROR', str(e), error_trace[:500]]],
            'query': f"Procedure execution error: {config['sql_query']}",
            'parameters': params,
            'report_id': report_id,
            'is_modular': True,
            'report_type': 'PROCEDURE'
        }

def check_procedure_exists(cursor, procedure_name):
    """Check if procedure exists in database"""
    cursor.execute("""
        SELECT OBJECT_NAME, OBJECT_TYPE, STATUS 
        FROM USER_OBJECTS 
        WHERE OBJECT_NAME = UPPER(:proc_name) 
        AND OBJECT_TYPE IN ('PROCEDURE', 'FUNCTION', 'PACKAGE')
    """, {'proc_name': procedure_name})
    
    return cursor.fetchone() is not None

def execute_procedure_method(cursor, procedure_name, params, method, report_id, config):
    """Execute procedure using specific method"""
    if method == 'function_cursor':
        return try_function_cursor(cursor, procedure_name, params, report_id, config)
    elif method == 'procedure_out_cursor':
        return try_procedure_out_cursor(cursor, procedure_name, params, report_id, config)
    elif method == 'simple_procedure':
        return try_simple_procedure(cursor, procedure_name, params, report_id, config)
    elif method == 'plsql_block':
        return try_plsql_block(cursor, procedure_name, params, report_id, config)
    
    return None

def try_function_cursor(cursor, procedure_name, params, report_id, config):
    """Try executing as function returning cursor"""
    param_values = list(params.values())
    result_cursor = cursor.callfunc(procedure_name, oracledb.CURSOR, param_values)
    
    if result_cursor:
        all_columns = [desc[0] for desc in result_cursor.description]
        all_data = result_cursor.fetchall()
        result_cursor.close()
        
        # Apply column filtering
        try:
            filtered_columns, column_headers = get_display_columns(config.get('params', {}), all_columns)
            
            # Filter data to match filtered columns
            column_indices = [all_columns.index(col) for col in filtered_columns if col in all_columns]
            filtered_data = [[row[i] for i in column_indices] for row in all_data]
            
            result = {
                'columns': filtered_columns,
                'data': filtered_data,
                'count': len(filtered_data),
                'query': f"Function call: {procedure_name}",
                'parameters': params,
                'report_id': report_id,
                'is_modular': True,
                'report_type': 'PROCEDURE'
            }
            
            # Add column headers if available
            if column_headers:
                result['column_headers'] = column_headers
            
            print(f"SUCCESS Applied column filtering: {len(all_columns)} -> {len(filtered_columns)} columns")
            return result
            
        except Exception as e:
            print(f"ERROR Column filtering failed: {e}, using original columns")
            return {
                'columns': all_columns,
                'data': all_data,
                'count': len(all_data),
                'query': f"Function call: {procedure_name}",
                'parameters': params,
                'report_id': report_id,
                'is_modular': True,
                'report_type': 'PROCEDURE'
            }
    
    return None

def try_procedure_out_cursor(cursor, procedure_name, params, report_id, config):
    """Try executing as procedure with OUT cursor parameter"""
    out_cursor = cursor.var(oracledb.CURSOR)
    param_values = list(params.values()) + [out_cursor]
    
    cursor.callproc(procedure_name, param_values)
    
    result_cursor = out_cursor.getvalue()
    if result_cursor:
        all_columns = [desc[0] for desc in result_cursor.description]
        all_data = result_cursor.fetchall()
        result_cursor.close()
        
        # Apply column filtering
        try:
            filtered_columns, column_headers = get_display_columns(config.get('params', {}), all_columns)
            
            # Filter data to match filtered columns
            column_indices = [all_columns.index(col) for col in filtered_columns if col in all_columns]
            filtered_data = [[row[i] for i in column_indices] for row in all_data]
            
            result = {
                'columns': filtered_columns,
                'data': filtered_data,
                'count': len(filtered_data),
                'query': f"Procedure with OUT cursor: {procedure_name}",
                'parameters': params,
                'report_id': report_id,
                'is_modular': True,
                'report_type': 'PROCEDURE'
            }
            
            # Add column headers if available
            if column_headers:
                result['column_headers'] = column_headers
            
            print(f"SUCCESS Applied column filtering: {len(all_columns)} -> {len(filtered_columns)} columns")
            return result
            
        except Exception as e:
            print(f"ERROR Column filtering failed: {e}, using original columns")
            return {
                'columns': all_columns,
                'data': all_data,
                'count': len(all_data),
                'query': f"Procedure with OUT cursor: {procedure_name}",
                'parameters': params,
                'report_id': report_id,
                'is_modular': True,
                'report_type': 'PROCEDURE'
            }
    
    return None

def try_simple_procedure(cursor, procedure_name, params, report_id, config):
    """Try executing as simple procedure"""
    param_values = list(params.values())
    cursor.callproc(procedure_name, param_values)
    
    # Try to find temp tables
    temp_table_names = [
        f"TEMP_{report_id}_{params.get('user_id', 'USER')}",
        f"RPT_{report_id}_TEMP",
        f"{report_id}_RESULT"
    ]
    
    for temp_table_name in temp_table_names:
        try:
            cursor.execute(f"SELECT * FROM {temp_table_name}")
            all_columns = [desc[0] for desc in cursor.description]
            all_data = cursor.fetchall()
            
            # Cleanup
            try:
                cursor.execute(f"DROP TABLE {temp_table_name}")
            except:
                pass
            
            # Apply column filtering
            try:
                filtered_columns, column_headers = get_display_columns(config.get('params', {}), all_columns)
                
                # Filter data to match filtered columns
                column_indices = [all_columns.index(col) for col in filtered_columns if col in all_columns]
                filtered_data = [[row[i] for i in column_indices] for row in all_data]
                
                result = {
                    'columns': filtered_columns,
                    'data': filtered_data,
                    'count': len(filtered_data),
                    'query': f"Procedure with temp table: {procedure_name}",
                    'parameters': params,
                    'report_id': report_id,
                    'is_modular': True,
                    'report_type': 'PROCEDURE'
                }
                
                # Add column headers if available
                if column_headers:
                    result['column_headers'] = column_headers
                
                print(f"SUCCESS Applied column filtering: {len(all_columns)} -> {len(filtered_columns)} columns")
                return result
                
            except Exception as e:
                print(f"ERROR Column filtering failed: {e}, using original columns")
                return {
                    'columns': all_columns,
                    'data': all_data,
                    'count': len(all_data),
                    'query': f"Procedure with temp table: {procedure_name}",
                    'parameters': params,
                    'report_id': report_id,
                    'is_modular': True,
                    'report_type': 'PROCEDURE'
                }
        except:
            continue
    
    # No temp table found, return success message
    return {
        'columns': ['Status', 'Message'],
        'data': [['SUCCESS', f'Procedure {procedure_name} executed successfully']],
        'count': 1,
        'query': f"Simple procedure call: {procedure_name}",
        'parameters': params,
        'report_id': report_id,
        'is_modular': True,
        'report_type': 'PROCEDURE'
    }

def try_plsql_block(cursor, procedure_name, params, report_id, config):
    """Try executing with PL/SQL block"""
    # Get procedure parameters
    cursor.execute("""
        SELECT ARGUMENT_NAME, DATA_TYPE, IN_OUT, POSITION
        FROM ALL_ARGUMENTS 
        WHERE OBJECT_NAME = UPPER(:proc_name)
        AND OWNER = USER
        ORDER BY POSITION
    """, {'proc_name': procedure_name})
    
    proc_params = cursor.fetchall()
    
    if proc_params:
        param_list = []
        bind_vars = {}
        
        for param_name, data_type, in_out, position in proc_params:
            if param_name:
                param_key = param_name.lower()
                
                if param_key in params:
                    bind_vars[param_key] = params[param_key]
                else:
                    # Default values
                    if data_type == 'VARCHAR2':
                        bind_vars[param_key] = ''
                    elif data_type in ['NUMBER', 'INTEGER']:
                        bind_vars[param_key] = 0
                    else:
                        bind_vars[param_key] = None
                
                param_list.append(f":{param_key}")
        
        proc_call = f"BEGIN {procedure_name}({', '.join(param_list)}); END;"
    else:
        proc_call = f"BEGIN {procedure_name}; END;"
        bind_vars = {}
    
    cursor.execute(proc_call, bind_vars)
    
    return {
        'count': 1,
        'columns': ['Status', 'Message', 'Procedure'],
        'data': [['SUCCESS', f'Procedure executed via PL/SQL', procedure_name]],
        'query': proc_call,
        'parameters': params,
        'report_id': report_id,
        'is_modular': True,
        'report_type': 'PROCEDURE'
    }
