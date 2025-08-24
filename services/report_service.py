import json
import pandas as pd
from io import BytesIO
from datetime import datetime
from flask import session, Response, flash, redirect, url_for, render_template
from database import get_db_connection


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
                        else:
                            # Create user-friendly header from column name
                            headers[col] = col.replace('_', ' ').title()
                    
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


class DynamicReportService:
    
    def get_report_definition(self, report_id):
        """Get report definition from RPT_REPORT_MASTER table"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, 
                           RPT_PARAMS, RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_ACTIVE_FLAG
                    FROM RPT_REPORT_MASTER 
                    WHERE RPT_ID = :report_id 
                      AND NVL(RPT_ACTIVE_FLAG, 'Y') = 'Y'
                """
                
                cursor.execute(query, {'report_id': report_id})
                result = cursor.fetchone()
                
                if result:
                    return {
                        'rpt_id': result[0],
                        'rpt_name': result[1],
                        'rpt_desc': result[2],
                        'rpt_type': result[3],
                        'rpt_source': result[4].read() if result[4] else '',  # CLOB to string
                        'rpt_params': result[5].read() if result[5] else '{}',  # CLOB to string
                        'rpt_output_formats': result[6],
                        'rpt_category': result[7],
                        'rpt_active_flag': result[8]
                    }
                return None
                
        except Exception as e:
            print(f"Error getting report definition: {e}")
            return None
    
    def parse_report_parameters(self, params_json):
        """Parse report parameters from JSON"""
        try:
            if not params_json:
                return []
            
            # Parse JSON parameters
            params = json.loads(params_json)
            
            # Return list of parameter definitions
            return params.get('parameters', [])
            
        except Exception as e:
            print(f"Error parsing report parameters: {e}")
            return []
    
    def build_parameter_form_config(self, report_definition):
        """Build form configuration from report definition"""
        try:
            # Parse parameters
            parameters = self.parse_report_parameters(report_definition['rpt_params'])
            
            # Build form config
            form_config = {
                'title': report_definition['rpt_name'],
                'description': report_definition['rpt_desc'],
                'report_id': report_definition['rpt_id'],
                'output_formats': report_definition['rpt_output_formats'].split(',') if report_definition['rpt_output_formats'] else ['view'],
                'parameters': parameters
            }
            
            return form_config
            
        except Exception as e:
            print(f"Error building form config: {e}")
            return None
    
    def execute_dynamic_report(self, report_id, form_params):
        """Execute dynamic report based on stored query"""
        try:
            print(f"🔍 Executing dynamic report for ID: {report_id}")
            
            # Get report definition
            report_def = self.get_report_definition(report_id)
            if not report_def:
                print(f"❌ Report definition not found for ID: {report_id}")
                return {
                    'columns': ['Error'],
                    'rows': [['Report definition not found. Please check RPT_REPORT_MASTER table.']],
                    'count': 0
                }
            
            # Get the SQL query
            sql_query = report_def['rpt_source']
            if not sql_query:
                print(f"❌ No SQL query defined for report: {report_id}")
                return {
                    'columns': ['Error'],
                    'rows': [['No SQL query defined for this report']],
                    'count': 0
                }
            
            print(f"✅ Report found: {report_def['rpt_name']}")
            print(f"📄 SQL Query length: {len(sql_query)} characters")
            
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Build query parameters
                query_params = self.build_query_parameters(sql_query, form_params)
                
                print(f"🔧 Form params received: {form_params}")
                print(f"🔧 Query params built: {query_params}")
                print(f"📜 SQL Query preview (first 200 chars): {sql_query[:200]}...")
                
                try:
                    # Execute the query
                    cursor.execute(sql_query, query_params)
                    
                    # Get ALL column names and data from database
                    all_columns = [desc[0] for desc in cursor.description]
                    all_rows = cursor.fetchall()
                    
                    print(f"✅ Query executed successfully")
                    print(f"📊 Total columns: {len(all_columns)}")
                    print(f"📊 Rows: {len(all_rows)}")
                    
                    # Apply column filtering based on RPT_PARAMS
                    display_columns, column_headers = get_display_columns(report_def['rpt_params'], all_columns)
                    
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
                        print("Column filtering applied:")
                        print(f"   Total columns: {len(all_columns)}")
                        print(f"   Display columns: {len(display_columns)} - {display_columns}")
                        print(f"   Hidden columns: {len(hidden_columns)} - {hidden_columns}")
                        
                        return {
                            'columns': display_columns,
                            'column_headers': column_headers,
                            'rows': filtered_rows,
                            'count': len(filtered_rows),
                            'report_name': report_def['rpt_name'],
                            'report_desc': report_def['rpt_desc'],
                            'all_columns': all_columns,
                            'hidden_columns': hidden_columns
                        }
                    else:
                        # No filtering needed - display all columns
                        print("No column filtering configured, displaying all columns")
                        
                        return {
                            'columns': all_columns,
                            'column_headers': {col: col for col in all_columns},
                            'rows': all_rows,
                            'count': len(all_rows),
                            'report_name': report_def['rpt_name'],
                            'report_desc': report_def['rpt_desc']
                        }
                    
                except Exception as sql_error:
                    print(f"❌ SQL Execution Error: {sql_error}")
                    print(f"❌ Error type: {type(sql_error).__name__}")
                    
                    # Return detailed error information
                    return {
                        'columns': ['Error Details'],
                        'rows': [
                            [f'SQL Error: {str(sql_error)}'],
                            [f'Report ID: {report_id}'],
                            [f'Query Length: {len(sql_query)} chars'],
                            [f'Parameters: {str(query_params)}']
                        ],
                        'count': 4
                    }
                    
        except Exception as e:
            print(f"❌ General Error executing dynamic report: {e}")
            import traceback
            traceback.print_exc()
            return {
                'columns': ['Error'],
                'rows': [[f'Error executing query: {str(e)}']],
                'count': 1
            }

    def build_query_parameters(self, sql_query, form_params):
        """Build query parameters based on SQL placeholders and form data"""
        query_params = {}
        
        # Standard session parameters - always include these
        query_params['comp_code'] = session.get('company_code')
        query_params['user_id'] = session.get('user_id')
        query_params['branch_code'] = session.get('branch_code')
        
        print(f"🔧 Session params: comp_code={query_params['comp_code']}, user_id={query_params['user_id']}")
        
        # Map form parameters to query parameters
        param_mapping = {
            'fromSdmCode': 'from_sdm_code',
            'toSdmCode': 'to_sdm_code', 
            'fromCustCode': 'from_cust_code',
            'toCustCode': 'to_cust_code',
            'fromFlashCode': 'from_flash_code',
            'toFlashCode': 'to_flash_code',
            'fromItemCode': 'from_item_code',
            'toItemCode': 'to_item_code',
            'fromLocnCode': 'from_locn_code',
            'toLocnCode': 'to_locn_code',
            'fromDate': 'from_date',
            'toDate': 'to_date',
            'Status': 'status'
        }
        
        print(f"🔧 Form params received: {form_params}")
        
        # Find all parameter placeholders in the SQL query
        import re
        placeholders = re.findall(r':(\w+)', sql_query)
        print(f"🔧 SQL placeholders found: {placeholders}")
        
        # Only add parameters that are actually used in the SQL
        for placeholder in placeholders:
            if placeholder in ['comp_code', 'user_id', 'branch_code']:
                # Already added above
                continue
            elif placeholder in param_mapping.values():
                # Find the form key for this query parameter
                form_key = None
                for fk, qk in param_mapping.items():
                    if qk == placeholder:
                        form_key = fk
                        break
                
                if form_key and form_key in form_params and form_params[form_key]:
                    value = form_params[form_key].strip()
                    if value and value not in ['ZZZZZZ', '']:
                        query_params[placeholder] = value
                        print(f"🔧 Set {placeholder} = {value}")
                    else:
                        query_params[placeholder] = None
                        print(f"🔧 Set {placeholder} = None (empty/default)")
                else:
                    query_params[placeholder] = None
                    print(f"🔧 Set {placeholder} = None (not provided)")
            else:
                # Handle special cases
                if placeholder == 'from_date':
                    query_params['from_date'] = form_params.get('fromDate', '01/01/2020')
                elif placeholder == 'to_date':
                    query_params['to_date'] = form_params.get('toDate', datetime.now().strftime('%d/%m/%Y'))
                else:
                    query_params[placeholder] = None
                    print(f"🔧 Set {placeholder} = None (unknown parameter)")
        
        print(f"🔧 Final query params: {query_params}")
        return query_params
    
    def get_menu_report_id(self, menu_id):
        """Get report ID from menu parameters"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Get MENU_PARAMETER_1 which should contain the report ID
                query = """
                    SELECT MENU_PARAMETER_1, MENU_PARAMETER_2, MENU_PARAMETER_3
                    FROM MENU_MENUS 
                    WHERE MENU_ID = :menu_id
                """
                
                cursor.execute(query, {'menu_id': menu_id})
                result = cursor.fetchone()
                
                if result and result[0]:
                    return result[0]  # MENU_PARAMETER_1 contains report ID
                
                return None
                
        except Exception as e:
            print(f"Error getting menu report ID: {e}")
            return None


# Initialize service
dynamic_report_service = DynamicReportService()

# Export functions for use in routes
def get_dynamic_report_config(menu_id):
    """Get report configuration for a menu"""
    report_id = dynamic_report_service.get_menu_report_id(menu_id)
    if not report_id:
        return None
    
    report_def = dynamic_report_service.get_report_definition(report_id)
    if not report_def:
        return None
    
    return dynamic_report_service.build_parameter_form_config(report_def)


def execute_dynamic_report_query(menu_id, form_params):
    """Execute dynamic report query"""
    report_id = dynamic_report_service.get_menu_report_id(menu_id)
    if not report_id:
        return {
            'columns': ['Error'],
            'rows': [['Report ID not found in menu configuration']],
            'count': 0
        }
    
    return dynamic_report_service.execute_dynamic_report(report_id, form_params)


def generate_excel_report(report_data, report_id, params):
    """Generate Excel report"""
    try:
        # Create DataFrame
        df = pd.DataFrame(report_data['rows'], columns=report_data['columns'])
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Report', index=False)
        
        output.seek(0)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_id}_{timestamp}.xlsx"
        
        return Response(
            output.getvalue(),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
        
    except Exception as e:
        print(f"Error generating Excel: {e}")
        flash(f'Error generating Excel: {str(e)}', 'danger')
        return redirect(url_for('dashboard.dashboard'))


def generate_pdf_report(report_data, form_id, params):
    """Generate PDF report - placeholder implementation"""
    try:
        flash('PDF generation not implemented yet. Showing view format.', 'info')
        return render_template(
            'reports/report_view.html',
            data=report_data,
            form_id=form_id,
            params=params,
            generated_at=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        )
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('dashboard.dashboard'))


# Legacy compatibility functions
def get_form_configuration(form_id, report_id):
    """Legacy function - redirects to dynamic config"""
    config = get_dynamic_report_config(form_id)
    if config:
        return config
    
    return {
        'title': 'Report Parameters',
        'parameters': [
            {
                'name': 'Date',
                'field': 'Date',
                'type': 'date_range',
                'required': True,
                'icon': 'fas fa-calendar-alt'
            }
        ]
    }


def execute_report_query(form_id, params):
    """Legacy function - redirects to dynamic execution"""
    result = execute_dynamic_report_query(form_id, params)
    if result and result.get('count', 0) > 0:
        return result
    
    return {
        'columns': ['Error'],
        'rows': [['Please configure this report in RPT_REPORT_MASTER table']],
        'count': 0
    }
