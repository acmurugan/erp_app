# ERP Application - Developer Guide

## Quick Start for Developers

### Prerequisites Checklist
- [ ] Python 3.12+ installed
- [ ] Oracle 11g XE running
- [ ] Git installed
- [ ] VS Code or preferred IDE
- [ ] Basic knowledge of Flask and SQL

### 5-Minute Setup
```bash
# 1. Clone and setup virtual environment
git clone <repository> erp_app
cd erp_app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Configure database (edit config.py)
ORACLE_USER = 'your_user'
ORACLE_PASSWORD = 'your_password'

# 3. Run application
python app.py
# Open: http://127.0.0.1:5000
# Login: Company=TTM, User=ADMIN, Password=admin
```

---

## Development Patterns

### 1. Adding New Reports

#### Pattern A: Python CLASS Report
```python
# Step 1: Create reports/classes/new_report.py
class NEW001Report:
    def __init__(self):
        self.report_name = "New Business Report"
    
    def generate(self, params):
        """
        Main report generation method
        Args:
            params (dict): All parameters including session variables
        Returns:
            pandas.DataFrame or dict with 'data' and 'columns'
        """
        # Extract parameters
        comp_code = params.get('comp_code')
        from_date = params.get('fm_dt')
        to_date = params.get('to_dt')
        
        # Business logic
        data = self.fetch_business_data(comp_code, from_date, to_date)
        
        return {
            'data': data,
            'columns': ['COL1', 'COL2', 'COL3'],
            'title': f'Business Report for {comp_code}'
        }
    
    def fetch_business_data(self, comp_code, from_date, to_date):
        """Fetch data from database"""
        from database import get_db_connection
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT col1, col2, col3 
                FROM business_table 
                WHERE comp_code = :comp_code 
                AND date_field BETWEEN :from_date AND :to_date
            """, {
                'comp_code': comp_code,
                'from_date': from_date,
                'to_date': to_date
            })
            return cursor.fetchall()

# Step 2: Register in database
INSERT INTO RPT_REPORT_MASTER (RPT_ID, RPT_NAME, RPT_TYPE, RPT_SOURCE, RPT_PARAMS) 
VALUES ('NEW001', 'New Business Report', 'CLASS', 'NEW001', '{...json...}');
```

#### Pattern B: SQL Report
```sql
-- Step 1: Create reports/sql/NEW002.sql
-- New SQL Report
-- Parameters: :FM_DT, :TO_DT, :COMP_CODE
SELECT 
    t.transaction_id as TXN_ID,
    t.transaction_date as TXN_DATE,
    t.amount as AMOUNT,
    t.status as STATUS,
    c.customer_name as CUSTOMER
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.comp_code = :COMP_CODE
  AND t.transaction_date BETWEEN :FM_DT AND :TO_DT
  AND t.status = 'ACTIVE'
ORDER BY t.transaction_date DESC

-- Step 2: Register in database  
INSERT INTO RPT_REPORT_MASTER (RPT_ID, RPT_NAME, RPT_TYPE, RPT_SOURCE, RPT_PARAMS)
VALUES ('NEW002', 'Transaction Report', 'SQL', 'NEW002', '{
    "parameters": [
        {"field": "FM_DT", "name": "From Date", "type": "date", "visible": true, "required": true},
        {"field": "TO_DT", "name": "To Date", "type": "date", "visible": true, "required": true}
    ],
    "display_columns": ["TXN_ID", "TXN_DATE", "AMOUNT", "STATUS", "CUSTOMER"],
    "column_headers": {
        "TXN_ID": "Transaction ID",
        "TXN_DATE": "Date", 
        "AMOUNT": "Amount",
        "STATUS": "Status",
        "CUSTOMER": "Customer Name"
    }
}');
```

### 2. Parameter Configuration Patterns

