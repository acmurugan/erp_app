from flask import Blueprint, render_template, redirect, url_for, session, flash
from datetime import datetime  # ADD THIS MISSING IMPORT
from database import get_db_connection
from services.menu_service import get_user_menus, get_report_menus, process_menu_url_filter

dashboard_bp = Blueprint('dashboard', __name__)

# Register the template filter
@dashboard_bp.app_template_filter('process_menu_url')
def process_menu_url_template_filter(menu_url, form_id=None, menu_id=None):
    """Template filter to process menu URLs"""
    return process_menu_url_filter(menu_url, form_id, menu_id)

@dashboard_bp.route('/dashboard')
def dashboard():
    """Enhanced Dashboard with dynamic URL processing"""
    print("\n" + "="*50)
    print("DASHBOARD ENHANCED DASHBOARD ROUTE CALLED")
    print(f"INFO Session keys: {list(session.keys()) if session else 'No session'}")
    print(f"User Session user_id: {session.get('user_id', 'NOT FOUND')}")
    
    # Strict session validation
    if 'user_id' not in session or not session.get('user_id'):
        print("ERROR No valid session - redirecting to login")
        session.clear()  # Clear any partial session
        flash('Please log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    print("SUCCESS Valid session found - loading enhanced dashboard")
    
    # Get user menus with dynamic URL processing
    user_menus = get_user_menus(session['user_id'])
    print(f"INFO Loaded {len(user_menus)} root menus with processed URLs")
    
    # Get report-specific menus
    report_menus = get_report_menus(session['user_id'])
    print(f"DASHBOARD Loaded {len(report_menus)} report menus")
    
    # Get sample tables (your existing code)
    master_tables = []
    transaction_tables = []
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT table_name FROM user_tables WHERE ROWNUM <= 10 ORDER BY table_name")
            available_tables = [row[0] for row in cursor.fetchall()]
            
            for table_name in available_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    
                    table_info = {
                        'name': table_name,
                        'row_count': row_count,
                        'display_name': table_name.replace('_', ' ').title()
                    }
                    
                    if row_count < 5000:
                        master_tables.append(table_info)
                    else:
                        transaction_tables.append(table_info)
                        
                except Exception as e:
                    print(f"WARNING Warning: Could not get count for {table_name}: {e}")
    
    except Exception as e:
        print(f"WARNING Warning: Error getting tables: {e}")
    
    print("RENDER Rendering enhanced dashboard template")
    print("="*50)
    
    return render_template('dashboard.html',
                         master_tables=master_tables,
                         transaction_tables=transaction_tables,
                         user_menus=user_menus,
                         report_menus=report_menus,  # NEW: Add report menus
                         user_name=session.get('user_desc', 'User'),
                         company_name=session.get('company_name', ''),
                         location_name=session.get('location_name', ''))

@dashboard_bp.route('/test-menu-urls')
def test_menu_urls():
    """Test route to verify menu URL processing"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        # Get both hierarchical and report menus for testing
        user_menus = get_user_menus(session['user_id'])
        report_menus = get_report_menus(session['user_id'])
        
        # Flatten hierarchical menus for testing
        def flatten_menus(menus):
            flat_list = []
            for menu in menus:
                flat_list.append(menu)
                if menu.get('children'):
                    flat_list.extend(flatten_menus(menu['children']))
            return flat_list
        
        all_flat_menus = flatten_menus(user_menus)
        
        html_output = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Menu URL Test</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>TEST Menu URL Processing Test</h2>
                
                <div class="alert alert-info">
                    <strong>User:</strong> {session['user_id']} | 
                    <strong>Total Hierarchical Menus:</strong> {len(all_flat_menus)} | 
                    <strong>Report Menus:</strong> {len(report_menus)}
                </div>
                
                <h3>DASHBOARD Report Menus</h3>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Menu ID</th>
                            <th>Menu Name</th>
                            <th>Form ID (Action)</th>
                            <th>Original URL</th>
                            <th>Processed URL</th>
                            <th>Test Link</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add report menus
        for menu in report_menus:
            test_link = f'<a href="{menu["processed_url"]}" class="btn btn-sm btn-outline-primary">Test</a>' if menu.get('processed_url') and menu['processed_url'] != '#' else 'No URL'
            
            html_output += f"""
                        <tr>
                            <td><code>{menu['id']}</code></td>
                            <td>{menu['name']}</td>
                            <td><code>{menu.get('form_id', 'N/A')}</code></td>
                            <td><code>{menu.get('button_1', 'N/A')}</code></td>
                            <td><code>{menu.get('processed_url', 'N/A')}</code></td>
                            <td>{test_link}</td>
                        </tr>
            """
        
        html_output += """
                    </tbody>
                </table>
                
                <h3>🏗️ All Menus with URLs</h3>
                <table class="table table-striped table-sm">
                    <thead>
                        <tr>
                            <th>Menu ID</th>
                            <th>Name</th>
                            <th>Type</th>
                            <th>Original URL</th>
                            <th>Processed URL</th>
                            <th>Test</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add all menus that have URLs
        for menu in all_flat_menus:
            if menu.get('button_1'):
                test_link = f'<a href="{menu["processed_url"]}" class="btn btn-sm btn-outline-success">Test</a>' if menu.get('processed_url') and menu['processed_url'] != '#' else 'No URL'
                
                html_output += f"""
                        <tr>
                            <td><code>{menu['id']}</code></td>
                            <td>{menu['name']}</td>
                            <td><span class="badge bg-secondary">{menu.get('action_type', 'N/A')}</span></td>
                            <td><code>{menu.get('button_1', 'N/A')}</code></td>
                            <td><code>{menu.get('processed_url', 'N/A')}</code></td>
                            <td>{test_link}</td>
                        </tr>
                """
        
        html_output += """
                    </tbody>
                </table>
                
                <div class="mt-4">
                    <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
                    <a href="/reports/admin/modular" class="btn btn-outline-warning">DASHBOARD Reports Admin</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_output
        
    except Exception as e:
        import traceback
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Error</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>❌ Error testing menu URLs</h2>
                <div class="alert alert-danger">
                    <strong>Error:</strong> {str(e)}
                </div>
                <pre class="bg-light p-3">{traceback.format_exc()}</pre>
                <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        """

@dashboard_bp.route('/debug-menus')
def debug_menus():
    """Debug route to show detailed menu information"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        from services.menu_service import debug_user_menus
        
        # Capture debug output
        import io
        import sys
        from contextlib import redirect_stdout
        
        debug_output = io.StringIO()
        with redirect_stdout(debug_output):
            debug_user_menus(session['user_id'])
        
        debug_text = debug_output.getvalue()
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Debug Menu Output</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>🐛 Debug Menu Output</h2>
                <pre class="bg-light p-3" style="max-height: 600px; overflow-y: auto;">{debug_text}</pre>
                <div class="mt-3">
                    <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
                    <a href="/dashboard/test-menu-urls" class="btn btn-outline-info">TEST Test URLs</a>
                </div>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"<h2>Debug Error: {str(e)}</h2>"

@dashboard_bp.route('/test-url-processing')
def test_url_processing():
    """Test URL processing logic - FIXED VERSION"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        from services.menu_service import process_menu_url
        
        # Test basic URL processing
        test_menu = {
            'id': 'T010509',
            'button_1': '/reports/:form_id/:id',
            'form_id': 'TTL201',
            'action': 'TTL201'
        }
        
        processed_url = process_menu_url(test_menu)
        expected_url = '/reports/TTL201/T010509'
        
        # Test with actual user menus
        report_menus = get_report_menus(session['user_id'])
        
        # Find T010509 menu specifically
        t010509_menu = None
        for menu in report_menus:
            if menu['id'] == 'T010509':
                t010509_menu = menu
                break
        
        # Start building HTML response
        return_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>URL Processing Test</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>TEST URL Processing Test Results</h2>
                
                <div class="alert alert-info">
                    <strong>User:</strong> {session.get('user_id')} | 
                    <strong>Report Menus Found:</strong> {len(report_menus)}
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5>CONFIG Basic Test</h5>
                            </div>
                            <div class="card-body">
                                <p><strong>Test Menu ID:</strong> T010509</p>
                                <p><strong>Original URL:</strong> <code>{test_menu['button_1']}</code></p>
                                <p><strong>Form ID:</strong> <code>{test_menu['form_id']}</code></p>
                                <p><strong>Processed URL:</strong> <code>{processed_url}</code></p>
                                <p><strong>Expected URL:</strong> <code>{expected_url}</code></p>
                                <div class="alert {'alert-success' if processed_url == expected_url else 'alert-danger'}">
                                    <strong>Result:</strong> {'SUCCESS PASS' if processed_url == expected_url else '❌ FAIL'}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5>DASHBOARD T010509 Menu Check</h5>
                            </div>
                            <div class="card-body">
        """
        
        if t010509_menu:
            return_html += f"""
                                <p><strong>T010509 Found:</strong> SUCCESS YES</p>
                                <p><strong>Original URL:</strong> <code>{t010509_menu['button_1']}</code></p>
                                <p><strong>Form ID:</strong> <code>{t010509_menu['form_id']}</code></p>
                                <p><strong>Processed URL:</strong> <code>{t010509_menu['processed_url']}</code></p>
                                <div class="alert {'alert-success' if t010509_menu['processed_url'] == expected_url else 'alert-danger'}">
                                    <strong>Actual Result:</strong> {'SUCCESS PASS' if t010509_menu['processed_url'] == expected_url else '❌ FAIL'}
                                </div>
            """
        else:
            return_html += """
                                <p><strong>T010509 Found:</strong> ❌ NO</p>
                                <p class="text-muted">Menu T010509 not found in user report menus</p>
            """
        
        return_html += """
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="mt-4">
                    <h3>INFO All Report Menus</h3>
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Menu ID</th>
                                <th>Name</th>
                                <th>Form ID</th>
                                <th>Original URL</th>
                                <th>Processed URL</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        for menu in report_menus:
            status = "SUCCESS Processed" if menu.get('processed_url') != menu.get('button_1') else "WARNING️ No Change"
            if not menu.get('button_1'):
                status = "❌ No URL"
            
            return_html += f"""
                            <tr>
                                <td><code>{menu['id']}</code></td>
                                <td>{menu['name']}</td>
                                <td><code>{menu.get('form_id', 'N/A')}</code></td>
                                <td><code>{menu.get('button_1', 'N/A')}</code></td>
                                <td><code>{menu.get('processed_url', 'N/A')}</code></td>
                                <td>{status}</td>
                            </tr>
            """
        
        return_html += """
                        </tbody>
                    </table>
                </div>
                
                <div class="mt-4">
                    <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
                    <a href="/dashboard/debug-menus" class="btn btn-outline-info">🐛 Debug Menus</a>
                    <a href="/reports/admin/modular" class="btn btn-outline-warning">DASHBOARD Reports Admin</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return return_html
        
    except Exception as e:
        import traceback
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Error</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>❌ Test Error</h2>
                <div class="alert alert-danger">
                    <strong>Error:</strong> {str(e)}
                </div>
                <pre class="bg-light p-3">{traceback.format_exc()}</pre>
                <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        """

@dashboard_bp.route('/check-menu-database')
def check_menu_database():
    """Check the database configuration for T010509"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check T010509 menu configuration
            cursor.execute("""
                SELECT MENU_ID, MENU_ACTION, MENU_BUTTON_1, MENU_SCR_NAME
                FROM MENU_MENUS 
                WHERE MENU_ID = 'T010509'
            """)
            
            menu_config = cursor.fetchone()
            
            # Check user access to this menu
            cursor.execute("""
                SELECT COUNT(*) as has_access
                FROM MENU_USER mu 
                JOIN MENU_USER_MENUS umm ON mu.USER_GROUP_ID = umm.UM_GROUP_ID
                JOIN MENU_MENUS mm ON mm.MENU_ID = umm.UM_MENU_ID
                WHERE mu.USER_ID = :1 AND mm.MENU_ID = 'T010509'
            """, [session['user_id']])
            
            user_access = cursor.fetchone()
            
            # Build HTML response
            html_response = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Menu Database Check</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-4">
                    <h2>CHECK Menu Database Configuration Check</h2>
                    
                    <div class="alert alert-info">
                        <strong>Checking menu T010509 for user:</strong> {session.get('user_id')}
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">
                                    <h5>INFO Menu Configuration</h5>
                                </div>
                                <div class="card-body">
            """
            
            if menu_config:
                menu_id, menu_action, menu_button_1, menu_name = menu_config
                has_form_id_placeholder = ':form_id' in str(menu_button_1) if menu_button_1 else False
                has_id_placeholder = ':id' in str(menu_button_1) if menu_button_1 else False
                has_form_id = bool(menu_action)
                
                html_response += f"""
                                    <p><strong>Menu ID:</strong> {menu_id}</p>
                                    <p><strong>Menu Action (Form ID):</strong> <code>{menu_action or 'None'}</code></p>
                                    <p><strong>Menu Button 1 (URL):</strong> <code>{menu_button_1 or 'None'}</code></p>
                                    <p><strong>Menu Name:</strong> {menu_name or 'None'}</p>
                                    
                                    <hr>
                                    <h6>Analysis:</h6>
                                    <ul>
                                        <li><strong>Has :form_id placeholder:</strong> {'SUCCESS YES' if has_form_id_placeholder else '❌ NO'}</li>
                                        <li><strong>Has :id placeholder:</strong> {'SUCCESS YES' if has_id_placeholder else '❌ NO'}</li>
                                        <li><strong>Form ID available:</strong> {'SUCCESS YES' if has_form_id else '❌ NO'}</li>
                                    </ul>
                                    
                                    <div class="alert {'alert-success' if has_form_id_placeholder and has_form_id else 'alert-warning'}">
                                        <strong>Configuration Status:</strong> 
                                        {'SUCCESS Ready for dynamic processing' if has_form_id_placeholder and has_form_id else 'WARNING️ Needs configuration update'}
                                    </div>
                """
            else:
                html_response += '<p class="text-danger">❌ Menu T010509 not found in database</p>'
            
            html_response += """
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">
                                    <h5>User User Access</h5>
                                </div>
                                <div class="card-body">
            """
            
            if user_access:
                html_response += f"""
                                    <p><strong>User has access to T010509:</strong> 
                                    {'SUCCESS YES' if user_access[0] > 0 else '❌ NO'}</p>
                                    <p><strong>Access count:</strong> {user_access[0]}</p>
                """
            
            if menu_config and menu_config[1]:  # menu_action exists
                html_response += f"""
                                    <div class="mt-3">
                                        <h6>Expected Processing Result:</h6>
                                        <p><strong>Should process to:</strong><br>
                                        <code>/reports/{menu_config[1]}/T010509</code></p>
                                    </div>
                """
            else:
                html_response += '<p class="text-muted">Cannot determine expected result</p>'
            
            html_response += """
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <h3>CONFIG Quick Fix Commands</h3>
                        <div class="card">
                            <div class="card-body">
            """
            
            if menu_config:
                form_id = menu_config[1] if menu_config[1] else 'TTL201'
                html_response += f"""
                                <p>If the configuration is incorrect, run this SQL:</p>
                                <pre class="bg-light p-3">
-- Update T010509 to use dynamic URL pattern
UPDATE MENU_MENUS 
SET MENU_BUTTON_1 = '/reports/:form_id/:id'
WHERE MENU_ID = 'T010509' 
  AND MENU_ACTION = '{form_id}';

-- Verify the update
SELECT MENU_ID, MENU_ACTION, MENU_BUTTON_1 
FROM MENU_MENUS 
WHERE MENU_ID = 'T010509';
                                </pre>
                """
            else:
                html_response += '<p class="text-danger">Menu T010509 not found. Please check if the menu exists in MENU_MENUS table.</p>'
            
            html_response += """
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
                        <a href="/dashboard/test-url-processing" class="btn btn-outline-primary">TEST Test URL Processing</a>
                        <a href="/dashboard/debug-menus" class="btn btn-outline-info">🐛 Debug Menus</a>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return html_response
            
    except Exception as e:
        import traceback
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Database Check Error</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2>❌ Database Check Error</h2>
                <div class="alert alert-danger">
                    <strong>Error:</strong> {str(e)}
                </div>
                <pre class="bg-light p-3">{traceback.format_exc()}</pre>
                <a href="/dashboard" class="btn btn-secondary">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        """

@dashboard_bp.route('/simple-test')
def simple_test():
    """Simple test to verify dashboard routes work"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Test</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-4">
            <h2>SUCCESS Simple Test Working</h2>
            <div class="alert alert-success">
                Dashboard blueprint is working correctly!
            </div>
            <p><strong>Session User:</strong> {session.get('user_id', 'Not logged in')}</p>
            <p><strong>Time:</strong> {datetime.now()}</p>
            
            <div class="mt-3">
                <h4>Available Test Routes:</h4>
                <ul class="list-group">
                    <li class="list-group-item">
                        <a href="/dashboard/check-menu-database">Check Menu Database</a> - Database configuration check
                    </li>
                    <li class="list-group-item">
                        <a href="/dashboard/test-url-processing">Test URL Processing</a> - URL processing test
                    </li>
                    <li class="list-group-item">
                        <a href="/dashboard/test-menu-urls">Test Menu URLs</a> - Menu URL testing
                    </li>
                    <li class="list-group-item">
                        <a href="/dashboard/debug-menus">Debug Menus</a> - Menu debugging
                    </li>
                    <li class="list-group-item">
                        <a href="/reports/admin/modular">Reports Admin</a> - Reports management
                    </li>
                    <li class="list-group-item">
                        <a href="/reports/debug/admin-test">Reports Debug</a> - Reports testing
                    </li>
                </ul>
            </div>
            
            <div class="mt-4">
                <a href="/dashboard" class="btn btn-primary">← Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """