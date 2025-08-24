# =============================================================================
# 3. reports/sql_executor.py - SQL and TEMPLATE Report Execution
# =============================================================================

from database import get_db_connection
from .core import load_sql_from_file
import re
import json

def format_report_data(data, columns, config):
    """Format report data including date formatting"""
    try:
        # Get date format from config, default to DD/MM/YYYY
        date_format = "DD/MM/YYYY"
        if config.get('params'):
            try:
                params_config = json.loads(config['params'])
                ui_config = params_config.get('ui_config', {})
                date_format = ui_config.get('date_format', 'DD/MM/YYYY')
            except:
                pass
        
        # Python date format mapping
        python_date_format = date_format.replace('DD', '%d').replace('MM', '%m').replace('YYYY', '%Y')
        
        print(f"TIME Using date format: {date_format} (Python: {python_date_format})")
        
        # Format the data
        formatted_data = []
        for row in data:
            formatted_row = []
            for i, value in enumerate(row):
                if value is not None and i < len(columns):
                    # Check if this looks like a date field - either by content or column name
                    column_name = columns[i].lower() if i < len(columns) else ""
                    is_date_column = any(date_word in column_name for date_word in ['date', '_dt', '_date', 'created', 'updated', 'modified', 'time'])
                    
                    # More comprehensive date detection patterns
                    date_patterns = [
                        r'\w{3}, \d{1,2} \w{3} \d{4}.*',  # Wed, 24 Jan 2024 (with optional time)
                        r'\d{1,2} \w{3} \d{4}.*',         # 24 Jan 2024 (with optional time)
                        r'\d{4}-\d{1,2}-\d{1,2}.*',       # 2024-01-24 (with optional time)
                        r'\d{1,2}/\d{1,2}/\d{4}.*'        # 24/01/2024 (with optional time)
                    ]
                    
                    looks_like_date = False
                    if isinstance(value, str) and len(value) >= 8:
                        import re
                        looks_like_date = any(re.search(pattern, value) for pattern in date_patterns)
                    
                    if isinstance(value, str) and (looks_like_date or (is_date_column and len(value) >= 8)):
                        try:
                            # Parse the date string and reformat
                            from datetime import datetime
                            # Handle different date formats that Oracle might return
                            date_formats = [
                                '%a, %d %b %Y %H:%M:%S',     # Wed, 24 Jan 2024 00:00:00
                                '%a, %d %b %Y %H:%M',        # Wed, 24 Jan 2024 00:00
                                '%a, %d %b %Y',              # Wed, 24 Jan 2024
                                '%d %b %Y %H:%M:%S',         # 24 Jan 2024 00:00:00
                                '%d %b %Y %H:%M',            # 24 Jan 2024 00:00
                                '%d %b %Y',                  # 24 Jan 2024
                                '%Y-%m-%d %H:%M:%S',         # 2024-01-24 00:00:00
                                '%Y-%m-%d %H:%M',            # 2024-01-24 00:00
                                '%Y-%m-%d',                  # 2024-01-24
                                '%d/%m/%Y %H:%M:%S',         # 24/01/2024 00:00:00
                                '%d/%m/%Y %H:%M',            # 24/01/2024 00:00
                                '%d/%m/%Y',                  # 24/01/2024
                                '%m/%d/%Y %H:%M:%S',         # 01/24/2024 00:00:00 (US format)
                                '%m/%d/%Y %H:%M',            # 01/24/2024 00:00 (US format)
                                '%m/%d/%Y'                   # 01/24/2024 (US format)
                            ]
                            
                            for fmt in date_formats:
                                try:
                                    # Clean the value first
                                    clean_value = value.replace(' GMT', '').replace(' UTC', '').strip()
                                    # Remove seconds if they appear as :XX at the end
                                    if clean_value.endswith(':00') or clean_value.endswith(':0'):
                                        clean_value = clean_value.rsplit(':', 1)[0]
                                    
                                    parsed_date = datetime.strptime(clean_value, fmt)
                                    formatted_value = parsed_date.strftime(python_date_format)
                                    if value != formatted_value:  # Only log when actually changed
                                        print(f"TIME Formatted date: {value} -> {formatted_value}")
                                    formatted_row.append(formatted_value)
                                    break
                                except ValueError:
                                    continue
                            else:
                                # If no format worked, keep original
                                formatted_row.append(value)
                        except:
                            formatted_row.append(value)
                    elif hasattr(value, 'strftime'):
                        # It's already a Python date/datetime object
                        try:
                            formatted_value = value.strftime(python_date_format)
                            print(f"TIME Formatted datetime object: {value} -> {formatted_value}")
                            formatted_row.append(formatted_value)
                        except:
                            formatted_row.append(str(value))
                    else:
                        # Not a date, keep as is
                        formatted_row.append(value)
                else:
                    formatted_row.append(value)
            
            formatted_data.append(formatted_row)
        
        return formatted_data
        
    except Exception as e:
        print(f"ERROR Error formatting data: {e}")
        # Return original data if formatting fails
        return data
    
