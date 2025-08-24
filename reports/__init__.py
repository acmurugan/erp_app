# =============================================================================
# File: reports/__init__.py
# This is the MAIN ENTRY POINT for your modular reports system
# =============================================================================

from .core import reports_bp

def create_reports_blueprint():
    """
    Create and configure the reports blueprint with all sub-modules
    This function replaces your old single reports_bp import
    """
    try:
        print("Loading modular reports system...")
        
        # Import all route modules to register their routes with the blueprint
        # This happens when the modules are imported
        from . import main_routes      # Main report generation routes
        from .admin_routes import admin_bp  # Admin interface routes
        from . import debug_routes     # Debug and test routes
        
        # Register the admin blueprint as a sub-blueprint
        reports_bp.register_blueprint(admin_bp, url_prefix='/admin')
        
        print("Reports modules loaded successfully")
        print("Available modules: main_routes, admin_routes, debug_routes")
        
        return reports_bp
        
    except Exception as e:
        print(f"Error loading reports modules: {e}")
        print("Make sure all required files exist in reports/ folder")
        raise

# Export the function for use in app.py
__all__ = ['create_reports_blueprint', 'reports_bp']

# Optional: For backwards compatibility (if someone tries to import reports_bp directly)
def get_reports_blueprint():
    """Alternative function name for getting the blueprint"""
    return create_reports_blueprint()