#### Basic Parameters
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
        },
        {
            "field": "status",
            "name": "Status",
            "type": "select",
            "required": false,
            "visible": true,
            "options": [
                {"value": "A", "label": "Active"},
                {"value": "I", "label": "Inactive"},
                {"value": "P", "label": "Pending"}
            ]
        }
    ]
}
```

#### Hidden Parameters (Auto-Applied)
```json
{
    "parameters": [
        {
            "field": "comp_code",
            "name": "Company Code",
            "type": "text",
            "required": true,
            "visible": false,
            "default": "SESSION_COMP_CODE"
        },
        {
            "field": "current_date",
            "name": "Current Date", 
            "type": "date",
            "visible": false,
            "default": "SYSDATE"
        }
    ]
}
```

#### Advanced Parameter Types
```json
{
    "parameters": [
        {
            "field": "amount_range",
            "name": "Amount Range",
            "type": "number",
            "validation": {
                "min": 0,
                "max": 999999.99
            }
        },
        {
            "field": "categories",
            "name": "Categories",
            "type": "multi_select",
            "options": [
                {"value": "CAT1", "label": "Category 1"},
                {"value": "CAT2", "label": "Category 2"}
            ]
        }
    ]
}
```

### 3. Database Access Patterns

#### Basic Query Pattern
```python
from database import get_db_connection

def fetch_data(params):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT col1, col2, col3
            FROM table_name
            WHERE condition = :param1
        """, params)
        return cursor.fetchall()
```

#### CLOB Handling Pattern
```python
def read_clob_data(report_id):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT rpt_params FROM rpt_report_master 
            WHERE rpt_id = :report_id
        """, {'report_id': report_id})
        
        result = cursor.fetchone()
        if result and result[0]:
            # Read CLOB within active connection
            clob_data = result[0].read() if hasattr(result[0], 'read') else str(result[0])
            return json.loads(clob_data)
        return {}
```

#### Transaction Pattern
```python
def update_with_transaction(data):
    with get_db_connection() as connection:
        try:
            cursor = connection.cursor()
            
            # Multiple operations
            cursor.execute("INSERT INTO table1 ...", data)
            cursor.execute("UPDATE table2 SET ...", data)
            
            connection.commit()
            return True
            
        except Exception as e:
            connection.rollback()
            raise e
```

---

## Code Organization Patterns

### 1. Service Layer Pattern
```python
# services/report_service.py
class ReportService:
    @staticmethod
    def generate_report(report_id, params):
        """Centralized report generation logic"""
        config = ReportService.get_config(report_id)
        
        if config['type'] == 'CLASS':
            return ReportService.execute_class_report(config, params)
        elif config['type'] == 'SQL':
            return ReportService.execute_sql_report(config, params)
    
    @staticmethod 
    def get_config(report_id):
        """Get report configuration"""
        # Implementation
        pass
```

### 2. Error Handling Pattern
```python
from functools import wraps
import traceback

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error in {f.__name__}: {str(e)}")
            app.logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': str(e),
                'function': f.__name__
            }), 500
    return decorated_function

@app.route('/api/endpoint')
@handle_errors
def api_endpoint():
    # Your code here
    pass
```

### 3. Validation Pattern
```python
from flask import request, jsonify