def execute_sql_report(report_id, config, params):
    """Execute SQL report with column filtering and date formatting support"""
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
            
            # Get all columns and data
            all_columns = [desc[0] for desc in cursor.description]
            all_rows = cursor.fetchall()
            
            print(f"CHART/INFO Query returned {len(all_rows)} rows with {len(all_columns)} columns")
            print(f"INFO All columns: {all_columns}")
            
            # **Apply column filtering based on RPT_PARAMS**
            display_columns, column_headers = get_display_columns(config, all_columns)
            
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
                print(f"STEP Column filtering applied:")
                print(f"   CHART/INFO Total columns: {len(all_columns)}")
                print(f"   VIEW Display columns: {len(display_columns)} - {display_columns}")
                print(f"   HIDDEN Hidden columns: {len(hidden_columns)} - {hidden_columns}")
                
                # **NEW: Apply date formatting to filtered data**
                formatted_data = format_report_data(filtered_rows, display_columns, config)
                
                result = {
                    'count': len(formatted_data),
                    'columns': display_columns,
                    'column_headers': column_headers,
                    'data': formatted_data,
                    'all_columns': all_columns,  # Keep for debugging
                    'hidden_columns': hidden_columns,
                    'query': str(sql_query)[:200] + "..." if len(str(sql_query)) > 200 else str(sql_query),
                    'parameters': params,
                    'report_id': report_id,
                    'is_modular': config.get('is_modular', False),
                    'report_type': config.get('type', 'SQL')
                }
            else:
                # No filtering needed - display all columns with date formatting
                print(f"INFO No column filtering configured, displaying all columns")
                formatted_data = format_report_data(all_rows, all_columns, config)
                
                result = {
                    'count': len(formatted_data),
                    'columns': all_columns,
                    'column_headers': {col: col for col in all_columns},
                    'data': formatted_data,
                    'query': str(sql_query)[:200] + "..." if len(str(sql_query)) > 200 else str(sql_query),
                    'parameters': params,
                    'report_id': report_id,
                    'is_modular': config.get('is_modular', False),
                    'report_type': config.get('type', 'SQL')
                }
            
            print(f"SUCCESS SQL query executed successfully. Final result: {len(result['data'])} rows, {len(result['columns'])} columns")
            return result
            
    except Exception as e:
        print(f"ERROR Error executing SQL report: {e}")
        print(f"INFO Report ID: {report_id}")
        print(f"INFO Config: {config}")
        print(f"INFO Parameters: {params}")
        raise

def get_display_columns(config, all_columns):
    """Extract display column configuration from RPT_PARAMS"""
    try:
        # Check if we have RPT_PARAMS with column configuration
        if config.get('params'):
            try:
                # Parse the JSON from RPT_PARAMS
                params_config = json.loads(config['params'])
                
                # Get display columns and hidden columns configuration
                display_columns = params_config.get('display_columns', [])
                hidden_columns = params_config.get('hidden_columns', [])
                column_headers = params_config.get('column_headers', {})
                
                print(f"CHART/INFO RPT_PARAMS configuration found:")
                print(f"   INFO Display columns specified: {display_columns}")
                print(f"   HIDDEN Hidden columns specified: {hidden_columns}")
                
                # **NEW LOGIC: Handle both display_columns and hidden_columns**
                if display_columns:
                    # If display_columns is specified, use only those columns
                    valid_display_columns = [col for col in display_columns if col in all_columns]
                    print(f"SUCCESS Using display_columns list: {valid_display_columns}")
                    
                elif hidden_columns:
                    # If only hidden_columns is specified, show all columns EXCEPT hidden ones
                    valid_display_columns = [col for col in all_columns if col not in hidden_columns]
                    print(f"SUCCESS Using hidden_columns exclusion: hiding {hidden_columns}")
                    print(f"SUCCESS Resulting display columns: {valid_display_columns}")
                    
                else:
                    # Neither specified, show all columns
                    valid_display_columns = all_columns
                    print(f"INFO No display/hidden columns specified, showing all columns")
                
                if valid_display_columns:
                    # Create headers for valid columns
                    headers = {}
                    for col in valid_display_columns:
                        # Use configured header, or create user-friendly default
                        if col in column_headers:
                            headers[col] = column_headers[col]
                        else:
                            # Create user-friendly header from column name
                            headers[col] = col.replace('_', ' ').title()
                    
                    return valid_display_columns, headers
                else:
                    print(f"WARNING No valid display columns found after filtering")
                    
            except json.JSONDecodeError as e:
                print(f"WARNING RPT_PARAMS is not valid JSON: {e}")
            except Exception as e:
                print(f"WARNING Error parsing RPT_PARAMS: {e}")
        else:
            print(f"INFO No RPT_PARAMS found for column configuration")
        
        # Fallback: return all columns with default headers
        print(f"STEP Falling back to all columns")
        return all_columns, {col: col for col in all_columns}
        
    except Exception as e:
        print(f"ERROR Error in get_display_columns: {e}")
        # Fallback: return all columns
        return all_columns, {col: col for col in all_columns}