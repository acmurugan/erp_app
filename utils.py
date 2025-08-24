import os

def ensure_directories():
    """Ensure necessary directories exist"""
    directories = [
        'templates/reports',
        'static/css',
        'static/js', 
        'static/images',
        'routes',
        'services'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def format_number(value):
    """Format numbers with commas"""
    try:
        if isinstance(value, (int, float)):
            return "{:,}".format(int(value) if value % 1 == 0 else value)
        return value
    except:
        return value

def safe_get_form_value(request, field_name, default_value=""):
    """Safely get form values with default"""
    try:
        return request.form.get(field_name, default_value).strip().upper()
    except:
        return default_value

def clean_filename(filename):
    """Clean filename for safe file operations"""
    import re
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and convert to lowercase
    filename = re.sub(r'\s+', '_', filename.strip())
    return filename

def validate_date_format(date_string, format_string='%d/%m/%Y'):
    """Validate date format"""
    try:
        from datetime import datetime
        datetime.strptime(date_string, format_string)
        return True
    except ValueError:
        return False

def get_current_timestamp():
    """Get current timestamp in standard format"""
    from datetime import datetime
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

def log_user_action(user_id, action, details=""):
    """Log user actions for audit trail"""
    try:
        timestamp = get_current_timestamp()
        log_message = f"[{timestamp}] User: {user_id} | Action: {action} | Details: {details}"
        print(log_message)
        # You can extend this to write to a log file if needed
        return True
    except Exception as e:
        print(f"Error logging user action: {e}")
        return False

def generate_session_id():
    """Generate a unique session identifier"""
    import uuid
    return str(uuid.uuid4())

def validate_file_extension(filename, allowed_extensions):
    """Validate file extension"""
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def is_valid_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def truncate_string(text, max_length, suffix="..."):
    """Truncate string to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-len(suffix)] + suffix

def get_client_ip(request):
    """Get client IP address from request"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def sanitize_sql_input(input_string):
    """Basic SQL injection prevention"""
    if not input_string:
        return ""
    # Remove dangerous characters
    dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
    cleaned = str(input_string)
    for char in dangerous_chars:
        cleaned = cleaned.replace(char, "")
    return cleaned.strip()

def create_backup_filename(original_name):
    """Create backup filename with timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(original_name)
    return f"{name}_backup_{timestamp}{ext}"