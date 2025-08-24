# ===============================================
# STEP 3: CREATE report_manager.py FILE
# ===============================================
# Save this as: report_manager.py

import json
import re
from datetime import datetime

class ReportManager:
    """Central report management system"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.report_cache = {}
    
    def get_report_config(self, report_id):
        """Get report configuration from database"""
        if report_id in self.report_cache:
            return self.report_cache[report_id]
        
        cursor = self.db.cursor()
        query = """
            SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, 
                   RPT_PARAMS, RPT_OUTPUT_FORMATS, RPT_CATEGORY
            FROM RPT_REPORT_MASTER 
            WHERE RPT_ID = :1 AND RPT_ACTIVE_FLAG = 'Y'
        """
        cursor.execute(query, [report_id])
        result = cursor.fetchone()
        
        if result:
            config = {
                'id': result[0],
                'name': result[1],
                'description': result[2],
                'type': result[3],
                'source': result[4],
                'params': json.loads(result[5]) if result[5] else {},
                'output_formats': result[6].split(',') if result[6] else ['VIEW'],
                'category': result[7]
            }
            self.report_cache[report_id] = config
            return config
        
        return None
    
    def execute_report(self, report_id, parameters, user_context):
        """Execute report based on its type"""
        config = self.get_report_config(report_id)
        if not config:
            raise ValueError(f"Report {report_id} not found")
        
        print(f"📊 Executing report: {config['name']} (Type: {config['type']})")
        
        if config['type'] == 'SQL':
            return self._execute_sql_report(config, parameters, user_context)
        elif config['type'] == 'PROC':
            return self._execute_procedure_report(config, parameters, user_context)
        elif config['type'] == 'CLASS':
            return self._execute_class_report(config, parameters, user_context)
        else:
            raise ValueError(f"Unsupported report type: {config['type']}")
    
    def _execute_sql_report(self, config, parameters, user_context):
        """Execute SQL-based report"""
        cursor = self.db.cursor()
        
        # Build query parameters
        query_params = self._build_query_params(parameters, user_context, config)
        
        # Get SQL from config
        sql = config['source']
        
        print(f"🔍 Executing SQL with parameters: {query_params}")
        
        try:
            cursor.execute(sql, query_params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            print(f"✅ Query executed successfully. Columns: {len(columns)}, Rows: {len(rows)}")
            
            return {
                'columns': columns,
                'rows': rows,
                'count': len(rows),
                'report_info': config,
                'parameters_used': query_params
            }
            
        except Exception as e:
            print(f"❌ SQL execution error: {e}")
            print(f"📝 SQL: {sql[:200]}...")
            raise e
    
    def _execute_procedure_report(self, config, parameters, user_context):
        """Execute stored procedure report"""
        cursor = self.db.cursor()
        
        # Build query parameters
        query_params = self._build_query_params(parameters, user_context, config)
        
        # Get procedure name from config
        proc_name = config['source']
        
        print(f"🔧 Executing procedure: {proc_name} with parameters: {query_params}")
        
        try:
            # Execute stored procedure
            result = cursor.callproc(proc_name, list(query_params.values()))
            
            # If procedure returns a cursor, fetch results
            if hasattr(cursor, 'fetchall'):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall() if cursor.description else []
            else:
                columns = []
                rows = []
            
            print(f"✅ Procedure executed successfully. Columns: {len(columns)}, Rows: {len(rows)}")
            
            return {
                'columns': columns,
                'rows': rows,
                'count': len(rows),
                'report_info': config,
                'parameters_used': query_params,
                'procedure_result': result
            }
            
        except Exception as e:
            print(f"❌ Procedure execution error: {e}")
            print(f"📝 Procedure: {proc_name}")
            raise e
    
    def _execute_class_report(self, config, parameters, user_context):
        """Execute Python class-based report"""
        try:
            # Import the report class dynamically
            module_name, class_name = config['source'].rsplit('.', 1)
            module = __import__(module_name, fromlist=[class_name])
            report_class = getattr(module, class_name)
            
            # Instantiate and execute
            report_instance = report_class(self.db)
            query_params = self._build_query_params(parameters, user_context, config)
            
            print(f"🐍 Executing class report: {config['source']} with parameters: {query_params}")
            
            result = report_instance.execute(query_params, user_context)
            
            print(f"✅ Class report executed successfully")
            
            return {
                'columns': result.get('columns', []),
                'rows': result.get('rows', []),
                'count': result.get('count', 0),
                'report_info': config,
                'parameters_used': query_params,
                'custom_data': result.get('custom_data', {})
            }
            
        except Exception as e:
            print(f"❌ Class report execution error: {e}")
            print(f"📝 Class: {config['source']}")
            raise e
    
    def _build_query_params(self, parameters, user_context, config):
        """Build query parameters with user context and defaults"""
        params = {
            'comp_code': user_context['company_code'],
            'user_id': user_context['user_id']
        }
        
        # Get default parameters from config
        default_params = config.get('params', {}).get('default_params', {})
        
        # Add default values first
        for key, value in default_params.items():
            params[key] = value
        
        # Override with user-provided parameters
        for key, value in parameters.items():
            if value and value.strip():
                # Handle range parameters
                if key.startswith('from') or key.startswith('to'):
                    # Convert form field names to parameter names
                    param_name = self._convert_field_name_to_param(key)
                    if value != 'ZZZZZZ':  # Don't override ZZZZZZ values
                        params[param_name] = value.upper()
                    else:
                        params[param_name] = value
                else:
                    params[key] = value.upper() if isinstance(value, str) else value
        
        # Ensure all required parameters exist (set to None if not provided)
        required_params = [
            'from_sdm_code', 'to_sdm_code',
            'from_cust_code', 'to_cust_code', 
            'from_flash_code', 'to_flash_code',
            'from_item_code', 'to_item_code',
            'from_locn_code', 'to_locn_code',
            'from_date', 'to_date'
        ]
        
        for param in required_params:
            if param not in params:
                params[param] = None
        
        return params
    
    def _convert_field_name_to_param(self, field_name):
        """Convert form field names to SQL parameter names"""
        # Convert camelCase to snake_case with proper prefixes
        mapping = {
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
            'toDate': 'to_date'
        }
        
        return mapping.get(field_name, field_name.lower())
    
    def get_parameter_form_config(self, report_id):
        """Get parameter form configuration for a report"""
        config = self.get_report_config(report_id)
        if not config:
            return None
        
        return config.get('params', {})
    
    def get_available_reports(self, category=None):
        """Get list of available reports"""
        cursor = self.db.cursor()
        
        if category:
            query = """
                SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_CATEGORY, RPT_OUTPUT_FORMATS
                FROM RPT_REPORT_MASTER 
                WHERE RPT_ACTIVE_FLAG = 'Y' AND RPT_CATEGORY = :1
                ORDER BY RPT_NAME
            """
            cursor.execute(query, [category])
        else:
            query = """
                SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_CATEGORY, RPT_OUTPUT_FORMATS
                FROM RPT_REPORT_MASTER 
                WHERE RPT_ACTIVE_FLAG = 'Y'
                ORDER BY RPT_CATEGORY, RPT_NAME
            """
            cursor.execute(query)
        
        reports = []
        for row in cursor.fetchall():
            reports.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'category': row[3],
                'output_formats': row[4].split(',') if row[4] else ['VIEW']
            })
        
        return reports


class ParameterFormBuilder:
    """Dynamic parameter form builder"""
    
    @staticmethod
    def build_parameter_form_html(report_config, form_id, menu_id):
        """Build complete parameter form HTML"""
        params_config = report_config.get('params', {})
        parameters = params_config.get('parameters', [])
        
        # Build parameter fields
        parameter_fields = ""
        for param in parameters:
            if param['type'] == 'range':
                parameter_fields += ParameterFormBuilder._build_range_field(param)
            elif param['type'] == 'date_range':
                parameter_fields += ParameterFormBuilder._build_date_range_field(param)
            elif param['type'] == 'dropdown':
                parameter_fields += ParameterFormBuilder._build_dropdown_field(param)
        
        # Get today's date
        today = datetime.now().strftime('%d/%m/%Y')
        
        # Complete HTML template
        html_template = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report_config.get('name', 'Report Parameters')}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                body {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .main-container {{
                    padding: 20px;
                }}
                .parameter-card {{
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    margin-bottom: 20px;
                    padding: 25px;
                }}
                .card-header {{
                    background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    border-radius: 10px 10px 0 0;
                    padding: 15px 20px;
                    margin: -25px -25px 20px -25px;
                    border: none;
                }}
                .card-title {{
                    margin: 0;
                    font-size: 1.4rem;
                    font-weight: 600;
                }}
                .form-group {{
                    margin-bottom: 20px;
                }}
                .form-label {{
                    font-weight: 600;
                    color: #333;
                    margin-bottom: 8px;
                    display: block;
                }}
                .form-control, .form-select {{
                    border: 2px solid #e1e8ed;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-size: 14px;
                    transition: all 0.3s ease;
                }}
                .form-control:focus, .form-select:focus {{
                    border-color: #4facfe;
                    box-shadow: 0 0 0 0.2rem rgba(79, 172, 254, 0.25);
                }}
                .btn-primary {{
                    background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
                    border: none;
                    padding: 12px 30px;
                    border-radius: 25px;
                    font-weight: 600;
                    transition: transform 0.2s ease;
                }}
                .btn-primary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
                }}
                .btn-secondary {{
                    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    padding: 12px 30px;
                    border-radius: 25px;
                    font-weight: 600;
                    margin-left: 10px;
                    transition: transform 0.2s ease;
                }}
                .btn-secondary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }}
                .row {{
                    margin-bottom: 15px;
                }}
                .range-group {{
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    border: 1px solid #e9ecef;
                }}
                .range-title {{
                    font-weight: 600;
                    color: #495057;
                    margin-bottom: 15px;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="main-container">
                <div class="parameter-card">
                    <div class="card-header">
                        <h4 class="card-title">
                            <i class="fas fa-filter"></i>
                            {report_config.get('name', 'Report Parameters')}
                        </h4>
                    </div>
                    
                    <form id="parameterForm" action="/execute_report" method="post" target="_blank">
                        <input type="hidden" name="report_id" value="{report_config.get('id', '')}">
                        <input type="hidden" name="form_id" value="{form_id}">
                        <input type="hidden" name="menu_id" value="{menu_id}">
                        
                        {parameter_fields}
                        
                        <div class="text-center mt-4">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-play"></i> Execute Report
                            </button>
                            <button type="reset" class="btn btn-secondary">
                                <i class="fas fa-undo"></i> Reset
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
            <script>
                // Set today's date as default for date fields
                document.addEventListener('DOMContentLoaded', function() {{
                    const dateInputs = document.querySelectorAll('input[type="date"]');
                    const today = new Date().toISOString().split('T')[0];
                    
                    dateInputs.forEach(input => {{
                        if (!input.value) {{
                            input.value = today;
                        }}
                    }});
                    
                    // Set focus on first input
                    const firstInput = document.querySelector('input, select');
                    if (firstInput) {{
                        firstInput.focus();
                    }}
                }});
                
                // Form submission handler
                document.getElementById('parameterForm').addEventListener('submit', function(e) {{
                    const submitBtn = this.querySelector('button[type="submit"]');
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                    submitBtn.disabled = true;
                    
                    setTimeout(() => {{
                        submitBtn.innerHTML = '<i class="fas fa-play"></i> Execute Report';
                        submitBtn.disabled = false;
                    }}, 2000);
                }});
            </script>
        </body>
        </html>
        '''
        
        return html_template
    
    @staticmethod
    def _build_range_field(param):
        """Build range parameter field (from/to)"""
        field_name = param['name']
        field_label = param['label']
        
        # Convert to proper case names
        from_field = f"from{field_name.title().replace('_', '')}"
        to_field = f"to{field_name.title().replace('_', '')}"
        
        return f'''
        <div class="range-group">
            <div class="range-title">{field_label} Range</div>
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label">From {field_label}</label>
                    <input type="text" class="form-control" name="{from_field}" 
                           placeholder="Enter starting {field_label.lower()}" maxlength="10">
                </div>
                <div class="col-md-6">
                    <label class="form-label">To {field_label}</label>
                    <input type="text" class="form-control" name="{to_field}" 
                           placeholder="Enter ending {field_label.lower()}" maxlength="10" value="ZZZZZZ">
                </div>
            </div>
        </div>
        '''
    
    @staticmethod
    def _build_date_range_field(param):
        """Build date range parameter field"""
        field_name = param['name']
        field_label = param['label']
        
        return f'''
        <div class="range-group">
            <div class="range-title">{field_label} Range</div>
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label">From Date</label>
                    <input type="date" class="form-control" name="fromDate" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">To Date</label>
                    <input type="date" class="form-control" name="toDate" required>
                </div>
            </div>
        </div>
        '''
    
    @staticmethod
    def _build_dropdown_field(param):
        """Build dropdown parameter field"""
        field_name = param['name']
        field_label = param['label']
        options = param.get('options', [])
        
        options_html = ""
        for option in options:
            if isinstance(option, dict):
                value = option.get('value', '')
                text = option.get('text', value)
                selected = 'selected' if option.get('default', False) else ''
            else:
                value = text = str(option)
                selected = ''
            
            options_html += f'<option value="{value}" {selected}>{text}</option>'
        
        return f'''
        <div class="form-group">
            <label class="form-label">{field_label}</label>
            <select class="form-select" name="{field_name}">
                <option value="">-- Select {field_label} --</option>
                {options_html}
            </select>
        </div>
        '''


class ReportFormatter:
    """Report output formatting utilities"""
    
    @staticmethod
    def format_to_html_table(report_data):
        """Format report data to HTML table"""
        columns = report_data['columns']
        rows = report_data['rows']
        report_info = report_data['report_info']
        
        # Build table headers
        headers_html = ""
        for col in columns:
            headers_html += f'<th class="sortable" data-column="{col}">{col}</th>'
        
        # Build table rows
        rows_html = ""
        for i, row in enumerate(rows):
            row_class = "table-row-even" if i % 2 == 0 else "table-row-odd"
            rows_html += f'<tr class="{row_class}">'
            
            for j, cell in enumerate(row):
                cell_value = str(cell) if cell is not None else ""
                # Format numbers and dates appropriately
                if isinstance(cell, (int, float)) and j > 0:  # Skip first column (usually ID)
                    if isinstance(cell, float):
                        cell_value = f"{cell:,.2f}"
                    else:
                        cell_value = f"{cell:,}"
                
                rows_html += f'<td>{cell_value}</td>'
            
            rows_html += '</tr>'
        
        # Complete HTML table
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report_info['name']} - Report Output</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                body {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .report-container {{
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .report-header {{
                    background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .report-title {{
                    margin: 0;
                    font-size: 1.8rem;
                    font-weight: 600;
                }}
                .report-info {{
                    margin-top: 5px;
                    opacity: 0.9;
                    font-size: 0.9rem;
                }}
                .table-container {{
                    padding: 20px;
                    overflow-x: auto;
                }}
                .table {{
                    margin: 0;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .table th {{
                    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 15px 12px;
                    font-weight: 600;
                    cursor: pointer;
                    user-select: none;
                    position: relative;
                }}
                .table th:hover {{
                    background: linear-gradient(45deg, #5a6fd8 0%, #6a4190 100%);
                }}
                .table th.sortable::after {{
                    content: '\\f0dc';
                    font-family: 'Font Awesome 6 Free';
                    font-weight: 900;
                    position: absolute;
                    right: 8px;
                    opacity: 0.5;
                }}
                .table td {{
                    padding: 12px;
                    border-bottom: 1px solid #e9ecef;
                    vertical-align: middle;
                }}
                .table-row-even {{
                    background-color: #f8f9fa;
                }}
                .table-row-odd {{
                    background-color: white;
                }}
                .table-row-even:hover, .table-row-odd:hover {{
                    background-color: #e3f2fd !important;
                    transform: translateY(-1px);
                    transition: all 0.2s ease;
                }}
                .report-footer {{
                    background: #f8f9fa;
                    padding: 15px 20px;
                    text-align: center;
                    color: #6c757d;
                    border-top: 1px solid #e9ecef;
                }}
                .export-buttons {{
                    text-align: center;
                    padding: 20px;
                    background: #f8f9fa;
                }}
                .btn-export {{
                    margin: 0 5px;
                    padding: 8px 20px;
                    border-radius: 20px;
                    font-weight: 500;
                }}
            </style>
        </head>
        <body>
            <div class="report-container">
                <div class="report-header">
                    <h2 class="report-title">
                        <i class="fas fa-chart-bar"></i> {report_info['name']}
                    </h2>
                    <div class="report-info">
                        Generated on {datetime.now().strftime('%d/%m/%Y at %H:%M:%S')} | 
                        Total Records: {len(rows)}
                    </div>
                </div>
                
                <div class="export-buttons">
                    <button class="btn btn-success btn-export" onclick="exportToExcel()">
                        <i class="fas fa-file-excel"></i> Export to Excel
                    </button>
                    <button class="btn btn-danger btn-export" onclick="exportToPDF()">
                        <i class="fas fa-file-pdf"></i> Export to PDF
                    </button>
                    <button class="btn btn-info btn-export" onclick="window.print()">
                        <i class="fas fa-print"></i> Print
                    </button>
                </div>
                
                <div class="table-container">
                    <table class="table table-hover" id="reportTable">
                        <thead>
                            <tr>
                                {headers_html}
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
                
                <div class="report-footer">
                    <small>
                        Report ID: {report_info['id']} | 
                        Category: {report_info['category']} | 
                        <i class="fas fa-clock"></i> Generated in real-time
                    </small>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
            <script>
                // Table sorting functionality
                document.querySelectorAll('.sortable').forEach(header => {{
                    header.addEventListener('click', function() {{
                        sortTable(this.cellIndex);
                    }});
                }});
                
                function sortTable(columnIndex) {{
                    const table = document.getElementById('reportTable');
                    const tbody = table.querySelector('tbody');
                    const rows = Array.from(tbody.rows);
                    
                    const isNumeric = !isNaN(parseFloat(rows[0].cells[columnIndex].textContent.replace(/,/g, '')));
                    
                    rows.sort((a, b) => {{
                        const aVal = a.cells[columnIndex].textContent.trim();
                        const bVal = b.cells[columnIndex].textContent.trim();
                        
                        if (isNumeric) {{
                            return parseFloat(aVal.replace(/,/g, '') || 0) - parseFloat(bVal.replace(/,/g, '') || 0);
                        }} else {{
                            return aVal.localeCompare(bVal);
                        }}
                    }});
                    
                    rows.forEach(row => tbody.appendChild(row));
                }}
                
                function exportToExcel() {{
                    const wb = XLSX.utils.book_new();
                    const ws = XLSX.utils.table_to_sheet(document.getElementById('reportTable'));
                    XLSX.utils.book_append_sheet(wb, ws, 'Report Data');
                    XLSX.writeFile(wb, '{report_info["name"].replace(" ", "_")}.xlsx');
                }}
                
                function exportToPDF() {{
                    window.print();
                }}
            </script>
        </body>
        </html>
        '''
        
        return html
    
    @staticmethod
    def format_to_csv(report_data):
        """Format report data to CSV"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(report_data['columns'])
        
        # Write data rows
        for row in report_data['rows']:
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def format_to_excel(report_data):
        """Format report data to Excel (requires openpyxl)"""
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment
            
            wb = Workbook()
            ws = wb.active
            ws.title = "Report Data"
            
            # Add headers with styling
            headers = report_data['columns']
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
            
            # Add data rows
            for row_num, row_data in enumerate(report_data['rows'], 2):
                for col_num, value in enumerate(row_data, 1):
                    ws.cell(row=row_num, column=col_num, value=value)
            
            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            return wb
            
        except ImportError:
            raise ImportError("openpyxl is required for Excel export. Install with: pip install openpyxl")


