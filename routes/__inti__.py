# =============================================================================
# 1. reports/__init__.py - Main Blueprint Registration
# =============================================================================

from flask import Blueprint
from .core import reports_bp
from . import admin_routes, debug_routes

# Register all sub-modules
def create_reports_blueprint():
    """Create and configure the reports blueprint with all sub-modules"""
    return reports_bp