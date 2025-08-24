# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Start the Flask development server
python app.py

# Alternative Windows batch file
start_erp.bat
```
The application runs on `http://localhost:5000` with debug mode enabled.

### Testing and Debugging
```bash
# Run specific test files in tests/ directory
python tests/test_ttl202.py
python tests/test_parameter_visibility.py

# Access debug endpoints for testing
# http://localhost:5000/debug/test-parameter-visibility/TTL715
# http://localhost:5000/reports/debug/admin-test
# http://localhost:5000/dashboard/simple-test
```

### Database Operations
The application connects to Oracle Database using the oracledb library. Connection parameters are configured in `config.py`:
- Default: localhost/XE with user MOZ/MOZ
- Oracle client path: `C:\instantclientOrcl\instantclient_19_28`

## Architecture Overview

### Core Application Structure
- **Flask Application**: Main entry point in `app.py` with modular blueprint registration
- **Database Layer**: Oracle database connectivity through `database.py` with comprehensive user authentication and session management
- **Configuration**: Environment-based configuration in `config.py`
- **Utilities**: Common functions in `utils.py` for validation, formatting, and security

### Authentication & Session Management
The application implements a comprehensive multi-company login system:
- **User Validation**: Against `MENU_USER` table with password verification
- **Company Validation**: Against `FM_COMPANY` table 
- **Branch/Location Validation**: Against `OM_LOCATION` and `OM_LOCATION_USER` tables
- **Session Tracking**: Login/logout details stored in `IM_LOGIN_USER_DETAIL` table
- **Menu Authorization**: User access determined through `MENU_USER_MENUS` relationships

### Reports System Architecture
The reports system is the core feature, implemented as a modular architecture:

#### Blueprint Structure
- **Core Blueprint**: `reports/core.py` - Main blueprint and configuration management
- **Main Routes**: `reports/main_routes.py` - Report generation and parameter handling
- **Admin Routes**: `reports/admin_routes.py` - Administrative interface for report configuration
- **Debug Routes**: `reports/debug_routes.py` - Development and testing utilities

#### Report Execution Models
1. **SQL Reports**: Direct SQL execution via `sql_executor.py`
2. **Class Reports**: Python class-based reports via `class_executor.py` 
3. **Procedure Reports**: Oracle stored procedure execution via `procedure_executor.py`

#### Report Configuration System
Reports are configured through the `RPT_REPORT_MASTER` table with:
- **RPT_PARAMS**: CLOB field containing JSON parameter definitions with multiple format support
- **Parameter Visibility**: Dynamic show/hide functionality for form parameters
- **Column Configuration**: Flexible display column management
- **Export Formats**: Support for Excel, PDF, and web view outputs

#### Parameter Handling Architecture
The system supports multiple parameter format styles:
- **FIELD_NAME_FORMAT**: `{"name": "Display Name", "field": "field_name", "type": "range"}`
- **NAME_LABEL_FORMAT**: `{"name": "field_name", "label": "Display Name", "type": "TEXT"}`
- **Legacy formats**: Various historical parameter configurations

Parameters support:
- **Visibility Control**: Parameters can be hidden from forms while still passing default values
- **Type Validation**: DATE, TEXT, NUMBER, SELECT parameter types
- **Dynamic Form Generation**: Automatic form creation based on parameter configuration

### Service Layer
- **Menu Service**: `services/menu_service.py` - Hierarchical menu management
- **Report Service**: `services/report_service.py` - Report execution coordination  
- **Dynamic Report Service**: `services/dynamic_report_service.py` - Runtime report generation

### Routes Organization
- **Authentication**: `routes/auth.py` - Login/logout functionality
- **Dashboard**: `routes/dashboard.py` - Main application dashboard
- **Tables**: `routes/tables.py` - Database table viewing utilities
- **API**: `routes/api.py` - REST API endpoints

## Important Implementation Details

### Database Connection Management
Always use `get_db_connection()` context manager for database operations. The connection automatically handles Oracle client initialization and proper cleanup.

### CLOB Handling
When working with RPT_PARAMS or other CLOB fields, always read the content within the active database connection:
```python
if hasattr(clob_field, 'read'):
    content = clob_field.read()  # Must be within connection context
```

### Parameter Processing
Hidden parameters (visible: false) are automatically filtered from forms but still included in report execution with their default values. This is handled in the `build_dynamic_parameters()` function.

### Report Class Structure
Report classes in `reports/classes/` follow a standard pattern:
- Inherit from base functionality
- Implement parameter processing
- Handle SQL generation and execution
- Support multiple output formats

### Security Considerations
- SQL injection prevention through parameterized queries
- Input sanitization in `utils.py`
- Session-based authentication with proper cleanup
- File upload restrictions and validation

## Debugging and Development

### Debug Endpoints Available
- `/debug/test-parameter-visibility/{report_id}` - Test parameter filtering
- `/reports/debug/admin-test` - Test admin interface functionality  
- `/dashboard/check-menu-database` - Verify menu database structure
- `/clear-session` - Emergency session cleanup

### Common Development Tasks
When modifying reports:
1. Update `RPT_REPORT_MASTER` table for configuration changes
2. Test parameter visibility using debug endpoints
3. Verify CLOB reading within database connections
4. Test all supported parameter formats

When adding new report types:
1. Create appropriate executor in `reports/` directory
2. Register in `core.py` execution dispatcher
3. Add templates in `templates/reports/`
4. Update export handlers if needed

### Project Organization
- **Production Code**: Main application directories (`routes/`, `reports/`, `services/`)
- **Debug Tools**: `debug_tools/` - Development utilities and test scripts
- **Historical Fixes**: `fixes/` - SQL scripts and patches from development
- **Tests**: `tests/` - Test files for validation
- **Templates**: Template files in appropriate subdirectories