class ReportExporter:
    """Handle different export formats"""
    
    def __init__(self, report_manager):
        self.report_manager = report_manager
    
    def export_report(self, report_data, format_type, filename=None):
        """Export report in specified format"""
        if not filename:
            report_name = report_data['report_info']['name'].replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{report_name}_{timestamp}"
        
        if format_type.upper() == 'HTML':
            return ReportFormatter.format_to_html_table(report_data)
        
        elif format_type.upper() == 'CSV':
            return ReportFormatter.format_to_csv(report_data)
        
        elif format_type.upper() == 'EXCEL':
            wb = ReportFormatter.format_to_excel(report_data)
            return wb
        
        elif format_type.upper() == 'JSON':
            import json
            export_data = {
                'report_info': report_data['report_info'],
                'generated_at': datetime.now().isoformat(),
                'columns': report_data['columns'],
                'data': [dict(zip(report_data['columns'], row)) for row in report_data['rows']],
                'summary': {
                    'total_records': len(report_data['rows']),
                    'parameters_used': report_data.get('parameters_used', {})
                }
            }
            return json.dumps(export_data, indent=2, default=str)
        
        else:
            raise ValueError(f"Unsupported export format: {format_type}")


class ReportCache:
    """Simple report caching mechanism"""
    
    def __init__(self, max_size=100, ttl_minutes=30):
        self.cache = {}
        self.max_size = max_size
        self.ttl_minutes = ttl_minutes
    
    def _generate_cache_key(self, report_id, parameters, user_context):
        """Generate unique cache key"""
        import hashlib
        
        key_data = {
            'report_id': report_id,
            'parameters': sorted(parameters.items()) if parameters else [],
            'user_context': user_context['company_code']
        }
        
        key_string = str(key_data)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, report_id, parameters, user_context):
        """Get cached report result"""
        cache_key = self._generate_cache_key(report_id, parameters, user_context)
        
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            
            # Check if cache is still valid
            cache_time = cached_item['timestamp']
            current_time = datetime.now()
            time_diff = (current_time - cache_time).total_seconds() / 60
            
            if time_diff < self.ttl_minutes:
                print(f"📋 Using cached result for report {report_id}")
                return cached_item['data']
            else:
                # Cache expired, remove it
                del self.cache[cache_key]
        
        return None
    
    def set(self, report_id, parameters, user_context, data):
        """Cache report result"""
        cache_key = self._generate_cache_key(report_id, parameters, user_context)
        
        # Remove oldest items if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now()
        }
        
        print(f"💾 Cached result for report {report_id}")
    
    def clear(self):
        """Clear all cached reports"""
        self.cache.clear()
        print("🗑️ Report cache cleared")


