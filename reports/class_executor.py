# =============================================================================
# 4. reports/class_executor.py - CLASS Report Execution
# =============================================================================

from pathlib import Path
import importlib.util
import sys
import inspect
import traceback
import json


def get_display_columns(rpt_params_json, all_columns):
    """Extract display column configuration from RPT_PARAMS"""
    try:
        # Check if we have RPT_PARAMS with column configuration
        if rpt_params_json:
            try:
                # Parse the JSON from RPT_PARAMS
                params_config = json.loads(rpt_params_json)
                
                # Get display columns and hidden columns configuration
                display_columns = params_config.get('display_columns', [])
                hidden_columns = params_config.get('hidden_columns', [])
                column_headers = params_config.get('column_headers', {})
                
                print("RPT_PARAMS configuration found:")
                print(f"   Display columns specified: {display_columns}")
                print(f"   Hidden columns specified: {hidden_columns}")
                
                # Handle both display_columns and hidden_columns
                if display_columns:
                    # If display_columns is specified, use only those columns
                    valid_display_columns = [col for col in display_columns if col in all_columns]
                    print(f"Using display_columns list: {valid_display_columns}")
                    
                elif hidden_columns:
                    # If only hidden_columns is specified, show all columns EXCEPT hidden ones
                    valid_display_columns = [col for col in all_columns if col not in hidden_columns]
                    print(f"Using hidden_columns exclusion: hiding {hidden_columns}")
                    print(f"Resulting display columns: {valid_display_columns}")
                    
                else:
                    # Neither specified, show all columns
                    valid_display_columns = all_columns
                    print("No display/hidden columns specified, showing all columns")
                
                if valid_display_columns:
                    # Create headers for valid columns
                    headers = {}
                    for col in valid_display_columns:
                        # Use configured header, or create user-friendly default
                        if col in column_headers:
                            headers[col] = column_headers[col]
                            print(f"DEBUG Using configured header: {col} -> {column_headers[col]}")
                        else:
                            # Create user-friendly header from column name
                            friendly_name = col.replace('_', ' ').title()
                            headers[col] = friendly_name
                            print(f"DEBUG Auto-generated header: {col} -> {friendly_name}")
                    
                    print(f"DEBUG Final headers dict: {headers}")
                    return valid_display_columns, headers
                else:
                    print("No valid display columns found after filtering")
                    
            except json.JSONDecodeError as e:
                print(f"RPT_PARAMS is not valid JSON: {e}")
            except Exception as e:
                print(f"Error parsing RPT_PARAMS: {e}")
        else:
            print("No RPT_PARAMS found for column configuration")
        
        # Fallback: return all columns with default headers
        print("Falling back to all columns")
        return all_columns, {col: col for col in all_columns}
        
    except Exception as e:
        print(f"Error in get_display_columns: {e}")
        # Fallback: return all columns
        return all_columns, {col: col for col in all_columns}


