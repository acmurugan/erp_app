from flask import Flask
import oracledb
import os
from config import Config
from database import init_oracle_client
from utils import ensure_directories

# Import blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
# OLD: from routes.reports import reports_bp
# NEW: Import modular reports
from reports import create_reports_blueprint  # ✅ NEW IMPORT
from routes.tables import tables_bp
from routes.api import api_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Oracle client
init_oracle_client()

# Template filter for number formatting
@app.template_filter('number_format')
def number_format(value):
    """Format numbers with commas"""
    try:
        if isinstance(value, (int, float)):
            return "{:,}".format(int(value) if value % 1 == 0 else value)
        return value
    except:
        return value

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
# OLD: app.register_blueprint(reports_bp, url_prefix='/reports')
# NEW: Create and register modular reports blueprint
reports_bp = create_reports_blueprint()  # ✅ NEW LINE
app.register_blueprint(reports_bp, url_prefix='/reports')  # ✅ SAME REGISTRATION
app.register_blueprint(tables_bp, url_prefix='/table')
app.register_blueprint(api_bp, url_prefix='/api')

# Debug visibility blueprint
from reports.debug_visibility import debug_visibility_bp
app.register_blueprint(debug_visibility_bp, url_prefix='/debug')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    from flask import render_template
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    from flask import render_template
    return render_template('error.html',
                         error_code=500, 
                         error_message="Internal server error"), 500

if __name__ == '__main__':
    # Ensure necessary directories exist
    ensure_directories()
    
    print("\n" + "="*50)
    print("STARTING ERP APPLICATION")
    print("="*50)
    print("Multi-Company Login System Enabled")
    print("Enhanced Session Management")
    print("Complete Menu Hierarchy Support")
    print("Login/Logout Tracking Enabled")
    print("Report Parameter Forms")
    print("Excel Export Functionality")
    print("Modular Reports System")
    print("CLASS & PROCEDURE Reports Support")
    print("="*50)
    print("Open: http://localhost:5000")
    print("Login Fields: Company Code, User ID, Password, Branch Code (optional)")
    print("="*50)
    print("Emergency session clear: http://localhost:5000/clear-session")
    print("Debug Dashboard Test: http://localhost:5000/dashboard/simple-test")
    print("Debug Reports Admin: http://localhost:5000/reports/debug/admin-test")
    print("Reports Admin: http://localhost:5000/reports/admin/modular")
    print("Debug Menu Database: http://localhost:5000/dashboard/check-menu-database")
    print("Test Modular Reports: http://localhost:5000/reports/debug/test")
    print("Test TTL201 Report: http://localhost:5000/reports/test/TTL201")
    print("="*50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)