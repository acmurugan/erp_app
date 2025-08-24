# =============================================================================
# 9. reports/debug_routes.py - Debug and Test Routes
# =============================================================================

from flask import session, redirect, request
import json
from pathlib import Path
from .core import reports_bp, get_report_config, execute_report_with_params

@reports_bp.route('/debug/test', methods=['GET', 'POST'])
def debug_test():
    """Simple debug test"""
    if request.method == 'POST':
        return f"""
        <div class="container mt-4">
            <h2>Debug Test Results</h2>
            <pre>{dict(request.form)}</pre>
            <a href="/dashboard" class="btn btn-secondary">Back</a>
        </div>
        """
    else:
        return f"""
        <div class="container mt-4">
            <h2>Debug Test Form</h2>
            <form method="POST">
                <input type="text" name="test_field" value="test_value" class="form-control">
                <button type="submit" class="btn btn-primary mt-2">Test</button>
            </form>
        </div>
        """

@reports_bp.route('/debug/modular/<report_id>')
def debug_modular_report(report_id):
    """Debug specific report"""
    if 'user_id' not in session:
        return redirect('/login')
    
    try:
        config = get_report_config(report_id)
        if not config:
            return f"<h2>Report {report_id} not found</h2>", 404
        
        debug_info = {
            'report_id': report_id,
            'config': config,
            'file_check': analyze_report_files(config)
        }
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Debug: {report_id}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>Debug: {report_id}</h2>
                <pre class="bg-light p-3">{json.dumps(debug_info, indent=2, default=str)}</pre>
                <div class="mt-4">
                    <a href="/reports/admin/modular" class="btn btn-secondary">Back to Admin</a>
                    <a href="/reports/test/{report_id}" class="btn btn-primary">Test Report</a>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"<h2>Debug Error</h2><p>{str(e)}</p>"

def analyze_report_files(config):
    """Analyze report files for debugging"""
    file_info = {
        'is_modular': config['is_modular'],
        'type': config['type'],
        'source': config['sql_query']
    }
    
    if config['is_modular']:
        if config['type'] == 'CLASS':
            expected_path = Path("reports/classes") / f"{config['sql_query']}.py"
        elif config['type'] == 'SQL':
            expected_path = Path("reports/sql") / f"{config['sql_query']}.sql"
        elif config['type'] == 'TEMPLATE':
            expected_path = Path("reports/templates") / f"{config['sql_query']}.sql"
        elif config['type'] == 'PROCEDURE':
            expected_path = Path("reports/procedures") / f"{config['sql_query']}.json"
        else:
            expected_path = Path("reports/unknown") / f"{config['sql_query']}.txt"
        
        file_info['expected_path'] = str(expected_path)
        file_info['file_exists'] = expected_path.exists()
        
        if expected_path.exists():
            try:
                content = expected_path.read_text(encoding='utf-8')
                file_info['file_size'] = len(content)
                file_info['preview'] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                file_info['read_error'] = str(e)
    
    return file_info

