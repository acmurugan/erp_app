from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import oracledb
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_change_this"

# Database configuration - UPDATE THESE IF DIFFERENT
DB_USER = "MOZ"
DB_PASS = "MOZ"
DB_DSN = "localhost/XE"
ORACLE_CLIENT_PATH = r"C:\instantclientOrcl\instantclient_19_28"

# Initialize Oracle client
try:
    oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
    print("Oracle client initialized successfully")
except Exception as e:
    print(f"Oracle client warning: {e}")

def get_db_connection():
    """Get database connection"""
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

# Available tables in your database (first 50 tables)
AVAILABLE_TABLES = ['ASSETH_PARAMETER_HIST', 'ASSET_CONTROL_TABLE', 'ASSET_PARAMETER', 'CUST_BLOCK_NOV12', 'DEL_LTED', 'FH_BANK_ACNT_DETAIL_HIST', 'FH_BANK_AUTH_PERSON_HIST', 'FH_BANK_CHQ_DETAIL_HIST', 'FH_BANK_CHQ_SIGN_DETAIL_HIST', 'FH_BANK_CHQ_SIGN_PANEL_HIST', 'FH_BANK_CHQ_STATUS_HIST', 'FH_BANK_CLEAR_TIME_HIST', 'FH_BANK_CONTACT_DETAIL_HIST', 'FH_BANK_HIST', 'FH_BANK_INTEREST_HIST', 'FH_BANK_LC_DETAIL_HIST', 'FH_BANK_OD_DETAIL_HIST', 'FH_BANK_RECO_BAL_HIST', 'FH_BANK_RECO_MATCH_SETUP_HIST', 'FH_BANK_TARIFF_HIST', 'FH_BANK_UPLOAD_FORMAT_HIST', 'FH_PANEL_HIST', 'FH_PANEL_MEMBERS_HIST', 'FH_ROUND_OFF_HIST', 'FIN_REP_INFO', 'FIR_ACNT1', 'FIXH_ADJ_REASON_HIST', 'FIXH_ASSET_HIST', 'FIXH_CATEGORY_HIST', 'FIXH_DOC_NUMBER_HIST', 'FIXH_EXPENSE_HIST', 'FIXH_LOCATION_HIST', 'FIXH_PERSON_HIST', 'FIXH_SUB_CATEGORY_HIST', 'FIX_ADJ_REASON', 'FIX_ASSET', 'FIX_CATEGORY', 'FIX_DAMAGE', 'FIX_DOC_NUMBER', 'FIX_EXPENSE', 'FIX_FLEXFIELD', 'FIX_LIFE_CHG_DETL', 'FIX_LIFE_CHG_HEAD', 'FIX_LOCATION', 'FIX_PURCHASE_DETAIL', 'FIX_PURCHASE_EXPENSE', 'FIX_PURCHASE_HEAD', 'FIX_REPAIR', 'FIX_SALE', 'FIX_SUB_CATEGORY']

@app.route('/')
def index():
    """Home page - redirect to login if not logged in"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password', 'danger')
            return render_template('login.html')
        
        # Simple authentication - you can enhance this
        # For now, any non-empty username/password works
        try:
            # Test database connection
            with get_db_connection():
                session['user_id'] = username
                session['user_name'] = username
                session['login_time'] = datetime.now().isoformat()
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Login failed: {e}', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard showing all tables"""
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    
    # Categorize tables for better display
    master_tables = []
    transaction_tables = []
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            for table_name in AVAILABLE_TABLES:
                # Get row count for each table
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    
                    table_info = {
                        'name': table_name,
                        'row_count': row_count,
                        'display_name': table_name.replace('_', ' ').title()
                    }
                    
                    # Simple categorization based on row count
                    if row_count < 5000:
                        master_tables.append(table_info)
                    else:
                        transaction_tables.append(table_info)
                        
                except Exception as e:
                    print(f"Warning: Could not get count for {table_name}: {e}")
                    master_tables.append({
                        'name': table_name,
                        'row_count': 0,
                        'display_name': table_name.replace('_', ' ').title()
                    })
    
    except Exception as e:
        flash(f'Error connecting to database: {e}', 'danger')
        master_tables = []
        transaction_tables = []
    
    return render_template('dashboard.html', 
                         master_tables=master_tables,
                         transaction_tables=transaction_tables,
                         user_name=session.get('user_name', 'User'))

@app.route('/table/<table_name>')
def view_table(table_name):
    """View data from a specific table"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if table_name not in AVAILABLE_TABLES:
        flash(f'Table {table_name} not found', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get column names
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
            
            # Get table data (limited to first 50 rows for performance)
            cursor.execute(f"SELECT * FROM {table_name} WHERE ROWNUM <= 50 ORDER BY 1")
            data = cursor.fetchall()
            
            # Get total row count
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
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         error_code=500, 
                         error_message="Internal server error"), 500

if __name__ == '__main__':
    print("Starting ERP Application...")
    print(f"Found {len(AVAILABLE_TABLES)} tables in database")
    print("Open http://localhost:5000 to access the application")
    print("Login with any username/password to start")
    print("-" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
