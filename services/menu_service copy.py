from database import get_db_connection
from flask import session

def process_menu_url(menu_item):
    """
    Enhanced: Process menu URL by replacing dynamic placeholders with better debugging
    """
    try:
        # Get URL from button_1
        menu_url = menu_item.get('button_1', '')
        menu_id = str(menu_item.get('id', ''))
        form_id = str(menu_item.get('form_id', '')) or str(menu_item.get('action', ''))
        
        if not menu_url:
            return '#'
        
        # Debug original values (only for menus with placeholders)
        if ':' in menu_url:
            print(f"DEBUG Processing URL for menu {menu_id}: {menu_url}")
        
        # Replace dynamic placeholders
        processed_url = menu_url
        
        # Replace placeholders efficiently
        if ':id' in processed_url and menu_id:
            processed_url = processed_url.replace(':id', menu_id)
        
        if ':form_id' in processed_url and form_id:
            processed_url = processed_url.replace(':form_id', form_id)
        
        return processed_url
        
    except Exception as e:
        print(f"FAIL Error processing menu URL: {e}")
        return menu_item.get('button_1', '#')

def process_menu_hierarchy(menu_results):
    """Enhanced: Process flat menu list into hierarchical structure with dynamic URL processing"""
    print(f"INFO Processing {len(menu_results)} menu results...")
    
    if not menu_results:
        print("WARNING No menu results to process")
        return []
    
    menu_dict = {}
    
    # First pass: create menu dictionary with all menus
    for menu_data in menu_results:
        # Handle different tuple lengths (6 or 7 elements)
        if len(menu_data) == 7:
            menu_id, parent_id, action_type, scr_name, seq_no, button_1, menu_action = menu_data
        else:
            # Fallback for 6-element tuples
            menu_id, parent_id, action_type, scr_name, seq_no, button_1 = menu_data
            menu_action = None
        
        menu_item = {
            'id': menu_id,
            'parent_id': parent_id,
            'name': scr_name,
            'action_type': action_type,
            'seq_no': seq_no or 999,
            'button_1': button_1,
            'form_id': menu_action,  # Store form_id from MENU_ACTION
            'action': menu_action,   # Also store as 'action' for compatibility
            'children': []
        }
        
        # Process dynamic URLs (simplified for performance)
        if button_1:
            menu_item['processed_url'] = process_menu_url(menu_item)
        else:
            menu_item['processed_url'] = '#'
        
        menu_dict[menu_id] = menu_item
    
    # Second pass: build hierarchy by linking children to parents
    root_menus = []
    orphaned_menus = []
    
    for menu in menu_dict.values():
        if menu['parent_id'] == '*' or menu['parent_id'] is None:
            # This is a root menu
            root_menus.append(menu)
            print(f"   Root menu: {menu['id']} - {menu['name']}")
        else:
            # This is a child menu, find its parent
            parent = menu_dict.get(menu['parent_id'])
            if parent:
                parent['children'].append(menu)
                print(f"   Child menu: {menu['id']} - {menu['name']} added to parent {menu['parent_id']}")
            else:
                # Parent not found, this could be an orphaned menu
                orphaned_menus.append(menu)
                print(f"   WARNING Orphaned menu: {menu['id']} - {menu['name']} (Parent {menu['parent_id']} not found)")
    
    # Third pass: try to resolve orphaned menus (in case parent comes later)
    max_attempts = 5
    attempt = 0
    while orphaned_menus and attempt < max_attempts:
        attempt += 1
        print(f"   Attempt {attempt} to resolve {len(orphaned_menus)} orphaned menus...")
        
        resolved = []
        for menu in orphaned_menus:
            parent = menu_dict.get(menu['parent_id'])
            if parent:
                parent['children'].append(menu)
                resolved.append(menu)
                print(f"   Resolved: {menu['id']} - {menu['name']} added to parent {menu['parent_id']}")
        
        # Remove resolved menus from orphaned list
        for resolved_menu in resolved:
            orphaned_menus.remove(resolved_menu)
    
    # Report final orphaned menus
    if orphaned_menus:
        print(f"   WARNING Final orphaned menus: {len(orphaned_menus)}")
        for menu in orphaned_menus:
            print(f"     - {menu['id']} - {menu['name']} (Parent: {menu['parent_id']})")
            # Add orphaned functional menus to root level if they have actions
            if menu['action_type'] in ['R', 'F', 'U', 'Q'] and menu['button_1']:
                root_menus.append(menu)
                print(f"     Added orphaned functional menu to root: {menu['id']}")
    
    # Recursive function to sort menus by sequence number
    def sort_menus(menu_list):
        menu_list.sort(key=lambda x: (x['seq_no'], x['name']))
        for menu in menu_list:
            if menu['children']:
                sort_menus(menu['children'])
    
    # Sort all menus
    sort_menus(root_menus)
    
    # Print final hierarchy for debugging
    def print_hierarchy(menus, level=0):
        for menu in menus:
            indent = "  " * level
            url_info = f" -> {menu['processed_url']}" if menu['processed_url'] != '#' else ""
            print(f"{indent}- {menu['id']}: {menu['name']} ({menu['action_type']}) [{len(menu['children'])} children]{url_info}")
            if menu['children']:
                print_hierarchy(menu['children'], level + 1)
    
    print(f"\nINFO Final menu hierarchy:")
    print_hierarchy(root_menus)
    
    print(f"SUCCESS Menu processing complete: {len(root_menus)} root menus")
    return root_menus

