# =============================================================================
# File: reports/core.py
# Core functions and blueprint creation for modular reports
# =============================================================================

from flask import Blueprint
from pathlib import Path
import json

# Create the main blueprint - this is what gets imported and used
reports_bp = Blueprint('reports', __name__)

def get_report_config(form_id):
    """Get report configuration from RPT_REPORT_MASTER with modular support - FIXED VARIABLE NAMES AND CLOB"""
    try:
        from database import get_db_connection
        
        print(f"DEBUG Querying database for report: {form_id}")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_PARAMS, RPT_OUTPUT_FORMATS
                FROM RPT_REPORT_MASTER 
                WHERE RPT_ID = :form_id 
                AND RPT_ACTIVE_FLAG = 'Y'
            """, {'form_id': form_id})
            
            result = cursor.fetchone()
            if result:
                print(f"SUCCESS Found database record for {form_id}")
                
                # Handle LOB for RPT_SOURCE - READ WITHIN CONNECTION
                sql_query = result[3]
                if hasattr(sql_query, 'read'):
                    sql_query = sql_query.read()
                
                # Handle LOB for RPT_PARAMS - READ WITHIN CONNECTION
                rpt_params_content = result[4]
                if rpt_params_content and hasattr(rpt_params_content, 'read'):
                    print(f"DEBUG Reading RPT_PARAMS CLOB for {form_id} within active connection...")
                    try:
                        rpt_params_content = rpt_params_content.read()
                        print(f"SUCCESS CLOB read successfully, length: {len(rpt_params_content)}")
                        print(f"INFO CLOB preview: {rpt_params_content[:100]}...")
                    except Exception as clob_error:
                        print(f"ERROR Error reading CLOB within connection: {clob_error}")
                        rpt_params_content = None
                else:
                    print(f"WARNING RPT_PARAMS is null or not a CLOB for {form_id}")
                
                # Determine report type and if it's modular
                report_type = result[2] or 'SQL'
                is_modular = not (sql_query.strip().upper().startswith('SELECT') or 
                                sql_query.strip().upper().startswith('WITH') or
                                len(sql_query.strip()) > 100)
                
                # Parse output formats
                output_formats_str = result[5] or 'VIEW,EXCEL'
                output_formats = [fmt.strip().lower() for fmt in output_formats_str.split(',')]
                
                print(f"TARGET Config for {form_id}: Type={report_type}, Has_Params={rpt_params_content is not None}")
                
                return {
                    'id': form_id,  # Add the ID for reference
                    'name': result[0],
                    'description': result[1],
                    'type': report_type,
                    'sql_query': sql_query,
                    'params': rpt_params_content,  # This is now a string, not a CLOB object
                    'output_formats': output_formats,
                    'is_modular': is_modular
                }
            else:
                print(f"ERROR No database record found for {form_id}")
                return None
    except Exception as e:
        print(f"ERROR Error getting report config for {form_id}: {e}")
        import traceback
        traceback.print_exc()
        return None

def execute_report_with_params(report_id, params):
    """Main report execution dispatcher"""
    try:
        print(f"DEBUG Executing report: {report_id}")
        
        config = get_report_config(report_id)
        if not config:
            raise Exception(f"Report {report_id} not found")
        
        print(f"REPORT Report Type: {config['type']}")
        
        # Import executors dynamically to avoid circular imports
        if config['type'] == 'CLASS':
            from .class_executor import execute_class_report
            return execute_class_report(report_id, config, params)
        elif config['type'] == 'PROCEDURE':
            from .procedure_executor import execute_procedure_report
            return execute_procedure_report(report_id, config, params)
        else:
            from .sql_executor import execute_sql_report
            return execute_sql_report(report_id, config, params)
            
    except Exception as e:
        print(f"ERROR Error executing report: {e}")
        raise

def load_sql_from_file(source_reference, report_type):
    """Load SQL content from external file"""
    try:
        reports_base_path = Path("reports")
        
        if report_type == 'SQL':
            sql_file = reports_base_path / "sql" / f"{source_reference}.sql"
        elif report_type == 'TEMPLATE':
            sql_file = reports_base_path / "templates" / f"{source_reference}.sql"
        else:
            raise ValueError(f"Cannot load SQL file for report type: {report_type}")
        
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_file}")
        
        return sql_file.read_text(encoding='utf-8')
        
    except Exception as e:
        print(f"ERROR Error loading SQL from file: {e}")
        raise

print("Enhanced core.py loaded successfully!")
print("Features:")
print("   - Fixed variable name mismatch (form_id vs report_id)")
print("   - Proper CLOB reading within active database connection")
print("   - Enhanced debug logging for troubleshooting")
print("   - Error handling for CLOB operations")
print("   - Support for all report types (SQL/CLASS/PROCEDURE/TEMPLATE)")
print("Ready to read FIN006 RPT_PARAMS from database!")