class EnhancedReportManager(ReportManager):
    """Enhanced report manager with caching and export capabilities"""
    
    def __init__(self, db_connection, enable_cache=True):
        super().__init__(db_connection)
        self.cache = ReportCache() if enable_cache else None
        self.exporter = ReportExporter(self)
    
    def execute_report(self, report_id, parameters, user_context, use_cache=True):
        """Enhanced execute report with caching"""
        
        # Try to get from cache first
        if self.cache and use_cache:
            cached_result = self.cache.get(report_id, parameters, user_context)
            if cached_result:
                return cached_result
        
        # Execute report normally
        result = super().execute_report(report_id, parameters, user_context)
        
        # Cache the result
        if self.cache and use_cache:
            self.cache.set(report_id, parameters, user_context, result)
        
        return result
    
    def export_report_data(self, report_data, format_type, filename=None):
        """Export report data in specified format"""
        return self.exporter.export_report(report_data, format_type, filename)
    
    def get_report_statistics(self):
        """Get report execution statistics"""
        cursor = self.db.cursor()
        
        # Get report usage statistics
        stats_query = """
            SELECT 
                COUNT(*) as total_reports,
                COUNT(CASE WHEN RPT_ACTIVE_FLAG = 'Y' THEN 1 END) as active_reports,
                COUNT(DISTINCT RPT_CATEGORY) as categories
            FROM RPT_REPORT_MASTER
        """
        
        cursor.execute(stats_query)
        stats = cursor.fetchone()
        
        # Get category breakdown
        category_query = """
            SELECT RPT_CATEGORY, COUNT(*) as report_count
            FROM RPT_REPORT_MASTER 
            WHERE RPT_ACTIVE_FLAG = 'Y'
            GROUP BY RPT_CATEGORY
            ORDER BY report_count DESC
        """
        
        cursor.execute(category_query)
        categories = cursor.fetchall()
        
        return {
            'total_reports': stats[0],
            'active_reports': stats[1],
            'total_categories': stats[2],
            'category_breakdown': [
                {'category': cat[0], 'count': cat[1]} 
                for cat in categories
            ],
            'cache_stats': {
                'cached_items': len(self.cache.cache) if self.cache else 0,
                'cache_enabled': self.cache is not None
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # This section would be used for testing the report manager
    print("ReportManager module loaded successfully!")
    print("Classes available:")
    print("- ReportManager: Core report execution")
    print("- ParameterFormBuilder: Dynamic form generation")
    print("- ReportFormatter: Output formatting")
    print("- ReportExporter: Export functionality")
    print("- ReportCache: Caching mechanism")
    print("- EnhancedReportManager: Full-featured manager")
    
    # Example configuration
    sample_config = {
        'id': 'RPT001',
        'name': 'Sales Summary Report',
        'description': 'Monthly sales summary by region',
        'type': 'SQL',
        'source': 'SELECT * FROM sales_view WHERE date_range = :from_date AND :to_date',
        'params': {
            'parameters': [
                {
                    'name': 'date',
                    'label': 'Date',
                    'type': 'date_range'
                },
                {
                    'name': 'region',
                    'label': 'Region',
                    'type': 'dropdown',
                    'options': [
                        {'value': 'NORTH', 'text': 'North Region'},
                        {'value': 'SOUTH', 'text': 'South Region'},
                        {'value': 'EAST', 'text': 'East Region'},
                        {'value': 'WEST', 'text': 'West Region'}
                    ]
                }
            ]
        },
        'output_formats': ['HTML', 'CSV', 'EXCEL'],
        'category': 'SALES'
    }
    
    print(f"\nSample configuration loaded: {sample_config['name']}")