# =============================================================================
# 3. reports/sql_executor.py - SQL and TEMPLATE Report Execution
# =============================================================================

from database import get_db_connection
from .core import load_sql_from_file

def execute_sql_report(report_id, config, params):
    """Execute SQL report (both traditional and modular)"""
    try:
        # Get SQL query (either from database or file)
        if config['is_modular']:
            sql_query = load_sql_from_file(config['sql_query'], config['type'])
        else:
            sql_query = config['sql_query']
        
        print(f"INFO SQL Query loaded, length: {len(sql_query)} characters")
        
        # Execute query
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, params)
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            result = {
                'count': len(rows),
                'columns': columns,
                'data': rows,
                'query': str(sql_query)[:200] + "..." if len(str(sql_query)) > 200 else str(sql_query),
                'parameters': params,
                'report_id': report_id,
                'is_modular': config['is_modular'],
                'report_type': config['type']
            }
            
            print(f"SUCCESS SQL query executed successfully. Rows: {len(rows)}")
            return result
            
    except Exception as e:
        print(f"ERROR Error executing SQL report: {e}")
        raise
