# ERP Application

A Flask-based ERP application with comprehensive reporting system and Oracle database integration.

## Quick Start

### Prerequisites
- Python 3.12+
- Oracle Database (11g XE or higher)
- Oracle Instant Client

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd erp_app

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

The application will be available at `http://localhost:5000`

### Windows Users
You can also use the batch file:
```bash
start_erp.bat
```

## Features

- **Multi-Company Authentication**: Support for multiple company codes and branch locations
- **Dynamic Reports System**: SQL, Class, and Procedure-based reports with flexible parameter handling
- **Admin Interface**: Web-based configuration for reports and parameters
- **Export Options**: Excel, PDF, and web view formats
- **Session Management**: Complete login/logout tracking with audit trail

## Login
- **Company Code**: Your company identifier (e.g., TTM)
- **User ID**: Your username
- **Password**: Your password  
- **Branch Code**: Optional branch/location code

## Project Structure

- `app.py` - Main application entry point
- `reports/` - Modular reports system
- `routes/` - Application routes (auth, dashboard, tables, api)
- `services/` - Business logic services
- `templates/` - HTML templates
- `static/` - Static assets

## Documentation

See `CLAUDE.md` for detailed development guidance and architecture information.

## Debug Endpoints

- `/clear-session` - Emergency session cleanup
- `/dashboard/simple-test` - Test dashboard functionality
- `/reports/admin/` - Reports administration interface