def execute_class_report(report_id, config, params):
    """Execute class-based complex reports with dynamic loading"""
    try:
        print(f"BUILD Executing class-based report: {config['sql_query']}")
        
        # Load Python class file
        reports_base_path = Path("reports")
        class_file = reports_base_path / "classes" / f"{config['sql_query']}.py"
        
        if not class_file.exists():
            return {
                'count': 1,
                'columns': ['Status', 'Message', 'Details'],
                'data': [['ERROR', f'Class file not found', str(class_file)]],
                'query': f"Class file loading failed: {config['sql_query']}.py",
                'parameters': params,
                'report_id': report_id,
                'is_modular': True,
                'report_type': 'CLASS'
            }
        
        # Dynamic class loading
        try:
            module_name = f"report_class_{config['sql_query']}"
            spec = importlib.util.spec_from_file_location(module_name, class_file)
            module = importlib.util.module_from_spec(spec)
            
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Find the report class
            report_class = find_report_class(module, config['sql_query'])
            
            if not report_class:
                available_classes = [name for name, obj in inspect.getmembers(module, inspect.isclass)]
                return {
                    'count': 1,
                    'columns': ['Status', 'Message', 'Available_Classes'],
                    'data': [['ERROR', 'No suitable report class found', str(available_classes)]],
                    'query': f"Class discovery failed in {config['sql_query']}.py",
                    'parameters': params,
                    'report_id': report_id,
                    'is_modular': True,
                    'report_type': 'CLASS'
                }
            
            # Execute the report class
            result = execute_class_method(report_class, params, config)
            
            if result:
                # Apply column filtering based on RPT_PARAMS
                all_columns = result.get('columns', [])
                all_rows = result.get('data', [])
                
                if all_columns and config.get('params'):
                    print(f"CLASS result before filtering: {len(all_columns)} columns, {len(all_rows)} rows")
                    print(f"DEBUG CLASS RPT_PARAMS content: {config.get('params', 'NONE')[:200]}...")
                    
                    display_columns, column_headers = get_display_columns(config['params'], all_columns)
                    print(f"DEBUG CLASS column headers returned: {column_headers}")
                    print(f"DEBUG CLASS display columns: {display_columns[:5]}...")
                    
                    # Filter data to show only display columns
                    if display_columns != all_columns:
                        # Get indices of columns to display
                        display_indices = [all_columns.index(col) for col in display_columns if col in all_columns]
                        
                        # Filter rows to include only display columns
                        filtered_rows = []
                        for row in all_rows:
                            filtered_row = [row[i] for i in display_indices]
                            filtered_rows.append(filtered_row)
                        
                        hidden_columns = [col for col in all_columns if col not in display_columns]
                        print("CLASS column filtering applied:")
                        print(f"   Total columns: {len(all_columns)}")
                        print(f"   Display columns: {len(display_columns)} - {display_columns}")
                        print(f"   Hidden columns: {len(hidden_columns)} - {hidden_columns}")
                        
                        result.update({
                            'columns': display_columns,
                            'column_headers': column_headers,
                            'data': filtered_rows,
                            'count': len(filtered_rows),
                            'all_columns': all_columns,
                            'hidden_columns': hidden_columns
                        })
                        print(f"DEBUG CLASS Final result column_headers: {column_headers}")
                        print(f"DEBUG CLASS Final result columns: {display_columns[:5]}...")
                    else:
                        # No filtering needed - display all columns
                        print("No CLASS column filtering configured, displaying all columns")
                        
                        # Still check if we have column headers configured
                        display_columns, column_headers = get_display_columns(config['params'], all_columns)
                        print(f"DEBUG CLASS (no filtering) column headers: {column_headers}")
                        print(f"DEBUG CLASS (no filtering) display columns: {display_columns[:5]}...")
                        
                        result.update({
                            'column_headers': column_headers
                        })
                
                result.update({
                    'report_id': report_id,
                    'is_modular': True,
                    'report_type': 'CLASS',
                    'parameters': params
                })
                return result
            else:
                return {
                    'count': 1,
                    'columns': ['Status', 'Message'],
                    'data': [['ERROR', 'No suitable execution method found']],
                    'query': f"Method execution failed in {report_class.__name__}",
                    'parameters': params,
                    'report_id': report_id,
                    'is_modular': True,
                    'report_type': 'CLASS'
                }
            
        except Exception as class_error:
            print(f"ERROR Error loading/executing class: {class_error}")
            error_trace = traceback.format_exc()
            return {
                'count': 1,
                'columns': ['Status', 'Error', 'Traceback'],
                'data': [['ERROR', str(class_error), error_trace[:500]]],
                'query': f"Class execution error: {config['sql_query']}.py",
                'parameters': params,
                'report_id': report_id,
                'is_modular': True,
                'report_type': 'CLASS'
            }
        
    except Exception as e:
        print(f"ERROR Error executing class report: {e}")
        return {
            'count': 1,
            'columns': ['Status', 'Error'],
            'data': [['FATAL_ERROR', str(e)]],
            'query': f"Fatal error in class report: {config['sql_query']}",
            'parameters': params,
            'report_id': report_id,
            'is_modular': True,
            'report_type': 'CLASS'
        }

def find_report_class(module, report_id):
    """Find the appropriate report class in the module"""
    expected_class_names = [
        f"{report_id}Report",  # TTL201Report
        f"{report_id}",        # TTL201
        "ReportProcessor",     # Generic name
        "Report"               # Simple name
    ]
    
    for class_name in expected_class_names:
        if hasattr(module, class_name):
            return getattr(module, class_name)
    
    # Try to find any class that has 'execute' or 'generate' method
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if hasattr(obj, 'execute') or hasattr(obj, 'generate') or hasattr(obj, 'run'):
            return obj
    
    return None

def execute_class_method(report_class, params, config):
    """Execute the appropriate method on the report class"""
    try:
        report_instance = report_class()
        execution_methods = ['execute', 'generate', 'run', 'process']
        
        for method_name in execution_methods:
            if hasattr(report_instance, method_name):
                method = getattr(report_instance, method_name)
                
                # Try different parameter combinations
                try:
                    return method(params, config)  # Try with params and config
                except TypeError:
                    try:
                        return method(params)  # Try with just params
                    except TypeError:
                        try:
                            return method()  # Try with no parameters
                        except:
                            continue
        
        return None
        
    except Exception as e:
        print(f"ERROR Error executing class method: {e}")
        return None
