from flask import Blueprint, jsonify, session
from database import get_db_connection
from services.menu_service import debug_user_menus, get_user_menus

api_bp = Blueprint('api', __name__)

@api_bp.route('/lov/<lov_type>')
def get_lov_data(lov_type):
    """Get List of Values data for parameter fields"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            lov_queries = {
                'sdm_codes': """
                    SELECT SDM_CODE as "Code", SDM_NAME as "Name", SDM_PHONE as "Phone"
                    FROM SDM_MASTER 
                    WHERE SDM_COMP_CODE = :comp_code
                    ORDER BY SDM_CODE
                """,
                'customer_codes': """
                    SELECT CUST_CODE as "Code", CUST_NAME as "Name", CUST_CITY as "City"
                    FROM CUSTOMER_MASTER
                    WHERE CUST_COMP_CODE = :comp_code  
                    ORDER BY CUST_CODE
                """,
                'flash_codes': """
                    SELECT FLASH_CODE as "Code", FLASH_DESC as "Description"
                    FROM FLASH_MASTER
                    WHERE FLASH_COMP_CODE = :comp_code
                    ORDER BY FLASH_CODE
                """,
                'item_codes': """
                    SELECT ITEM_CODE as "Code", ITEM_DESC as "Description", ITEM_UOM as "UOM"
                    FROM ITEM_MASTER
                    WHERE ITEM_COMP_CODE = :comp_code
                    ORDER BY ITEM_CODE
                """,
                'location_codes': """
                    SELECT LOCN_CODE as "Code", LOCN_NAME as "Name", LOCN_CITY as "City"
                    FROM LOCATION_MASTER  
                    WHERE LOCN_COMP_CODE = :comp_code
                    ORDER BY LOCN_CODE
                """
            }
            
            query = lov_queries.get(lov_type)
            if not query:
                return jsonify({'error': 'Invalid LOV type'}), 400
            
            cursor.execute(query, {'comp_code': session['company_code']})
            
            # Convert to list of dictionaries
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
            
            return jsonify(data)
            
    except Exception as e:
        print(f"Error getting LOV data: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/debug-menus')
def debug_menus():
    """Debug route to check menu structure"""
    if 'user_id' not in session:
        return "Please login first"
    
    username = session['user_id']
    debug_user_menus(username)
    
    # Get processed menus
    user_menus = get_user_menus(username)
    
    def menu_to_dict(menu, level=0):
        return {
            'level': level,
            'id': menu['id'],
            'name': menu['name'],
            'parent_id': menu['parent_id'],
            'action_type': menu['action_type'],
            'button_1': menu['button_1'],
            'children_count': len(menu['children']),
            'children': [menu_to_dict(child, level+1) for child in menu['children']]
        }
    
    debug_data = [menu_to_dict(menu) for menu in user_menus]
    
    return jsonify({
        'user': username,
        'menu_count': len(user_menus),
        'menus': debug_data
    })