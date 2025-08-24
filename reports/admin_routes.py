from flask import Blueprint, render_template, request, jsonify, session
import oracledb
import json
from datetime import datetime
import traceback

admin_bp = Blueprint('admin', __name__)

def get_db_connection():
    """Get database connection"""
    try:
        from database import get_db_connection as get_db_conn
        return get_db_conn()
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@admin_bp.route('/')
def admin_dashboard():
    """Render the admin dashboard"""
    return render_template('reports/report_config_admin.html')

@admin_bp.route('/config/<report_id>', methods=['GET'])
def get_report_config(report_id):
    """Fetch report configuration by RPT_ID"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            
            # Fetch report configuration - simplified to match actual table structure
            query = """
            SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_PARAMS
            FROM RPT_REPORT_MASTER 
            WHERE RPT_ID = :report_id
            """
            
            cursor.execute(query, {'report_id': report_id})
            result = cursor.fetchone()
            
            if not result:
                return jsonify({
                    'success': False,
                    'error': f'Report {report_id} not found'
                }), 404
            
            # Handle CLOB for RPT_PARAMS - read within active connection
            rpt_params = result[5]
            print(f"DEBUG RPT_PARAMS type: {type(rpt_params)}")
            
            if rpt_params is not None:
                if hasattr(rpt_params, 'read'):
                    print(f"DEBUG Reading RPT_PARAMS CLOB for {report_id} within active connection...")
                    try:
                        rpt_params = rpt_params.read()
                        print(f"SUCCESS CLOB read successfully, length: {len(rpt_params)}")
                        print(f"DEBUG CLOB content type after read: {type(rpt_params)}")
                    except Exception as clob_error:
                        print(f"ERROR Error reading CLOB: {clob_error}")
                        rpt_params = None
                else:
                    print(f"DEBUG RPT_PARAMS is not a CLOB, it's: {type(rpt_params)}")
                    # Convert to string if it's not already
                    rpt_params = str(rpt_params)
            else:
                print(f"DEBUG RPT_PARAMS is None")
            
            # Parse JSON parameters
            try:
                params_json = json.loads(rpt_params) if rpt_params else {}
                print(f"SUCCESS JSON parsed successfully")
            except json.JSONDecodeError as e:
                print(f"ERROR JSON decode error: {e}")
                params_json = {}
            
            # Ensure all fields are JSON serializable
            rpt_source = result[4]
            if hasattr(rpt_source, 'read'):
                print(f"DEBUG Reading RPT_SOURCE CLOB for {report_id}")
                try:
                    rpt_source = rpt_source.read()
                    print(f"SUCCESS RPT_SOURCE CLOB read successfully")
                except Exception as e:
                    print(f"ERROR Error reading RPT_SOURCE CLOB: {e}")
                    rpt_source = str(rpt_source) if rpt_source else ""
            
            print(f"DEBUG Final data types: rpt_id={type(result[0])}, rpt_name={type(result[1])}, rpt_desc={type(result[2])}, rpt_type={type(result[3])}, rpt_source={type(rpt_source)}, params_json={type(params_json)}")
            
            report_data = {
                'rpt_id': str(result[0]) if result[0] else "",
                'rpt_name': str(result[1]) if result[1] else "",
                'rpt_desc': str(result[2]) if result[2] else "",
                'rpt_type': str(result[3]) if result[3] else "",
                'rpt_source': str(rpt_source) if rpt_source else "",
                'rpt_params': params_json,
                'created_by': 'SYSTEM',
                'created_date': None,
                'updated_by': 'SYSTEM', 
                'updated_date': None
            }
            
            print(f"SUCCESS Returning report data: {report_data}")
            return jsonify({
                'success': True,
                'data': report_data,
                'message': f'Report {report_id} loaded successfully'
            })
        
    except Exception as e:
        print(f"Error fetching report config: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/config/<report_id>', methods=['PUT'])
def update_report_config(report_id):
    """Update report configuration"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        print(f"DEBUG UPDATE - Report ID: {report_id}")
        print(f"DEBUG UPDATE - Received data keys: {list(data.keys()) if data else 'None'}")
        
        # Check RPT_PARAMS structure
        rpt_params = data.get('rpt_params', {})
        print(f"DEBUG UPDATE - RPT_PARAMS keys: {list(rpt_params.keys()) if rpt_params else 'None'}")
        print(f"DEBUG UPDATE - Parameters count: {len(rpt_params.get('parameters', []))}")
        print(f"DEBUG UPDATE - Display columns count: {len(rpt_params.get('display_columns', []))}")
        print(f"DEBUG UPDATE - Column headers count: {len(rpt_params.get('column_headers', {}))}")
        print(f"DEBUG UPDATE - Hidden columns count: {len(rpt_params.get('hidden_columns', []))}")
        
        cursor = connection.cursor()
        
        # Prepare JSON parameters
        rpt_params_json = json.dumps(rpt_params, indent=2)
        print(f"DEBUG UPDATE - RPT_PARAMS JSON length: {len(rpt_params_json)}")
        
        # Update query - simplified to match actual table structure
        update_query = """
        UPDATE RPT_REPORT_MASTER 
        SET RPT_NAME = :rpt_name,
            RPT_DESC = :rpt_desc,
            RPT_TYPE = :rpt_type,
            RPT_SOURCE = :rpt_source,
            RPT_PARAMS = :rpt_params,
            RPT_UPD_DT = SYSDATE,
            RPT_UPD_UID = 'ADMIN_WEB'
        WHERE RPT_ID = :report_id
        """
        
        cursor.execute(update_query, {
            'rpt_name': data.get('rpt_name'),
            'rpt_desc': data.get('rpt_desc'),
            'rpt_type': data.get('rpt_type'),
            'rpt_source': data.get('rpt_source'),
            'rpt_params': rpt_params_json,
            'report_id': report_id
        })
        
        rows_updated = cursor.rowcount
        print(f"DEBUG UPDATE - Rows updated: {rows_updated}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"SUCCESS UPDATE - Report {report_id} updated successfully")
        return jsonify({
            'success': True,
            'message': f'Report {report_id} updated successfully',
            'rows_updated': rows_updated,
            'params_preserved': len(rpt_params.get('parameters', [])),
            'column_headers_saved': len(rpt_params.get('column_headers', {}))
        })
        
    except Exception as e:
        print(f"ERROR UPDATE - Report {report_id}: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/config/<report_id>', methods=['POST'])
def create_report_config(report_id):
    """Create new report configuration"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        data = request.get_json()
        cursor = connection.cursor()
        
        # Check if report already exists
        check_query = "SELECT COUNT(*) FROM RPT_REPORT_MASTER WHERE RPT_ID = :report_id"
        cursor.execute(check_query, {'report_id': report_id})
        if cursor.fetchone()[0] > 0:
            return jsonify({
                'success': False,
                'error': f'Report {report_id} already exists'
            }), 400
        
        # Prepare JSON parameters
        rpt_params_json = json.dumps(data.get('rpt_params', {}), indent=2)
        
        # Insert query - simplified to match actual table structure
        insert_query = """
        INSERT INTO RPT_REPORT_MASTER 
        (RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_PARAMS)
        VALUES (:report_id, :rpt_name, :rpt_desc, :rpt_type, :rpt_source, :rpt_params)
        """
        
        cursor.execute(insert_query, {
            'report_id': report_id,
            'rpt_name': data.get('rpt_name'),
            'rpt_desc': data.get('rpt_desc'),
            'rpt_type': data.get('rpt_type'),
            'rpt_source': data.get('rpt_source'),
            'rpt_params': rpt_params_json
        })
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': f'Report {report_id} created successfully'
        })
        
    except Exception as e:
        print(f"Error creating report config: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/config/<report_id>', methods=['DELETE'])
def delete_report_config(report_id):
    """Delete report configuration"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if report exists
        check_query = "SELECT COUNT(*) FROM RPT_REPORT_MASTER WHERE RPT_ID = :report_id"
        cursor.execute(check_query, {'report_id': report_id})
        if cursor.fetchone()[0] == 0:
            return jsonify({
                'success': False,
                'error': f'Report {report_id} not found'
            }), 404
        
        # Delete query
        delete_query = "DELETE FROM RPT_REPORT_MASTER WHERE RPT_ID = :report_id"
        cursor.execute(delete_query, {'report_id': report_id})
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': f'Report {report_id} deleted successfully'
        })
        
    except Exception as e:
        print(f"Error deleting report config: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/reports/list', methods=['GET'])
def list_all_reports():
    """List all reports for dropdown/selection"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT RPT_ID, RPT_NAME, RPT_TYPE, RPT_SOURCE
        FROM RPT_REPORT_MASTER 
        ORDER BY RPT_ID
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        reports = []
        for row in results:
            reports.append({
                'rpt_id': row[0],
                'rpt_name': row[1],
                'rpt_type': row[2],
                'rpt_source': row[3]
            })
        
        cursor.close()
        connection.close()
        
        return jsonify(reports)
        
    except Exception as e:
        print(f"Error listing reports: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/analyze/<report_id>', methods=['GET'])
def analyze_report_structure(report_id):
    """Analyze report structure to suggest parameters and columns"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        # Get report info first
        cursor = connection.cursor()
        query = "SELECT RPT_TYPE, RPT_SOURCE FROM RPT_REPORT_MASTER WHERE RPT_ID = :report_id"
        cursor.execute(query, {'report_id': report_id})
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'error': f'Report {report_id} not found'}), 404
        
        rpt_type, rpt_source = result
        suggestions = {
            'parameters': [],
            'columns': [],
            'analysis': f'Report Type: {rpt_type}, Source: {rpt_source}'
        }
        
        if rpt_type == 'CLASS':
            # Try to read the Python file for parameter analysis
            try:
                import os
                py_file_path = os.path.join('reports', 'classes', f'{rpt_source.lower()}.py')
                if os.path.exists(py_file_path):
                    with open(py_file_path, 'r') as f:
                        content = f.read()
                        
                    # Extract potential parameters from the code
                    import re
                    param_matches = re.findall(r'params\.get\([\'"]([^\'"]+)[\'"]', content)
                    date_matches = re.findall(r'(from_date|to_date|start_date|end_date)', content)
                    
                    for param in set(param_matches + date_matches):
                        param_type = 'date' if 'date' in param.lower() else 'text'
                        suggestions['parameters'].append({
                            'name': param.replace('_', ' ').title(),
                            'field': param,
                            'type': param_type,
                            'required': 'date' in param.lower()
                        })
                        
            except Exception as e:
                suggestions['analysis'] += f' (Analysis error: {str(e)})'
        
        elif rpt_type == 'SQL':
            # Try to read the SQL file for parameter analysis
            try:
                import os
                sql_file_path = os.path.join('reports', 'sql', f'{rpt_source}.sql')
                if os.path.exists(sql_file_path):
                    with open(sql_file_path, 'r') as f:
                        content = f.read()
                        
                    # Extract bind variables from SQL
                    import re
                    bind_matches = re.findall(r':(\w+)', content)
                    
                    for bind_var in set(bind_matches):
                        if bind_var not in ['comp_code', 'user_id']:  # Skip global variables
                            param_type = 'date' if any(x in bind_var.lower() for x in ['date', 'dt', 'fm_dt', 'to_dt']) else 'text'
                            suggestions['parameters'].append({
                                'name': bind_var.replace('_', ' ').title(),
                                'field': bind_var,
                                'type': param_type,
                                'required': param_type == 'date'
                            })
                            
            except Exception as e:
                suggestions['analysis'] += f' (SQL Analysis error: {str(e)})'
        
        cursor.close()
        connection.close()
        
        return jsonify(suggestions)
        
    except Exception as e:
        print(f"Error analyzing report structure: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500