def get_user_menus(username):
    """Enhanced: Get complete user menu hierarchy with dynamic URL processing"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get language code from session, default to 'ENG'
            lang_code = session.get('M_LANG_CODE', 'ENG')
            print(f"LANG Using language code: {lang_code}")
            
            # Enhanced query to include MENU_ACTION for form_id with language support
            menu_scr_select = f"INITCAP(DECODE('{lang_code}', 'ENG', mm.MENU_SCR_NAME, mm.MENU_SCR_NAME_BL)) AS MENU_SCR_NAME"
            menus_query = f"""
                   SELECT mm.MENU_ID, mm.MENU_PARENT_ID, mm.MENU_ACTION_TYPE, 
                       {menu_scr_select}, 
                       mm.MENU_DISP_SEQ_NO, mm.MENU_BUTTON_1, mm.MENU_ACTION
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND mm.MENU_PARENT_ID = '*'
          AND mu.USER_ID = :1
        UNION
        SELECT mm.MENU_ID, mm.MENU_PARENT_ID, mm.MENU_ACTION_TYPE, 
                       {menu_scr_select}, 
                       mm.MENU_DISP_SEQ_NO, mm.MENU_BUTTON_1, mm.MENU_ACTION
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND mm.MENU_PARENT_ID IN (
            SELECT MENU_ID
            FROM MENU_USER mu2, MENU_MENUS mm2, MENU_USER_MENUS umm2
            WHERE mu2.USER_GROUP_ID = umm2.UM_GROUP_ID
              AND mm2.MENU_ID = umm2.UM_MENU_ID
              AND mm2.MENU_PARENT_ID = '*'
              AND mu2.USER_ID = :1
          )
          AND mu.USER_ID = :1
        UNION
        SELECT mm.MENU_ID, mm.MENU_PARENT_ID, mm.MENU_ACTION_TYPE, 
                       {menu_scr_select}, 
                       mm.MENU_DISP_SEQ_NO, mm.MENU_BUTTON_1, mm.MENU_ACTION
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND mm.MENU_PARENT_ID IN (
            SELECT MENU_ID
            FROM MENU_USER mu3, MENU_MENUS mm3, MENU_USER_MENUS umm3
            WHERE mu3.USER_GROUP_ID = umm3.UM_GROUP_ID
              AND mm3.MENU_ID = umm3.UM_MENU_ID
              AND mm3.MENU_PARENT_ID IN (
                SELECT MENU_ID
                FROM MENU_USER mu4, MENU_MENUS mm4, MENU_USER_MENUS umm4
                WHERE mu4.USER_GROUP_ID = umm4.UM_GROUP_ID
                  AND mm4.MENU_ID = umm4.UM_MENU_ID
                  AND mm4.MENU_PARENT_ID = '*'
                  AND mu4.USER_ID = :1
              )
              AND mu3.USER_ID = :1
          )
          AND mu.USER_ID = :1
        UNION
        SELECT mm.MENU_ID, mm.MENU_PARENT_ID, mm.MENU_ACTION_TYPE, 
                       {menu_scr_select}, 
                       mm.MENU_DISP_SEQ_NO, mm.MENU_BUTTON_1, mm.MENU_ACTION
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND mm.MENU_PARENT_ID IN (
            SELECT MENU_ID
            FROM MENU_USER mu5, MENU_MENUS mm5, MENU_USER_MENUS umm5
            WHERE mu5.USER_GROUP_ID = umm5.UM_GROUP_ID
              AND mm5.MENU_ID = umm5.UM_MENU_ID
              AND mm5.MENU_PARENT_ID IN (
                SELECT MENU_ID
                FROM MENU_USER mu6, MENU_MENUS mm6, MENU_USER_MENUS umm6
                WHERE mu6.USER_GROUP_ID = umm6.UM_GROUP_ID
                  AND mm6.MENU_ID = umm6.UM_MENU_ID
                  AND mm6.MENU_PARENT_ID IN (
                    SELECT MENU_ID
                    FROM MENU_USER mu7, MENU_MENUS mm7, MENU_USER_MENUS umm7
                    WHERE mu7.USER_GROUP_ID = umm7.UM_GROUP_ID
                      AND mm7.MENU_ID = umm7.UM_MENU_ID
                      AND mm7.MENU_PARENT_ID = '*'
                      AND mu7.USER_ID = :1
                  )
                  AND mu6.USER_ID = :1
              )
              AND mu5.USER_ID = :1
          )
          AND mu.USER_ID = :1
          ORDER BY MENU_DISP_SEQ_NO
          """
            
            print(f"STEP Fetching menus for user: {username}")
            cursor.execute(menus_query, [username])
            menu_results = cursor.fetchall()
            
            print(f"SUCCESS Found {len(menu_results)} total menus")
            
            if not menu_results:
                return []
            
            # Process into hierarchy with dynamic URL processing
            hierarchical_menus = process_menu_hierarchy(menu_results)
            return hierarchical_menus
            
    except Exception as e:
        print(f"ERROR Error getting user menus: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_report_menus(username):
    """Enhanced: Get specifically report-related menus for the user with better processing"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get language code from session, default to 'ENG'
            lang_code = session.get('M_LANG_CODE', 'ENG')
            
            # Get report menus specifically with language support
            report_menu_scr_select = f"INITCAP(DECODE('{lang_code}', 'ENG', mm.MENU_SCR_NAME, mm.MENU_SCR_NAME_BL)) AS MENU_SCR_NAME"
            report_menus_query = f"""
                    SELECT mm.MENU_ID, {report_menu_scr_select}, mm.MENU_OPTION_DESC,
                       mm.MENU_BUTTON_1, mm.MENU_ACTION, mm.MENU_DISP_SEQ_NO 
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND (mm.MENU_BUTTON_1 LIKE '/reports/%' OR mm.MENU_ACTION_TYPE = 'R')
          AND mm.MENU_PARENT_ID = '*'
          AND mu.USER_ID = :1
        UNION
        SELECT mm.MENU_ID, {report_menu_scr_select}, mm.MENU_OPTION_DESC,
                       mm.MENU_BUTTON_1, mm.MENU_ACTION, mm.MENU_DISP_SEQ_NO 
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND (mm.MENU_BUTTON_1 LIKE '/reports/%' OR mm.MENU_ACTION_TYPE = 'R')
          AND mm.MENU_PARENT_ID IN (
            SELECT MENU_ID
            FROM MENU_USER mu2, MENU_MENUS mm2, MENU_USER_MENUS umm2
            WHERE mu2.USER_GROUP_ID = umm2.UM_GROUP_ID
              AND mm2.MENU_ID = umm2.UM_MENU_ID
              AND mm2.MENU_PARENT_ID = '*'
              AND mu2.USER_ID = :1
          )
          AND mu.USER_ID = :1
        UNION
        SELECT mm.MENU_ID, {report_menu_scr_select}, mm.MENU_OPTION_DESC,
                       mm.MENU_BUTTON_1, mm.MENU_ACTION, mm.MENU_DISP_SEQ_NO 
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND (mm.MENU_BUTTON_1 LIKE '/reports/%' OR mm.MENU_ACTION_TYPE = 'R')
          AND mm.MENU_PARENT_ID IN (
            SELECT MENU_ID
            FROM MENU_USER mu3, MENU_MENUS mm3, MENU_USER_MENUS umm3
            WHERE mu3.USER_GROUP_ID = umm3.UM_GROUP_ID
              AND mm3.MENU_ID = umm3.UM_MENU_ID
              AND mm3.MENU_PARENT_ID IN (
                SELECT MENU_ID
                FROM MENU_USER mu4, MENU_MENUS mm4, MENU_USER_MENUS umm4
                WHERE mu4.USER_GROUP_ID = umm4.UM_GROUP_ID
                  AND mm4.MENU_ID = umm4.UM_MENU_ID
                  AND mm4.MENU_PARENT_ID = '*'
                  AND mu4.USER_ID = :1
              )
              AND mu3.USER_ID = :1
          )
          AND mu.USER_ID = :1
        UNION
        SELECT mm.MENU_ID, {report_menu_scr_select}, mm.MENU_OPTION_DESC,
                       mm.MENU_BUTTON_1, mm.MENU_ACTION, mm.MENU_DISP_SEQ_NO 
        FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
        WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
          AND mm.MENU_ID = umm.UM_MENU_ID
          AND (mm.MENU_BUTTON_1 LIKE '/reports/%' OR mm.MENU_ACTION_TYPE = 'R')
          AND mm.MENU_PARENT_ID IN (
            SELECT MENU_ID
            FROM MENU_USER mu5, MENU_MENUS mm5, MENU_USER_MENUS umm5
            WHERE mu5.USER_GROUP_ID = umm5.UM_GROUP_ID
              AND mm5.MENU_ID = umm5.UM_MENU_ID
              AND mm5.MENU_PARENT_ID IN (
                SELECT MENU_ID
                FROM MENU_USER mu6, MENU_MENUS mm6, MENU_USER_MENUS umm6
                WHERE mu6.USER_GROUP_ID = umm6.UM_GROUP_ID
                  AND mm6.MENU_ID = umm6.UM_MENU_ID
                  AND mm6.MENU_PARENT_ID IN (
                    SELECT MENU_ID
                    FROM MENU_USER mu7, MENU_MENUS mm7, MENU_USER_MENUS umm7
                    WHERE mu7.USER_GROUP_ID = umm7.UM_GROUP_ID
                      AND mm7.MENU_ID = umm7.UM_MENU_ID
                      AND mm7.MENU_PARENT_ID = '*'
                      AND mu7.USER_ID = :1
                  )
                  AND mu6.USER_ID = :1
              )
              AND mu5.USER_ID = :1
          )
          AND mu.USER_ID = :1
    ORDER BY MENU_DISP_SEQ_NO
    """
            
            print(f"STEP Fetching report menus for user: {username}")
            cursor.execute(report_menus_query, [username])
            report_results = cursor.fetchall()
            
            report_menus = []
            for row in report_results:
                menu_item = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'button_1': row[3],
                    'form_id': row[4],
                    'action': row[4],
                    'display_seq': row[5] or 999
                }
                
                # Process dynamic URL
                menu_item['processed_url'] = process_menu_url(menu_item)
                
                report_menus.append(menu_item)
            
            print(f"SUCCESS Found {len(report_menus)} report menus")
            return report_menus
            
    except Exception as e:
        print(f"FAIL Error getting report menus: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_global_menu_params(menu_id):
    """Get global menu parameters for a menu item"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT MENU_PARAMETER_1, MENU_PARAMETER_2, MENU_PARAMETER_3, MENU_PARAMETER_4, MENU_PARAMETER_5,
                       MENU_PARAMETER_6, MENU_PARAMETER_7, MENU_PARAMETER_8, MENU_PARAMETER_9, MENU_PARAMETER_10,
                       MENU_PARAMETER_11, MENU_PARAMETER_12, MENU_PARAMETER_13, MENU_PARAMETER_14, MENU_PARAMETER_15,
                       MENU_PARAMETER_16, MENU_PARAMETER_17, MENU_PARAMETER_18, MENU_PARAMETER_19, MENU_PARAMETER_20
                FROM MENU_MENUS 
                WHERE MENU_ID = :menu_id
            """
            
            cursor.execute(query, {'menu_id': menu_id})
            result = cursor.fetchone()
            
            if result:
                params = {}
                for i, value in enumerate(result, 1):
                    if value:
                        params[f'MENU_PARAMETER_{i}'] = value
                return params
            
            return {}
            
    except Exception as e:
        print(f"Error getting global menu params: {e}")
        return {}

def debug_user_menus(username):
    """Enhanced: Debug function to check user menu access with URL processing"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            print(f"\nSTEP DEBUGGING MENU ACCESS FOR USER: {username}")
            print("="*60)
            
            # Check user group
            cursor.execute("SELECT USER_GROUP_ID FROM MENU_USER WHERE USER_ID = :1", [username])
            user_group = cursor.fetchone()
            if user_group:
                print(f"User Group ID: {user_group[0]}")
            else:
                print("FAIL User not found in MENU_USER table")
                return
            
            # Check all menus user has access to (with MENU_ACTION)
            cursor.execute("""
                SELECT mm.MENU_ID, mm.MENU_PARENT_ID, mm.MENU_ACTION_TYPE, 
                       mm.MENU_SCR_NAME, mm.MENU_SEQ_NO, mm.MENU_BUTTON_1, mm.MENU_ACTION
                FROM MENU_USER mu 
                JOIN MENU_USER_MENUS umm ON mu.USER_GROUP_ID = umm.UM_GROUP_ID
                JOIN MENU_MENUS mm ON mm.MENU_ID = umm.UM_MENU_ID
                WHERE mu.USER_ID = :1
                ORDER BY mm.MENU_DISP_SEQ_NO, mm.MENU_ID
            """, [username])
            
            all_menus = cursor.fetchall()
            print(f"\nINFO Total menus accessible: {len(all_menus)}")
            
            # Process each menu and show URL processing
            print(f"\nURL URL Processing Results:")
            for menu in all_menus:
                menu_id, parent_id, action_type, scr_name, seq_no, button_1, menu_action = menu
                
                if button_1:  # Only process menus with URLs
                    # Process URL for this menu
                    menu_item = {
                        'id': menu_id,
                        'button_1': button_1,
                        'form_id': menu_action,
                        'action': menu_action
                    }
                    processed_url = process_menu_url(menu_item)
                    
                    print(f"  URL {menu_id}: {scr_name}")
                    print(f"     Original: {button_1}")
                    print(f"     Processed: {processed_url}")
                    print(f"     Form ID: {menu_action}")
                    if ':' in button_1:
                        print(f"     WARNING Contains placeholders: {'YES' if processed_url != button_1 else 'NO'}")
                    print()
            
            print("="*60)
            
    except Exception as e:
        print(f"FAIL Error debugging menus: {e}")
        import traceback
        traceback.print_exc()

# Enhanced template filter function
def process_menu_url_filter(menu_url, form_id=None, menu_id=None):
    """Enhanced template filter to process menu URLs"""
    if not menu_url:
        return '#'
    
    processed_url = menu_url
    
    # Replace placeholders
    if menu_id and ':id' in processed_url:
        processed_url = processed_url.replace(':id', str(menu_id))
    if form_id and ':form_id' in processed_url:
        processed_url = processed_url.replace(':form_id', str(form_id))
    
    return processed_url

# NEW: Function to test URL processing
def test_menu_url_processing():
    """Test function to verify URL processing works correctly"""
    print("\nTEST TESTING MENU URL PROCESSING")
    print("="*40)
    
    test_cases = [
        {
            'id': 'T010509',
            'button_1': '/reports/:form_id/:id',
            'form_id': 'TTL201',
            'expected': '/reports/TTL201/T010509'
        },
        {
            'id': 'T010510',
            'button_1': '/reports/:form_id/:id',
            'form_id': 'TTL202',
            'expected': '/reports/TTL202/T010510'
        },
        {
            'id': 'T010511',
            'button_1': '/static/page.html',
            'form_id': None,
            'expected': '/static/page.html'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['id']}")
        result = process_menu_url(test_case)
        expected = test_case['expected']
        status = "SUCCESS PASS" if result == expected else "FAIL FAIL"
        
        print(f"  Input: {test_case['button_1']}")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")
        print(f"  Status: {status}")
        print()
    
    print("="*40)