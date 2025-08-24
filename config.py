import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or "your_secret_key_change_this_in_production"
    
    # Database configuration
    DB_USER = os.environ.get('DB_USER') or "MOZ"
    DB_PASS = os.environ.get('DB_PASS') or "MOZ"
    DB_DSN = os.environ.get('DB_DSN') or "localhost/XE"
    ORACLE_CLIENT_PATH = os.environ.get('ORACLE_CLIENT_PATH') or r"C:\instantclientOrcl\instantclient_19_28"
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size