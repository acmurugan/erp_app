# ERP Application - Complete System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Database Architecture](#database-architecture)
4. [Folder Structure](#folder-structure)
5. [Application Architecture](#application-architecture)
6. [Core Components](#core-components)
7. [Report System Architecture](#report-system-architecture)
8. [Authentication & Session Management](#authentication--session-management)
9. [API Endpoints](#api-endpoints)
10. [Configuration Files](#configuration-files)
11. [Development Workflow](#development-workflow)
12. [Deployment Guide](#deployment-guide)

---

## System Overview

### Application Purpose
A comprehensive Enterprise Resource Planning (ERP) web application built with Flask, designed to replace Oracle Forms 6i with modern web technology. The system handles:
- Multi-company operations
- User authentication and session management
- Dynamic report generation (CLASS and SQL based)
- Menu hierarchy management
- Parameter-driven report forms
- Export functionality (Excel, View, PDF)

### Key Features
- **Modern Web Interface**: Bootstrap-based responsive design
- **Modular Report System**: Supports both Python CLASS and SQL report types
- **Dynamic Parameter Forms**: Auto-generated forms based on database configurations
- **Admin Interface**: Report configuration management with drag/drop column reordering
- **Multi-format Export**: View, Excel, PDF export capabilities
- **Session Management**: Secure user sessions with company/branch context
- **Global Variables**: Seamless mapping from Oracle Forms 6i global variables

---

## Technology Stack

### Backend
- **Python 3.12**: Core programming language
- **Flask 3.x**: Web framework
- **oracledb 2.x**: Oracle database connectivity (thin mode for Oracle 11g XE compatibility)
- **pandas**: Data manipulation and Excel export
- **openpyxl**: Excel file generation
- **Jinja2**: Template engine

### Frontend
- **Bootstrap 5.3**: CSS framework
- **JavaScript ES6**: Client-side scripting
- **Font Awesome**: Icons
- **jQuery**: DOM manipulation (minimal usage)

### Database
- **Oracle 11g XE**: Primary database
- **CLOB Storage**: Large configuration data (RPT_PARAMS)

### Development Tools
- **VS Code**: Recommended IDE
- **Git**: Version control
- **Flask Development Server**: Local development

---

## Database Architecture

### Core Tables

#### RPT_REPORT_MASTER
Primary table for report configurations:
```sql
CREATE TABLE RPT_REPORT_MASTER (
    RPT_ID VARCHAR2(20) PRIMARY KEY,
    RPT_NAME VARCHAR2(100),
    RPT_DESC VARCHAR2(500),
    RPT_TYPE VARCHAR2(10), -- 'CLASS', 'SQL', 'PROCEDURE', 'TEMPLATE'
    RPT_SOURCE CLOB,       -- Python class name or SQL query
    RPT_PARAMS CLOB,       -- JSON configuration
    RPT_OUTPUT_FORMATS VARCHAR2(100),
    RPT_CATEGORY VARCHAR2(50),
    RPT_ACTIVE_FLAG CHAR(1) DEFAULT 'Y',
    CREATED_BY VARCHAR2(30),
    CREATED_DATE DATE,
    UPDATED_BY VARCHAR2(30),
    UPDATED_DATE DATE
);
```

#### RPT_PARAMS JSON Structure
```json
{
    "parameters": [
        {
            "field": "fm_dt",
            "name": "From Date", 
            "type": "date",
            "required": true,
            "visible": true,
            "default": "01/01/2024"
        }
    ],
    "display_columns": ["COL1", "COL2"],
    "hidden_columns": ["COL3", "COL4"],
    "column_headers": {
        "COL1": "Column 1 Display Name"
    },
    "global_variables": {
        "comp_code": {
            "forms6i_mapping": ":GLOBAL.M_COMP_CODE",
            "web_mapping": "session[comp_code]"
        }
    },
    "ui_config": {
        "date_format": "DD/MM/YYYY",
        "theme": "bootstrap"
    }
}
```

### Menu System Tables
```sql
-- Menu hierarchy for navigation
CREATE TABLE SYS_MENU_MASTER (
    MENU_ID VARCHAR2(20) PRIMARY KEY,
    MENU_NAME VARCHAR2(100),
    PARENT_MENU_ID VARCHAR2(20),
    MENU_LEVEL NUMBER,
    MENU_URL VARCHAR2(200),
    ACTIVE_FLAG CHAR(1)
);
```

---

## Folder Structure

```
erp_app/
│
├── app.py                          # Main Flask application entry point
├── config.py                       # Application configuration
├── database.py                     # Oracle database connection management
├── utils.py                        # Utility functions
├── requirements.txt                # Python dependencies
├── start_erp.bat                  # Windows startup script
├── SYSTEM_DOCUMENTATION.md        # This documentation
│
├── reports/                        # Report system modules
│   ├── __init__.py                # Reports package initialization
│   ├── main_routes.py             # Core report routing and logic
│   ├── admin_routes.py            # Report administration interface
│   ├── core.py                    # Report configuration loading
│   ├── debug_visibility.py       # Debug utilities for parameter visibility
│   │
│   ├── classes/                   # Python CLASS-based reports
│   │   ├── __init__.py
│   │   ├── fin001.py             # Trial Balance Report
│   │   ├── fin006.py             # Financial Report
│   │   ├── ttl202.py             # Transaction Report
│   │   └── ttl308.py             # Transaction Analysis
│   │
│   ├── sql/                       # SQL-based reports
│   │   ├── TTL201.sql            # SQL Query for TTL201 report
│   │   └── TTL715.sql            # SQL Query for TTL715 report
│   │
│   └── executors/                 # Report execution engines
│       ├── __init__.py
│       ├── class_executor.py     # Python CLASS report executor
│       └── sql_executor.py       # SQL report executor
│
├── services/                      # Business logic services
│   ├── __init__.py
│   ├── menu_service.py           # Menu hierarchy management
│   ├── session_service.py        # Session management utilities
│   └── report_service.py         # Report generation services
│
├── templates/                     # Jinja2 HTML templates
│   ├── base.html                 # Base template with common layout
│   ├── login.html                # Login form
│   ├── dashboard.html            # Main dashboard
│   ├── error.html                # Error page template
│   │
│   └── reports/                  # Report-specific templates
│       ├── form.html             # Dynamic parameter form
│       ├── view.html             # Report display template
│       ├── report_config_admin.html  # Admin configuration interface
│       └── list.html             # Report listing
│
├── static/                       # Static assets
│   ├── css/                     
│   │   ├── custom.css           # Custom styles
│   │   └── admin.css            # Admin interface styles
│   ├── js/
│   │   ├── common.js            # Common JavaScript utilities
│   │   ├── reports.js           # Report-specific scripts
│   │   └── admin.js             # Admin interface scripts
│   └── images/
│       └── logo.png             # Application logo
│
└── migrations/                   # Database migration scripts
    ├── 001_create_tables.sql     # Initial table creation
    ├── 002_sample_data.sql       # Sample report configurations
    └── README.md                 # Migration instructions
```

---

## Application Architecture

### MVC Pattern Implementation

#### Model Layer
- **database.py**: Database connection and basic operations
- **reports/core.py**: Report configuration data access
- **services/**: Business logic services

#### View Layer  
- **templates/**: Jinja2 HTML templates
- **static/**: CSS, JavaScript, and images
- **Bootstrap framework**: Responsive UI components

#### Controller Layer
- **app.py**: Main application routing
- **reports/main_routes.py**: Report generation logic
- **reports/admin_routes.py**: Administration interface
- **services/**: Service layer controllers

### Request Flow
```
User Request
    ↓
app.py (Main Router)
    ↓
Route Handler (main_routes.py/admin_routes.py)
    ↓
Service Layer (services/)
    ↓
Data Access (core.py/database.py)
    ↓
Oracle Database
    ↓
Template Rendering (templates/)
    ↓
Response to User
```

---

## Core Components

### 1. Application Entry Point (app.py)
```python
# Key responsibilities:
# - Flask app initialization
# - Blueprint registration
# - Session configuration
# - Global error handling
# - Development server startup

from flask import Flask, session, request, redirect, url_for
from reports import reports_bp
from services.menu_service import get_menu_hierarchy

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.register_blueprint(reports_bp, url_prefix='/reports')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
```

### 2. Database Connection (database.py)
```python
# Oracle database connection management
import oracledb

def get_db_connection():
    """
    Returns Oracle database connection using thin mode
    Compatible with Oracle 11g XE
    """
    connection = oracledb.connect(
        user="your_user",
        password="your_password", 
        dsn="localhost:1521/XE",
        mode=oracledb.THIN_MODE
    )
    return connection

def execute_query(query, params=None):
    """Execute SELECT query and return results"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or {})
        return cursor.fetchall()
```

### 3. Report Core (reports/core.py)
```python
# Report configuration loading and management
def get_report_config(form_id):
    """
    Load report configuration from RPT_REPORT_MASTER
    Handles CLOB data and JSON parsing
    """
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT RPT_ID, RPT_NAME, RPT_TYPE, RPT_SOURCE, RPT_PARAMS 
            FROM RPT_REPORT_MASTER 
            WHERE RPT_ID = :form_id
        """, {'form_id': form_id})
        
        result = cursor.fetchone()
        if not result:
            return None
            
        # Handle CLOB data
        rpt_params = result[4]
        if hasattr(rpt_params, 'read'):
            rpt_params_content = rpt_params.read()
        else:
            rpt_params_content = str(rpt_params)
            
        return {
            'id': result[0],
            'name': result[1], 
            'type': result[2],
            'source': result[3],
            'params': json.loads(rpt_params_content)
        }
```

---

## Report System Architecture

### Universal Report Processing System

The ERP application implements a **Universal Report System** that handles any RPT_PARAMS format dynamically:

#### 1. Parameter Processing Pipeline
```
RPT_PARAMS (JSON) → parse_rpt_params_universal() → Form Fields
                                ↓
User Input → build_dynamic_parameters() → Executable Parameters
                                ↓
Report Executor (CLASS/SQL) → Data Results → Template Rendering
```

#### 2. Report Types Supported

##### CLASS Reports (Python-based)
Located in `reports/classes/`:
```python
# Example: fin001.py
class FIN001Report:
    def __init__(self):
        self.report_name = "Trial Balance Report"
    
    def generate(self, params):
        """
        Generate report data based on parameters
        Returns: pandas DataFrame or dict
        """
        comp_code = params.get('comp_code')
        fm_yyyymm = params.get('M_FM_YYYYMM')
        
        # Business logic here
        data = self.fetch_trial_balance_data(comp_code, fm_yyyymm)
        return data
    
    def fetch_trial_balance_data(self, comp_code, period):
        # Database queries and calculations
        pass
```

##### SQL Reports
Located in `reports/sql/`:
```sql
-- Example: TTL715.sql
SELECT 
    TXN_CODE as TXN,
    TXN_DATE as DT,
    DOC_NUMBER as NUM,
    LOCATION_CODE as LOCN,
    SUPPLIER_CODE as CODE,
    SUPPLIER_NAME as NAME,
    CASE WHEN ITEM_COUNT > 0 THEN 'Y' ELSE 'N' END as ITEM,
    TXN_TYPE_DESC as TXN_TYPE,
    CREATED_BY as UID
FROM TRANSACTION_PENDING_VIEW
WHERE TXN_DATE BETWEEN :FM_DT AND :TO_DT
  AND TXN_CODE BETWEEN :FM_TXN_CODE AND :TO_TXN_CODE
ORDER BY TXN_DATE, TXN_CODE
```

#### 3. Parameter Visibility System
```json
{
    "parameters": [
        {
            "field": "FM_DT",
            "name": "From Date",
            "type": "date",
            "visible": false,  // Hidden parameter
            "default": "01/01/2024"  // Auto-applied default
        },
        {
            "field": "TO_DT", 
            "name": "To Date",
            "type": "date",
            "visible": true,   // Visible in form
            "required": true
        }
    ]
}
```

### Report Execution Flow

#### 1. Form Generation (`/reports/form/<report_id>`)
```python
def dynamic_form(form_id, menu_id):
    # Load report configuration
    config = get_report_config(form_id)
    
    # Parse parameters for form display (visible only)
    form_params = parse_rpt_params_universal(config['params'], config['type'], filter_hidden=True)
    
    # Render dynamic form
    return render_template('reports/form.html', parameters=form_params)
```

#### 2. Report Generation (`/reports/<form_id>/<menu_id>/generate`)
```python
def generate_report(form_id, menu_id):
    # Get form data
    form_data = request.form.to_dict()
    
    # Load report configuration
    config = get_report_config(form_id)
    
    # Build complete parameters (including hidden ones with defaults)
    params = build_dynamic_parameters(form_data, session, config)
    
    # Execute based on report type
    if config['type'] == 'CLASS':
        result = class_executor.execute(form_id, params)
    elif config['type'] == 'SQL':
        result = sql_executor.execute(form_id, params)
    
    # Format output based on request
    output_format = form_data.get('outputFormat', 'view')
    if output_format == 'excel':
        return generate_excel_response(result)
    else:
        return render_template('reports/view.html', data=result)
```

#### 3. Hidden Parameter Processing
```python
def build_dynamic_parameters(form_data, session, report_config):
    """
    Combines visible form data with hidden parameter defaults
    """
    params = form_data.copy()
    
    # Add session variables
    params['comp_code'] = session.get('comp_code')
    params['user_id'] = session.get('user_id')
    
    # Process hidden parameters from config
    rpt_params = report_config.get('params', {})
    for param in rpt_params.get('parameters', []):
        if param.get('visible', True) == False:
            field = param.get('field')
            default = param.get('default', '')
            if field and field not in params:
                params[field] = default
                # Add both case variations for Oracle compatibility
                params[field.upper()] = default
    
    return params
```

---

## Authentication & Session Management

### Session Structure
```python
session = {
    'user_id': 'ADMIN',
    'comp_code': 'TTM', 
    'branch_code': '001',
    'login_time': datetime.now(),
    'menu_access': ['M01', 'M02', 'R01'],
    'is_authenticated': True
}
```

### Login Process
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        comp_code = request.form.get('comp_code')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        branch_code = request.form.get('branch_code', '')
        
        # Validate credentials against database
        if validate_user(comp_code, user_id, password):
            session['user_id'] = user_id
            session['comp_code'] = comp_code
            session['branch_code'] = branch_code
            session['is_authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')
```

### Authentication Decorator
```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

---

## API Endpoints

### Core Application Routes
```
GET  /                          # Home page (redirects to dashboard)
GET  /login                     # Login form
POST /login                     # Process login
GET  /logout                    # Logout and clear session
GET  /dashboard                 # Main dashboard
GET  /clear-session            # Emergency session clear
```

### Report Routes (`/reports` prefix)
```
GET  /reports/                                    # Report listing
GET  /reports/form/<report_id>                   # Parameter form
GET  /reports/<report_id>/<menu_id>              # Dynamic form
POST /reports/<report_id>/<menu_id>/generate     # Generate report
POST /reports/dynamic/<menu_id>/generate         # Generate from dynamic form
```

### Admin Routes (`/reports/admin` prefix)
```
GET  /reports/admin/                             # Admin dashboard
GET  /reports/admin/config                       # Configuration interface
GET  /reports/admin/config/<report_id>           # Get report config
PUT  /reports/admin/config/<report_id>           # Update report config
POST /reports/admin/config/<report_id>           # Create report config
```

### Debug Routes (`/reports/debug` prefix)
```
GET  /reports/debug/test-parameter-visibility/<report_id>  # Test parameter filtering
GET  /reports/debug/test-parameter-processing/<report_id>  # Test parameter processing
```

---

## Configuration Files

### 1. config.py
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database Configuration
    ORACLE_USER = os.environ.get('ORACLE_USER') or 'your_user'
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD') or 'your_password'
    ORACLE_DSN = os.environ.get('ORACLE_DSN') or 'localhost:1521/XE'
    
    # Session Configuration
    SESSION_TIMEOUT = 30 * 60  # 30 minutes
    PERMANENT_SESSION_LIFETIME = SESSION_TIMEOUT
    
    # Report Configuration
    REPORTS_PER_PAGE = 50
    MAX_EXPORT_ROWS = 10000
    DEFAULT_DATE_FORMAT = 'DD/MM/YYYY'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
```

### 2. requirements.txt
```
Flask==3.0.0
oracledb==2.0.1
pandas==2.1.4
openpyxl==3.1.2
Jinja2==3.1.2
Werkzeug==3.0.1
```

### 3. start_erp.bat (Windows)
```batch
@echo off
echo Starting ERP Application...
cd /d "C:\SourceCode\Orion_Claude\erp_app"
python app.py
pause
```

---

## Development Workflow

### 1. Adding New Reports

#### CLASS Report Example:
```python
# 1. Create reports/classes/new_report.py
class NEW001Report:
    def __init__(self):
        self.report_name = "New Report"
    
    def generate(self, params):
        # Implementation
        return data

# 2. Add to RPT_REPORT_MASTER
INSERT INTO RPT_REPORT_MASTER (
    RPT_ID, RPT_NAME, RPT_TYPE, RPT_SOURCE, RPT_PARAMS
) VALUES (
    'NEW001',
    'New Report', 
    'CLASS',
    'NEW001',
    '{"parameters":[...],"display_columns":[...]}'
);
```

#### SQL Report Example:
```sql
-- 1. Create reports/sql/NEW002.sql
SELECT col1, col2 FROM table WHERE date = :FM_DT

-- 2. Add to RPT_REPORT_MASTER
INSERT INTO RPT_REPORT_MASTER (
    RPT_ID, RPT_NAME, RPT_TYPE, RPT_SOURCE, RPT_PARAMS
) VALUES (
    'NEW002',
    'New SQL Report',
    'SQL', 
    'NEW002',
    '{"parameters":[{"field":"FM_DT","name":"Date","type":"date","visible":true}]}'
);
```

### 2. Database Migration Process

#### Step 1: Create Migration File
```sql
-- migrations/003_add_new_table.sql
CREATE TABLE NEW_TABLE (
    ID NUMBER PRIMARY KEY,
    NAME VARCHAR2(100),
    CREATED_DATE DATE DEFAULT SYSDATE
);

-- Add sample data
INSERT INTO NEW_TABLE (ID, NAME) VALUES (1, 'Sample');
COMMIT;
```

#### Step 2: Apply Migration
```bash
sqlplus username/password@XE
@migrations/003_add_new_table.sql
```

### 3. Testing Workflow

#### Unit Testing Structure
```python
# tests/test_reports.py
import unittest
from reports.core import get_report_config
from reports.main_routes import build_dynamic_parameters

class TestReports(unittest.TestCase):
    def test_report_config_loading(self):
        config = get_report_config('FIN001')
        self.assertIsNotNone(config)
        self.assertEqual(config['type'], 'CLASS')
    
    def test_parameter_building(self):
        form_data = {'to_dt': '31/12/2024'}
        session = {'comp_code': 'TTM', 'user_id': 'ADMIN'}
        config = {'params': {'parameters': []}}
        
        params = build_dynamic_parameters(form_data, session, config)
        self.assertIn('comp_code', params)
        self.assertIn('user_id', params)
```

---

## Deployment Guide

### 1. Prerequisites
- Python 3.12+
- Oracle 11g XE
- Web server (Apache/Nginx) - optional for production

### 2. Installation Steps

#### Step 1: Clone and Setup
```bash
git clone <repository-url> erp_app
cd erp_app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Step 2: Database Setup
```sql
-- Run in SQL*Plus or SQL Developer
sqlplus username/password@XE
@migrations/001_create_tables.sql
@migrations/002_sample_data.sql
```

#### Step 3: Configuration
```python
# config.py - Update with your database credentials
ORACLE_USER = 'your_actual_user'
ORACLE_PASSWORD = 'your_actual_password'  
ORACLE_DSN = 'your_host:1521/XE'
SECRET_KEY = 'generate-strong-secret-key'
```

#### Step 4: Start Application
```bash
# Development
python app.py

# Production with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Production Configuration

#### Apache Virtual Host
```apache
<VirtualHost *:80>
    ServerName erp.yourcompany.com
    DocumentRoot /var/www/erp_app
    
    WSGIDaemonProcess erp_app python-path=/var/www/erp_app
    WSGIProcessGroup erp_app
    WSGIScriptAlias / /var/www/erp_app/app.wsgi
    
    <Directory /var/www/erp_app>
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

#### WSGI Configuration (app.wsgi)
```python
#!/usr/bin/python3
import sys
import os

sys.path.insert(0, "/var/www/erp_app/")

from app import app as application

if __name__ == "__main__":
    application.run()
```

---

## Key Architecture Decisions

### 1. Oracle Database Connectivity
- **Choice**: oracledb (thin mode) instead of cx_Oracle
- **Reason**: Better compatibility with Oracle 11g XE, no Oracle Client installation required
- **Benefit**: Simplified deployment, reduced dependencies

### 2. CLOB Storage for RPT_PARAMS
- **Choice**: Store report configurations as JSON in CLOB columns
- **Reason**: Flexible schema, can accommodate any report parameter structure
- **Benefit**: No schema changes needed for new report types

### 3. Universal Parameter Processing
- **Choice**: Single parameter processor for all report types
- **Reason**: Consistency across CLASS and SQL reports
- **Benefit**: Zero hardcoding, future-proof for new report formats

### 4. Modular Report System
- **Choice**: Separate executors for CLASS and SQL reports
- **Reason**: Different execution patterns, maintainable code
- **Benefit**: Easy to extend with new report types

### 5. Session-based Authentication
- **Choice**: Flask sessions instead of JWT tokens
- **Reason**: Simpler implementation, server-side session control
- **Benefit**: Easy session timeout management, logout control

---

## Future Enhancement Areas

### 1. Performance Optimizations
- Database connection pooling
- Query result caching
- Async report generation for large datasets

### 2. Security Enhancements
- Role-based access control (RBAC)
- API rate limiting  
- Input validation improvements
- SQL injection prevention

### 3. UI/UX Improvements
- Real-time report progress indicators
- Advanced filtering and search
- Report scheduling functionality
- Mobile responsiveness enhancements

### 4. Integration Capabilities
- REST API for external systems
- Email report delivery
- Automated report generation
- Data warehouse integration

---

## Troubleshooting Guide

### Common Issues

#### 1. Database Connection Errors
```python
# Error: DPY-6005: cannot connect to database
# Solution: Check Oracle service status, verify credentials
sqlplus username/password@XE  # Test connection
```

#### 2. CLOB Reading Issues
```python
# Error: CLOB data not accessible after connection close
# Solution: Read CLOB within active connection context
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    clob_data = result[0].read()  # Read within connection
```

#### 3. Report Parameter Binding
```python
# Error: ORA-01008: not all variables bound
# Solution: Ensure all SQL parameters have corresponding values
# Check build_dynamic_parameters() function
```

#### 4. Session Timeout Issues
```python
# Error: User logged out unexpectedly
# Solution: Check SESSION_TIMEOUT in config.py
# Verify session data persistence
```

---

## Maintenance Procedures

### 1. Database Maintenance
```sql
-- Weekly maintenance
ANALYZE TABLE RPT_REPORT_MASTER COMPUTE STATISTICS;
ANALYZE TABLE SYS_MENU_MASTER COMPUTE STATISTICS;

-- Monthly cleanup
DELETE FROM USER_SESSIONS WHERE LAST_ACCESS < SYSDATE - 30;
COMMIT;
```

### 2. Log Management
```python
# Configure logging in app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/erp_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 3. Backup Procedures
```bash
# Database backup
exp username/password@XE file=erp_backup.dmp tables=RPT_REPORT_MASTER,SYS_MENU_MASTER

# Application backup
tar -czf erp_app_backup_$(date +%Y%m%d).tar.gz erp_app/
```

---

This comprehensive documentation provides a complete understanding of the ERP application architecture, from database design to deployment procedures. Use this as a reference for future development and maintenance activities.

**System Status**: ✅ Fully Operational
**Last Updated**: $(date)
**Version**: 1.0
**Maintainer**: Development Team