def validate_required_fields(required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for field in required_fields:
                if field not in request.form and field not in request.json:
                    return jsonify({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/create-report', methods=['POST'])
@validate_required_fields(['report_id', 'report_name', 'report_type'])
def create_report():
    # Your code here
    pass
```

---

## Testing Patterns

### 1. Unit Test Pattern
```python
# tests/test_reports.py
import unittest
from unittest.mock import patch, MagicMock
from reports.core import get_report_config
from reports.main_routes import build_dynamic_parameters

class TestReports(unittest.TestCase):
    def setUp(self):
        self.sample_config = {
            'id': 'TEST001',
            'type': 'CLASS',
            'params': {
                'parameters': [
                    {'field': 'test_param', 'visible': True, 'default': 'test_value'}
                ]
            }
        }
    
    @patch('reports.core.get_db_connection')
    def test_get_report_config(self, mock_db):
        # Mock database response
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('TEST001', 'Test Report', 'CLASS', '{}')
        mock_db.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        
        config = get_report_config('TEST001')
        self.assertIsNotNone(config)
        self.assertEqual(config['id'], 'TEST001')
    
    def test_build_dynamic_parameters(self):
        form_data = {'user_input': 'test_value'}
        session = {'comp_code': 'TTM', 'user_id': 'ADMIN'}
        
        params = build_dynamic_parameters(form_data, session, self.sample_config)
        
        self.assertIn('comp_code', params)
        self.assertIn('user_id', params)
        self.assertEqual(params['comp_code'], 'TTM')

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Test Pattern  
```python
# tests/test_integration.py
import unittest
import requests
from app import app

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def login(self):
        return self.app.post('/login', data={
            'comp_code': 'TTM',
            'user_id': 'ADMIN', 
            'password': 'admin'
        }, follow_redirects=True)
    
    def test_report_generation_flow(self):
        # Login
        response = self.login()
        self.assertEqual(response.status_code, 200)
        
        # Get report form
        response = self.app.get('/reports/form/FIN001')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'From Date', response.data)
        
        # Generate report
        response = self.app.post('/reports/FIN001/T020101/generate', data={
            'fm_dt': '01/01/2024',
            'to_dt': '31/12/2024',
            'outputFormat': 'view'
        })
        self.assertEqual(response.status_code, 200)
```

---

## Debugging Patterns

### 1. Debug Logging Pattern
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def debug_parameters(params):
    logger.debug(f"Parameters received: {params}")
    for key, value in params.items():
        logger.debug(f"  {key}: {value} (type: {type(value)})")

# Usage in report generation
def generate_report(params):
    debug_parameters(params)
    # ... rest of code
```

### 2. Performance Monitoring Pattern  
```python
import time
from functools import wraps

def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # milliseconds
        app.logger.info(f"{f.__name__} executed in {execution_time:.2f}ms")
        
        return result
    return decorated_function

@monitor_performance
def generate_report(report_id, params):
    # Your report generation code
    pass
```

### 3. Database Query Debugging
```python
def debug_query(query, params):
    """Debug SQL queries with parameter substitution"""
    import re
    
    # Simple parameter substitution for debugging
    debug_query = query
    for param, value in params.items():
        debug_query = re.sub(f':{param}\\b', f"'{value}'", debug_query)
    
    app.logger.debug(f"Executing query: {debug_query}")
    return debug_query
```

---

## Performance Optimization Patterns

### 1. Database Connection Pooling
```python
# database.py - Enhanced with connection pooling
import oracledb
from contextlib import contextmanager

class DatabasePool:
    def __init__(self, min_connections=1, max_connections=10):
        self.pool = oracledb.create_pool(
            user="your_user",
            password="your_password",
            dsn="localhost:1521/XE",
            min=min_connections,
            max=max_connections,
            increment=1
        )
    
    @contextmanager
    def get_connection(self):
        connection = self.pool.acquire()
        try:
            yield connection
        finally:
            self.pool.release(connection)

# Global pool instance
db_pool = DatabasePool()

def get_db_connection():
    return db_pool.get_connection()
```

### 2. Caching Pattern
```python
from functools import lru_cache
import json

# Cache report configurations
@lru_cache(maxsize=128)
def get_cached_report_config(report_id):
    """Cache report configurations to avoid repeated database calls"""
    return get_report_config(report_id)

# Cache with TTL (using external library like redis)
def cache_with_ttl(ttl_seconds=300):
    def decorator(f):
        cache = {}
        timestamps = {}
        
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            if key in cache and (current_time - timestamps[key]) < ttl_seconds:
                return cache[key]
            
            result = f(*args, **kwargs)
            cache[key] = result
            timestamps[key] = current_time
            
            return result
        return wrapper
    return decorator

@cache_with_ttl(300)  # 5 minutes TTL
def get_menu_hierarchy():
    # Expensive database operation
    pass
```

### 3. Async Processing Pattern
```python
import threading
import queue

class ReportQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.results = {}
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()
    
    def _worker(self):
        while True:
            job_id, report_id, params = self.queue.get()
            try:
                result = self._generate_report(report_id, params)
                self.results[job_id] = {'status': 'completed', 'data': result}
            except Exception as e:
                self.results[job_id] = {'status': 'error', 'error': str(e)}
            self.queue.task_done()
    
    def submit_report(self, job_id, report_id, params):
        self.queue.put((job_id, report_id, params))
        self.results[job_id] = {'status': 'pending'}
    
    def get_result(self, job_id):
        return self.results.get(job_id, {'status': 'not_found'})

# Global report queue
report_queue = ReportQueue()
```

---

## Security Patterns

### 1. Input Sanitization
```python
import re
from html import escape

def sanitize_input(value, input_type='text'):
    """Sanitize user input based on type"""
    if value is None:
        return None
    
    value = str(value).strip()
    
    if input_type == 'text':
        # Remove potentially dangerous characters
        value = re.sub(r'[<>&"\']', '', value)
        return escape(value)
    
    elif input_type == 'date':
        # Validate date format
        if re.match(r'^\d{2}/\d{2}/\d{4}$', value):
            return value
        raise ValueError("Invalid date format")
    
    elif input_type == 'number':
        try:
            return float(value)
        except ValueError:
            raise ValueError("Invalid number format")
    
    return value

def sanitize_params(params):
    """Sanitize all parameters"""
    sanitized = {}
    for key, value in params.items():
        sanitized[key] = sanitize_input(value)
    return sanitized
```

### 2. SQL Injection Prevention
```python
def safe_execute_query(query, params):
    """Execute query with parameter binding to prevent SQL injection"""
    # Never use string formatting for SQL queries
    # WRONG: f"SELECT * FROM table WHERE id = {user_id}"
    # RIGHT: Use parameterized queries
    
    with get_db_connection() as connection:
        cursor = connection.cursor()
        # Oracle uses :param_name format
        cursor.execute(query, params)
        return cursor.fetchall()

# Validate parameter names to prevent injection
def validate_param_names(params):
    """Ensure parameter names contain only safe characters"""
    safe_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    
    for param_name in params.keys():
        if not safe_pattern.match(param_name):
            raise ValueError(f"Invalid parameter name: {param_name}")
```

### 3. Session Security
```python
from datetime import datetime, timedelta

def check_session_security(session):
    """Check session validity and security"""
    # Check if session exists
    if 'user_id' not in session:
        return False, "No active session"
    
    # Check session timeout
    last_activity = session.get('last_activity')
    if last_activity:
        last_activity = datetime.fromisoformat(last_activity)
        if datetime.now() - last_activity > timedelta(minutes=30):
            return False, "Session expired"
    
    # Update last activity
    session['last_activity'] = datetime.now().isoformat()
    
    return True, "Session valid"

@app.before_request
def check_session():
    """Check session on every request"""
    if request.endpoint and request.endpoint != 'login':
        is_valid, message = check_session_security(session)
        if not is_valid:
            session.clear()
            return redirect(url_for('login'))
```

---

## Deployment Patterns

### 1. Environment Configuration
```python
# config.py - Environment-specific configurations
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database
    ORACLE_USER = os.environ.get('ORACLE_USER')
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD')
    ORACLE_DSN = os.environ.get('ORACLE_DSN')

class DevelopmentConfig(Config):
    DEBUG = True
    ORACLE_USER = 'dev_user'
    ORACLE_PASSWORD = 'dev_password'
    ORACLE_DSN = 'localhost:1521/XE'

class ProductionConfig(Config):
    DEBUG = False
    ORACLE_USER = os.environ.get('ORACLE_USER')
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD') 
    ORACLE_DSN = os.environ.get('ORACLE_DSN')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

### 2. Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  erp_app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ORACLE_USER=your_user
      - ORACLE_PASSWORD=your_password
      - ORACLE_DSN=oracle:1521/XE
      - SECRET_KEY=your_secret_key
    depends_on:
      - oracle
  
  oracle:
    image: container-registry.oracle.com/database/express:11.2.0.2-xe
    environment:
      - ORACLE_PWD=your_oracle_password
    ports:
      - "1521:1521"
```

This developer guide provides comprehensive patterns and practices for extending and maintaining the ERP application effectively.