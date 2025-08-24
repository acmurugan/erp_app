from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from database import (
    get_db_connection, 
    validate_user_credentials, 
    validate_company_code, 
    validate_branch_code, 
    get_user_menu_count,
    insert_login_detail, 
    update_logout_detail
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Home page - ALWAYS check session properly"""
    print("\n" + "="*50)
    print("INDEX ROUTE CALLED")
    print(f"- Session keys: {list(session.keys()) if session else 'No session'}")
    print(f"User User in session: {'user_id' in session}")
    print(f"Key Session user_id: {session.get('user_id', 'NOT FOUND')}")
    
    # CLEAR CHECK: If no user_id in session, go to login
    if 'user_id' not in session or not session.get('user_id'):
        print("ERROR NO VALID USER SESSION - REDIRECTING TO LOGIN")
        print("="*50)
        return redirect(url_for('auth.login'))
    
    print("OK USER SESSION EXISTS - REDIRECTING TO DASHBOARD")
    print("="*50)
    return redirect(url_for('dashboard.dashboard'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Enhanced login with proper session clearing and login tracking"""
    print("\n" + "="*50)
    print("LOGIN LOGIN ROUTE CALLED")
    print(f"STEP Request method: {request.method}")
    
    # IMPORTANT: Clear any existing session first
    if request.method == 'GET':
        session.clear()
        print("CLEARED Session cleared for fresh login")
    
    if request.method == 'POST':
        print("PROCESSING Processing POST request...")
        print(f"FORM Raw form data: {request.form}")
        print(f"FORM Form keys: {list(request.form.keys())}")
        
        # Get form data
        username = request.form.get('username', '').strip().upper()
        password = request.form.get('password', '').strip()
        company_code = request.form.get('company_code', '').strip().upper()
        branch_code = request.form.get('branch_code', '').strip().upper()
        
        print(f"User Username: {username}")
        print(f"Company Company: {company_code}")
        print(f"Branch Branch: {branch_code}")
        print(f"Key Password provided: {'Yes' if password else 'No'}")
        
        # Validate required fields
        if not username or not password or not company_code:
            print("ERROR Missing required fields")
            flash('Please enter Username, Password, and Company Code', 'danger')
            return render_template('login.html')
        
        try:
            print("DB Connecting to database...")
            
            # Step 1: Validate User
            print("STEP Step 1: Validating user credentials...")
            user_data = validate_user_credentials(username, password)
            
            if not user_data:
                print("ERROR Invalid credentials")
                flash('Invalid username or password', 'danger')
                return render_template('login.html')
            
            print(f"SUCCESS User validated: {user_data['user_desc']}")
            
            # Step 2: Validate Company
            print("STEP Step 2: Validating company...")
            company_name = validate_company_code(company_code)
            
            if not company_name:
                print("ERROR Invalid company")
                flash('Invalid or frozen company code', 'danger')
                return render_template('login.html')
            
            print(f"SUCCESS Company validated: {company_name}")
            
            # Step 3: Validate Branch (if provided)
            location_name = ""
            if branch_code:
                print("STEP Step 3: Validating branch...")
                location_name = validate_branch_code(branch_code, username)
                
                if not location_name:
                    print("ERROR Invalid branch")
                    flash('Invalid branch code for this user', 'danger')
                    return render_template('login.html')
                
                print(f"SUCCESS Branch validated: {location_name}")
            
            # Step 4: Get language setting
            print("STEP Step 4: Getting language setting...")
            lang_code = 'ENG'  # Default language
            try:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT NVL(SUBSTR(P_VALUE,1,3), 'ENG')
                        FROM MENU_PARAMETER
                        WHERE P_ID = 'LANGUAGE'
                    """)
                    result = cursor.fetchone()
                    if result:
                        lang_code = result[0]
                        print(f"SUCCESS Language code set to: {lang_code}")
                    else:
                        print("WARNING No language parameter found, using default: ENG")
            except Exception as e:
                print(f"WARNING Error getting language setting: {e}, using default: ENG")
            
            # Step 5: Count menus
            print("STEP Step 5: Counting user menus...")
            menu_count = get_user_menu_count(username)
            print(f"INFO User has access to {menu_count} menus")
            
            # Step 6: Insert login detail into IM_LOGIN_USER_DETAIL
            print("STEP Step 6: Recording login details...")
            sys_id = insert_login_detail(username, company_code, branch_code, user_data['user_desc'])
            
            if not sys_id:
                print("ERROR Failed to record login details")
                flash('Login recording failed', 'warning')
                # Continue with login even if recording fails
            
            # Clear session and set new values
            session.clear()
            session['user_id'] = username
            session['user_desc'] = user_data['user_desc']
            session['user_group_id'] = user_data['user_group_id']
            session['company_code'] = company_code
            session['company_name'] = company_name
            session['branch_code'] = branch_code
            session['location_name'] = location_name
            session['menu_count'] = menu_count
            session['login_time'] = datetime.now().isoformat()
            session['sys_id'] = sys_id  # Store sys_id for logout tracking
            session['M_LANG_CODE'] = lang_code  # Language code for menu display
            
            print("SUCCESS Session created successfully")
            print(f"- New session keys: {list(session.keys())}")
            print(f"ID Session SYS_ID: {sys_id}")
            
            flash(f'Welcome {user_data["user_desc"]}!', 'success')
            print("REDIRECT Redirecting to dashboard...")
            print("="*50)
            return redirect(url_for('dashboard.dashboard'))
                
        except Exception as e:
            print(f"ERROR Database error: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Login failed: {str(e)}', 'danger')
    
    print("RENDER Rendering login template")
    print("="*50)
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Enhanced logout with complete session cleanup and logout tracking"""
    print("\n" + "="*50)
    print("LOGOUT LOGOUT ROUTE CALLED")
    
    user_name = session.get('user_desc', 'User')
    sys_id = session.get('sys_id')
    
    # Update logout time if sys_id exists
    if sys_id:
        print(f"STEP Updating logout time for SYS_ID: {sys_id}")
        if update_logout_detail(sys_id):
            print("SUCCESS Logout time updated successfully")
        else:
            print("ERROR Failed to update logout time")
    else:
        print("WARNING No SYS_ID found in session - skipping logout update")
    
    # Clear session completely
    session.clear()
    
    print("CLEARED Session cleared completely")
    flash(f'Goodbye {user_name}! You have been logged out successfully', 'info')
    print("="*50)
    return redirect(url_for('auth.login'))

@auth_bp.route('/clear-session')
def clear_session():
    """Emergency route to clear session"""
    session.clear()
    flash('Session cleared successfully', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/toggle-language', methods=['POST'])
def toggle_language():
    """Toggle language between ENG and FOR"""
    print("\n" + "="*50)
    print("LANGUAGE LANGUAGE TOGGLE ROUTE CALLED")
    
    # Check if user is logged in
    if 'user_id' not in session:
        print("ERROR User not logged in")
        return jsonify({'success': False, 'message': 'User not logged in'}), 401
    
    current_lang = session.get('M_LANG_CODE', 'ENG')
    new_lang = 'FOR' if current_lang == 'ENG' else 'ENG'
    
    print(f"TOGGLE Toggling language from {current_lang} to {new_lang}")
    
    # Update session
    session['M_LANG_CODE'] = new_lang
    
    print(f"SUCCESS Language updated to: {new_lang}")
    print("="*50)
    
    return jsonify({
        'success': True, 
        'new_language': new_lang,
        'message': f'Language changed to {new_lang}'
    })

@auth_bp.route('/debug-login', methods=['GET', 'POST'])
def debug_login():
    """Debug route to test login credentials"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip().upper()
        password = request.form.get('password', '').strip()
        company_code = request.form.get('company_code', '').strip().upper()
        
        print(f"DEBUG Testing credentials:")
        print(f"DEBUG Username: '{username}'")
        print(f"DEBUG Company: '{company_code}'")
        print(f"DEBUG Password provided: {'Yes' if password else 'No'}")
        
        # Test user credentials
        user_data = validate_user_credentials(username, password)
        print(f"DEBUG User validation result: {user_data}")
        
        # Test company code
        company_name = validate_company_code(company_code)
        print(f"DEBUG Company validation result: {company_name}")
        
        # Check what users exist in database
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT USER_ID, USER_DESC FROM MENU_USER WHERE ROWNUM <= 10")
                users = cursor.fetchall()
                print(f"DEBUG Sample users in database: {users}")
                
                cursor.execute("SELECT COMP_CODE, COMP_NAME FROM FM_COMPANY WHERE ROWNUM <= 10")
                companies = cursor.fetchall()
                print(f"DEBUG Sample companies in database: {companies}")
                
        except Exception as e:
            print(f"DEBUG Error checking database: {e}")
        
        return f"""
        <html><body>
        <h2>Debug Login Results</h2>
        <p><strong>Username:</strong> {username}</p>
        <p><strong>Company:</strong> {company_code}</p>
        <p><strong>User Valid:</strong> {'YES' if user_data else 'NO'}</p>
        <p><strong>Company Valid:</strong> {'YES' if company_name else 'NO'}</p>
        <p><strong>User Data:</strong> {user_data}</p>
        <p><strong>Company Name:</strong> {company_name}</p>
        <p>Check console output for more details</p>
        <a href="/debug-login">← Try Again</a>
        </body></html>
        """
    
    # GET request - show form
    return '''
    <html><body>
    <h2>Debug Login Test</h2>
    <form method="POST">
        Username: <input name="username" placeholder="ORION"><br><br>
        Password: <input name="password" type="password"><br><br>
        Company: <input name="company_code" placeholder="TTM"><br><br>
        <button type="submit">Test Credentials</button>
    </form>
    <p><a href="/login">← Back to Login</a></p>
    </body></html>
    '''