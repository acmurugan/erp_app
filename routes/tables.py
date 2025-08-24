from flask import Blueprint, render_template, redirect, url_for, session, flash
from database import get_db_connection

tables_bp = Blueprint('tables', __name__)

@tables_bp.route('/<table_name>')
def view_table(table_name):
    """View table data"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get column info
            cursor.execute("""
                SELECT column_name, data_type, nullable 
                FROM user_tab_columns 
                WHERE table_name = :1 
                ORDER BY column_id
            """, [table_name])
            
            columns = []
            for col_name, data_type, nullable in cursor.fetchall():
                columns.append({
                    'name': col_name,
                    'type': data_type,
                    'nullable': nullable == 'Y'
                })
            
            # Get data (limited)
            cursor.execute(f"SELECT * FROM {table_name} WHERE ROWNUM <= 50 ORDER BY 1")
            data = cursor.fetchall()
            
            # Get total count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_rows = cursor.fetchone()[0]
            
            return render_template('table_view.html',
                                 table_name=table_name,
                                 display_name=table_name.replace('_', ' ').title(),
                                 columns=columns,
                                 data=data,
                                 total_rows=total_rows,
                                 showing_rows=len(data))
                                 
    except Exception as e:
        flash(f'Error loading table {table_name}: {e}', 'danger')
        return redirect(url_for('dashboard.dashboard'))