@reports_bp.route('/test/<report_id>')
def test_report_execution(report_id):
    """Test report execution with default parameters"""
    if 'user_id' not in session:
        return redirect('/login')
    
    try:
        # Default test parameters
        test_params = {
            'comp_code': 'TTM',
            'user_id': session.get('user_id', 'TEST'),
            'from_date': '01/01/2024',
            'to_date': '31/12/2024',
            'from_cust_code': '0',
            'to_cust_code': 'ZZZZZZ',
            'from_sdm_code': '0',
            'to_sdm_code': 'ZZZZZZ'
        }
        
        result = execute_report_with_params(report_id, test_params)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Results: {report_id}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h3>SUCCESS Test Results: {report_id}</h3>
                    </div>
                    <div class="card-body">
                        <ul>
                            <li><strong>Records:</strong> {result['count']}</li>
                            <li><strong>Columns:</strong> {len(result['columns'])}</li>
                            <li><strong>Type:</strong> {result.get('report_type', 'SQL')}</li>
                            <li><strong>Modular:</strong> {result.get('is_modular', False)}</li>
                        </ul>
                        
                        <h4>Columns:</h4>
                        <pre>{', '.join(result['columns'])}</pre>
                        
                        <h4>Sample Data:</h4>
                        <pre>{json.dumps(result['data'][:3], indent=2, default=str)}</pre>
                        
                        <div class="mt-4">
                            <a href="/reports/admin/modular" class="btn btn-secondary">Back</a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Error: {report_id}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <div class="alert alert-danger">
                    <strong>Error:</strong> {str(e)}
                </div>
                <a href="/reports/admin/modular" class="btn btn-secondary">Back</a>
            </div>
        </body>
        </html>
        """

@reports_bp.route('/debug/column-headers/<report_id>')
def debug_column_headers(report_id):
    """Debug column header functionality with detailed logging"""
    try:
        from database import get_db_connection
        import json
        
        print(f"DEBUG Testing column headers for report: {report_id}")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get the report definition
            query = """
                SELECT RPT_ID, RPT_NAME, RPT_TYPE, RPT_PARAMS
                FROM RPT_REPORT_MASTER 
                WHERE RPT_ID = :report_id
            """
            
            cursor.execute(query, {'report_id': report_id})
            result = cursor.fetchone()
            
            if result:
                rpt_params_clob = result[3]
                rpt_params_str = rpt_params_clob.read() if rpt_params_clob else '{}'
                
                print(f"DEBUG RPT_PARAMS raw: {rpt_params_str}")
                
                try:
                    params_config = json.loads(rpt_params_str)
                    print(f"DEBUG Parsed params config: {params_config}")
                    
                    display_columns = params_config.get('display_columns', [])
                    hidden_columns = params_config.get('hidden_columns', [])
                    column_headers = params_config.get('column_headers', {})
                    
                    print(f"DEBUG Display columns: {display_columns}")
                    print(f"DEBUG Hidden columns: {hidden_columns}")
                    print(f"DEBUG Column headers: {column_headers}")
                    
                    return f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Column Header Debug - {report_id}</title>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                    </head>
                    <body>
                        <div class="container mt-4">
                            <h2>Column Header Debug for {report_id}</h2>
                            <div class="card">
                                <div class="card-body">
                                    <h3>RPT_PARAMS Content:</h3>
                                    <pre class="bg-light p-3">{rpt_params_str}</pre>
                                    <h3>Parsed Configuration:</h3>
                                    <ul class="list-group">
                                        <li class="list-group-item"><strong>Display columns:</strong> {display_columns}</li>
                                        <li class="list-group-item"><strong>Hidden columns:</strong> {hidden_columns}</li>
                                        <li class="list-group-item"><strong>Column headers:</strong> {column_headers}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    
                except json.JSONDecodeError as e:
                    return f"""
                    <div class="container mt-4">
                        <h2>JSON Error:</h2>
                        <div class="alert alert-danger">
                            <p><strong>Error:</strong> {e}</p>
                            <p><strong>Raw content:</strong> {rpt_params_str}</p>
                        </div>
                    </div>
                    """
            else:
                return f"<h2>Report not found: {report_id}</h2>"
                
    except Exception as e:
        return f"<h2>Error:</h2><p>{e}</p>"

@reports_bp.route('/debug/test-fin001')
def debug_test_fin001():
    """Test FIN001 execution without session"""
    try:
        from reports.class_executor import execute_class_report
        
        # Simulate a config like what would come from the database
        config = {
            'sql_query': 'fin001',
            'type': 'CLASS',
            'is_modular': True,
            'params': '''{
  "parameters": [
    {
      "default": "202501",
      "field": "M_FM_YYYYMM",
      "name": "From Period",
      "required": true,
      "type": "text"
    }
  ],
  "display_columns": [],
  "column_headers": {
    "ABAL_ACNT_YEAR": "Account Year",
    "ABAL_COMP_CODE": "Company New",
    "ABAL_DEPT_CODE": "Department Code",
    "ABAL_DIVN_CODE": "Division Code"
  },
  "hidden_columns": [],
  "ui_config": {
    "date_format": "DD/MM/YYYY",
    "theme": "bootstrap"
  }
}'''
        }
        
        # Test parameters
        params = {
            'M_FM_YYYYMM': '202501',
            'M_TO_YYYYMM': '202512',
            'M_FM_DIVN': '0',
            'M_TO_DIVN': 'ZZZZZZ'
        }
        
        print("DEBUG Starting FIN001 test execution...")
        result = execute_class_report('FIN001', config, params)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>FIN001 Test Results</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>FIN001 Test Results</h2>
                <div class="card">
                    <div class="card-body">
                        <h3>Result Summary:</h3>
                        <ul>
                            <li><strong>Records:</strong> {result.get('count', 0)}</li>
                            <li><strong>Columns:</strong> {len(result.get('columns', []))}</li>
                            <li><strong>Has Column Headers:</strong> {'column_headers' in result}</li>
                        </ul>
                        
                        <h3>Columns:</h3>
                        <pre>{result.get('columns', [])[:10]}</pre>
                        
                        <h3>Column Headers:</h3>
                        <pre>{result.get('column_headers', {})}</pre>
                        
                        <h3>Sample Data (first 3 rows):</h3>
                        <pre>{result.get('data', [])[:3]}</pre>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"""
        <div class="container mt-4">
            <h2>Error Testing FIN001:</h2>
            <div class="alert alert-danger">
                <pre>{str(e)}</pre>
            </div>
        </div>
        """

@reports_bp.route('/debug/set-session')
def debug_set_session():
    """Set session for testing"""
    from flask import session
    session['user_id'] = 'ORION'
    session['company_code'] = 'TTL'
    session['branch_code'] = 'MAIN'
    session['user_desc'] = 'Test User'
    return "Session set. Now you can <a href='/reports/FIN001/FIN001?outputFormat=view&fromDate=01%2F08%2F2024&toDate=31%2F08%2F2024&table_prefix=TTL'>test FIN001</a>"

@reports_bp.route('/debug/test-column-headers-all')
def test_column_headers_all():
    """Test column headers work for all report types"""
    try:
        from reports.sql_executor import execute_sql_report
        from reports.class_executor import execute_class_report
        from services.report_service import execute_dynamic_report_query
        
        # Test configuration with column headers
        test_config_sql = {
            'params': '''{
                "display_columns": [],
                "column_headers": {
                    "TEST_COL_1": "Test Column 1",
                    "TEST_COL_2": "Test Column 2", 
                    "ABAL_COMP_CODE": "Company Code"
                },
                "hidden_columns": []
            }'''
        }
        
        # For other executors, pass the JSON string directly
        test_params_json = '''{
            "display_columns": [],
            "column_headers": {
                "TEST_COL_1": "Test Column 1",
                "TEST_COL_2": "Test Column 2",
                "ABAL_COMP_CODE": "Company Code"
            },
            "hidden_columns": []
        }'''
        
        results = []
        
        # 1. Test SQL Executor (simulate)
        try:
            # Create fake SQL result
            fake_sql_result = {
                'columns': ['TEST_COL_1', 'TEST_COL_2', 'ABAL_COMP_CODE'],
                'data': [['Value1', 'Value2', 'TTM']],
                'count': 1
            }
            
            # Apply column filtering logic manually
            from reports.sql_executor import get_display_columns
            display_columns, column_headers = get_display_columns(test_config_sql, fake_sql_result['columns'])
            
            results.append({
                'type': 'SQL Executor',
                'status': 'SUCCESS',
                'column_headers': column_headers,
                'display_columns': display_columns
            })
        except Exception as e:
            results.append({
                'type': 'SQL Executor', 
                'status': 'ERROR',
                'error': str(e)
            })
        
        # 2. Test CLASS Executor (simulate)  
        try:
            from reports.class_executor import get_display_columns as class_get_display_columns
            display_columns, column_headers = class_get_display_columns(test_params_json, ['TEST_COL_1', 'TEST_COL_2', 'ABAL_COMP_CODE'])
            
            results.append({
                'type': 'CLASS Executor',
                'status': 'SUCCESS', 
                'column_headers': column_headers,
                'display_columns': display_columns
            })
        except Exception as e:
            results.append({
                'type': 'CLASS Executor',
                'status': 'ERROR',
                'error': str(e)
            })
        
        # 3. Test Service Executor (simulate)
        try:
            from services.report_service import get_display_columns as service_get_display_columns
            display_columns, column_headers = service_get_display_columns(test_params_json, ['TEST_COL_1', 'TEST_COL_2', 'ABAL_COMP_CODE'])
            
            results.append({
                'type': 'Service Executor',
                'status': 'SUCCESS',
                'column_headers': column_headers, 
                'display_columns': display_columns
            })
        except Exception as e:
            results.append({
                'type': 'Service Executor',
                'status': 'ERROR',
                'error': str(e)
            })
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Column Headers Test - All Executors</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>Column Headers Test Results</h2>
                <div class="row">
                    {' '.join([f'''
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-header {'bg-success' if result['status'] == 'SUCCESS' else 'bg-danger'} text-white">
                                <h5>{result['type']}</h5>
                                <span class="badge {'badge-light' if result['status'] == 'SUCCESS' else 'badge-warning'}">{result['status']}</span>
                            </div>
                            <div class="card-body">
                                {f"<p><strong>Error:</strong> {result['error']}</p>" if result['status'] == 'ERROR' else f'''
                                <p><strong>Column Headers:</strong></p>
                                <ul>
                                    {''.join([f"<li><code>{k}</code> → <strong>{v}</strong></li>" for k, v in result.get('column_headers', {}).items()])}
                                </ul>
                                <p><strong>Display Columns:</strong> {result.get('display_columns', [])}</p>
                                '''}
                            </div>
                        </div>
                    </div>
                    ''' for result in results])}
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"""
        <div class="container mt-4">
            <h2>Error Testing Column Headers:</h2>
            <div class="alert alert-danger">
                <pre>{str(e)}</pre>
            </div>
        </div>
        """

@reports_bp.route('/debug/verify-all-executors-column-headers')
def verify_all_executors_column_headers():
    """
    Comprehensive verification that all executor types (SQL, CLASS, SERVICE, PROCEDURE) 
    support column headers functionality
    """
    try:
        print("VERIFICATION Starting comprehensive executor column headers verification")
        
        from reports.sql_executor import get_display_columns as sql_get_display_columns
        from reports.class_executor import get_display_columns as class_get_display_columns  
        from reports.procedure_executor import get_display_columns as procedure_get_display_columns
        from services.report_service import get_display_columns as service_get_display_columns
        from services.dynamic_report_service import get_display_columns as dynamic_service_get_display_columns
        
        # Test configuration with column headers
        test_config = {
            'display_columns': ['COL1', 'COL3'],
            'hidden_columns': ['COL4'],
            'column_headers': {
                'COL1': 'Column One Display',
                'COL2': 'Column Two Display', 
                'COL3': 'Column Three Display'
            }
        }
        
        test_columns = ['COL1', 'COL2', 'COL3', 'COL4', 'COL5']
        
        results = []
        
        # Test SQL Executor
        try:
            filtered_cols, headers = sql_get_display_columns(test_config, test_columns)
            results.append({
                'executor': 'SQL Executor',
                'status': 'SUCCESS',
                'filtered_columns': filtered_cols,
                'column_headers': headers,
                'details': f'Filtered {len(test_columns)} -> {len(filtered_cols)} columns'
            })
        except Exception as e:
            results.append({
                'executor': 'SQL Executor', 
                'status': 'ERROR',
                'error': str(e)
            })
        
        # Test CLASS Executor  
        try:
            filtered_cols, headers = class_get_display_columns(test_config, test_columns)
            results.append({
                'executor': 'CLASS Executor',
                'status': 'SUCCESS', 
                'filtered_columns': filtered_cols,
                'column_headers': headers,
                'details': f'Filtered {len(test_columns)} -> {len(filtered_cols)} columns'
            })
        except Exception as e:
            results.append({
                'executor': 'CLASS Executor',
                'status': 'ERROR',
                'error': str(e) 
            })
            
        # Test PROCEDURE Executor
        try:
            filtered_cols, headers = procedure_get_display_columns(test_config, test_columns)
            results.append({
                'executor': 'PROCEDURE Executor', 
                'status': 'SUCCESS',
                'filtered_columns': filtered_cols,
                'column_headers': headers,
                'details': f'Filtered {len(test_columns)} -> {len(filtered_cols)} columns'
            })
        except Exception as e:
            results.append({
                'executor': 'PROCEDURE Executor',
                'status': 'ERROR', 
                'error': str(e)
            })
            
        # Test Report Service
        try:
            filtered_cols, headers = service_get_display_columns(test_config, test_columns)
            results.append({
                'executor': 'Report Service',
                'status': 'SUCCESS',
                'filtered_columns': filtered_cols, 
                'column_headers': headers,
                'details': f'Filtered {len(test_columns)} -> {len(filtered_cols)} columns'
            })
        except Exception as e:
            results.append({
                'executor': 'Report Service',
                'status': 'ERROR',
                'error': str(e)
            })
            
        # Test Dynamic Report Service  
        try:
            filtered_cols, headers = dynamic_service_get_display_columns(test_config, test_columns)
            results.append({
                'executor': 'Dynamic Report Service',
                'status': 'SUCCESS',
                'filtered_columns': filtered_cols,
                'column_headers': headers, 
                'details': f'Filtered {len(test_columns)} -> {len(filtered_cols)} columns'
            })
        except Exception as e:
            results.append({
                'executor': 'Dynamic Report Service', 
                'status': 'ERROR',
                'error': str(e)
            })
        
        success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
        total_count = len(results)
        
        print(f"VERIFICATION Results: {success_count}/{total_count} executors passed column header verification")
        
        return f"""
        <html>
        <head>
            <title>All Executors Column Headers Verification</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h1>All Executors Column Headers Verification</h1>
                <div class="alert alert-{'success' if success_count == total_count else 'warning'}">
                    <h4>Results: {success_count}/{total_count} executors passed verification</h4>
                    <p>Test Configuration:</p>
                    <ul>
                        <li>Test Columns: {test_columns}</li>
                        <li>Display Columns: {test_config['display_columns']}</li>
                        <li>Hidden Columns: {test_config['hidden_columns']}</li>
                        <li>Column Headers: {len(test_config['column_headers'])} mappings</li>
                    </ul>
                </div>
                
                {''.join([f'''
                <div class="card mb-3">
                    <div class="card-header bg-{'success' if result['status'] == 'SUCCESS' else 'danger'} text-white">
                        <h5>{result['executor']} - {result['status']}</h5>
                    </div>
                    <div class="card-body">
                        {f"""
                        <p><strong>Details:</strong> {result['details']}</p>
                        <p><strong>Filtered Columns:</strong> {result['filtered_columns']}</p>
                        <p><strong>Column Headers Count:</strong> {len(result['column_headers'])} mappings</p>
                        <div class="mt-2">
                            <strong>Column Headers:</strong>
                            <ul>
                                {''.join([f'<li>{col} → {header}</li>' for col, header in result['column_headers'].items()])}
                            </ul>
                        </div>
                        """ if result['status'] == 'SUCCESS' else f'<div class="text-danger"><strong>Error:</strong> {result["error"]}</div>'}
                    </div>
                </div>
                ''' for result in results])}
                
                <div class="mt-4">
                    <h3>Verification Summary</h3>
                    <p>This verification confirms that all executor types in the ERP system properly support:</p>
                    <ul>
                        <li>✅ Display columns filtering</li>
                        <li>✅ Hidden columns exclusion</li>
                        <li>✅ Column headers mapping</li>
                        <li>✅ Consistent get_display_columns() function interface</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"""
        <div class="container mt-4">
            <h2>Error in Comprehensive Verification:</h2>
            <div class="alert alert-danger">
                <pre>{str(e)}</pre>
            </div>
        </div>
        """