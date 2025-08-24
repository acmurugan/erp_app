import oracledb
import socket
import os
from datetime import datetime
from config import Config

def init_oracle_client():
    """Initialize Oracle client"""
    try:
        oracledb.init_oracle_client(lib_dir=Config.ORACLE_CLIENT_PATH)
        print("Oracle client initialized successfully")
    except Exception as e:
        print(f"Oracle client warning: {e}")

def get_db_connection():
    """Get database connection"""
    try:
        return oracledb.connect(
            user=Config.DB_USER, 
            password=Config.DB_PASS, 
            dsn=Config.DB_DSN
        )
    except Exception as e:
        print(f"[ERROR] Database connection error: {e}")
        raise

def insert_login_detail(username, company_code, branch_code, user_desc):
    """Insert login details into IM_LOGIN_USER_DETAIL table"""
    try:
        print(f"KEY Attempting to insert login detail...")
        print(f"   User: {username}")
        print(f"   Company: {company_code}")
        print(f"   Branch: {branch_code}")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get next sequence value for LUD_SYS_ID
            seq_query = "SELECT LUD_SYS_ID.NEXTVAL FROM DUAL"
            cursor.execute(seq_query)
            next_sys_id = cursor.fetchone()[0]
            print(f"   Next SYS_ID from sequence: {next_sys_id}")
            
            # Get machine name and OS user (simulated for web application)
            machine_name = socket.gethostname()
            os_user = os.environ.get('USERNAME', 'WEB_USER')
            
            print(f"   Machine: {machine_name}")
            print(f"   OS User: {os_user}")
            
            # Insert login details matching the exact table structure
            insert_query = """
                INSERT INTO IM_LOGIN_USER_DETAIL (
                    LUD_SYS_ID,
                    LUD_COMP_CODE,
                    LUD_USER_ID,
                    LUD_LOCN_CODE,
                    LUD_SID_NO,
                    LUD_MACHINE_NAME,
                    LUD_OSUSER,
                    LUD_LOGIN_DT,
                    LUD_CR_DT,
                    LUD_CR_UID
                ) VALUES (
                    :sys_id,
                    :comp_code,
                    :user_id,
                    :locn_code,
                    :sid_no,
                    :machine_name,
                    :os_user,
                    SYSDATE,
                    SYSDATE,
                    :cr_uid
                )
            """
            
            # Get session ID (simulated - you can enhance this)
            sid_no = 1  # You can enhance this to get actual database session ID
            
            cursor.execute(insert_query, {
                'sys_id': next_sys_id,
                'comp_code': company_code,
                'user_id': username,
                'locn_code': branch_code if branch_code else None,
                'sid_no': sid_no,
                'machine_name': machine_name[:40],  # Limit to 40 chars
                'os_user': os_user[:256],  # Limit to 256 chars
                'cr_uid': username
            })
            
            # Check if row was inserted
            rows_affected = cursor.rowcount
            print(f"INFO Rows affected: {rows_affected}")
            
            conn.commit()
            print(f"SUCCESS Login detail inserted successfully with SYS_ID: {next_sys_id}")
            
            # Verify insertion
            verify_query = "SELECT COUNT(*) FROM IM_LOGIN_USER_DETAIL WHERE LUD_SYS_ID = :sys_id"
            cursor.execute(verify_query, {'sys_id': next_sys_id})
            verify_count = cursor.fetchone()[0]
            print(f"CHECK Verification count: {verify_count}")
            
            return next_sys_id
            
    except Exception as e:
        print(f"ERROR Error inserting login detail: {e}")
        print(f"ERROR Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

def update_logout_detail(sys_id):
    """Update logout time in IM_LOGIN_USER_DETAIL table"""
    try:
        print(f"KEY Attempting to update logout for SYS_ID: {sys_id}")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # First check if record exists
            check_query = """
                SELECT LUD_USER_ID, LUD_LOGIN_DT, LUD_LOGOUT_DT 
                FROM IM_LOGIN_USER_DETAIL 
                WHERE LUD_SYS_ID = :sys_id
            """
            cursor.execute(check_query, {'sys_id': sys_id})
            existing_record = cursor.fetchone()
            
            if not existing_record:
                print(f"ERROR No record found with SYS_ID: {sys_id}")
                return False
            
            user_id, login_dt, logout_dt = existing_record
            print(f"SUCCESS Found record - User: {user_id}, Login: {login_dt}, Current Logout: {logout_dt}")
            
            # Update logout time and update fields
            update_query = """
                UPDATE IM_LOGIN_USER_DETAIL
                SET LUD_LOGOUT_DT = SYSDATE,
                    LUD_UPD_DT = SYSDATE,
                    LUD_UPD_UID = :upd_uid
                WHERE LUD_SYS_ID = :sys_id
            """
            
            cursor.execute(update_query, {
                'upd_uid': user_id,
                'sys_id': sys_id
            })
            
            # Check rows affected
            rows_affected = cursor.rowcount
            print(f"INFO Rows affected: {rows_affected}")
            
            conn.commit()
            
            if rows_affected > 0:
                print(f"SUCCESS Logout time updated successfully for SYS_ID: {sys_id}")
                
                # Verify update
                cursor.execute(check_query, {'sys_id': sys_id})
                updated_record = cursor.fetchone()
                if updated_record:
                    print(f"CHECK Updated record: Login: {updated_record[1]}, Logout: {updated_record[2]}")
                
                return True
            else:
                print(f"ERROR No rows updated for SYS_ID: {sys_id}")
                return False
            
    except Exception as e:
        print(f"ERROR Error updating logout detail: {e}")
        print(f"ERROR Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def validate_user_credentials(username, password):
    """Validate user credentials against MENU_USER table"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            user_query = """
                SELECT USER_ID, USER_DESC, USER_GROUP_ID
                FROM MENU_USER 
                WHERE USER_ID = :1 
                  AND USER_PASSWD = :2 
                  AND NVL(USER_DISABLE_FLAG, 'N') <> 'Y'
            """
            
            cursor.execute(user_query, [username, password])
            user_result = cursor.fetchone()
            
            if user_result:
                return {
                    'user_id': user_result[0],
                    'user_desc': user_result[1],
                    'user_group_id': user_result[2]
                }
            return None
            
    except Exception as e:
        print(f"ERROR Error validating user credentials: {e}")
        return None

def validate_company_code(company_code):
    """Validate company code against FM_COMPANY table"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            company_query = """
                SELECT COMP_NAME
                FROM FM_COMPANY
                WHERE COMP_CODE = :1
                  AND NVL(COMP_FRZ_FLAG, 'N') != 'Y'
            """
            
            cursor.execute(company_query, [company_code])
            company_result = cursor.fetchone()
            
            if company_result:
                return company_result[0]  # Return company name
            return None
            
    except Exception as e:
        print(f"⚌ Error validating company code: {e}")
        return None

def validate_branch_code(branch_code, username):
    """Validate branch code against OM_LOCATION and OM_LOCATION_USER tables"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            branch_query = """
                SELECT loc.LOCN_NAME
                FROM OM_LOCATION loc
                JOIN OM_LOCATION_USER usr ON loc.LOCN_CODE = usr.LUSR_LOCN_CODE
                WHERE usr.LUSR_LOCN_CODE = :1
                  AND usr.LUSR_USER_ID = :2
                  AND NVL(usr.LUSR_FRZ_FLAG_NUM, 2) != 1
                  AND NVL(loc.LOCN_FRZ_FLAG_NUM, 2) != 1
            """
            
            cursor.execute(branch_query, [branch_code, username])
            branch_result = cursor.fetchone()
            
            if branch_result:
                return branch_result[0]  # Return location name
            return None
            
    except Exception as e:
        print(f"⚌ Error validating branch code: {e}")
        return None

def get_user_menu_count(username):
    """Get count of menus accessible to user"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            menu_count_query = """
                SELECT COUNT(*) FROM (
                    SELECT DISTINCT mm.MENU_ID
                    FROM MENU_USER mu, MENU_MENUS mm, MENU_USER_MENUS umm
                    WHERE mu.USER_GROUP_ID = umm.UM_GROUP_ID
                      AND mm.MENU_ID = umm.UM_MENU_ID
                      AND mu.USER_ID = :1
                )
            """
            
            cursor.execute(menu_count_query, [username])
            menu_count = cursor.fetchone()[0]
            return menu_count
            
    except Exception as e:
        print(f"⚌ Error getting user menu count: {e}")
        return 0

def get_table_count(table_name):
    """Get count of rows in a table"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"⚠ Warning: Could not get count for {table_name}: {e}")
        return 0

def get_user_tables(limit=10):
    """Get list of user accessible tables"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT table_name FROM user_tables WHERE ROWNUM <= {limit} ORDER BY table_name")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"⚠ Warning: Error getting tables: {e}")
        return []

def get_table_structure(table_name):
    """Get table column information"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT column_name, data_type, nullable 
                FROM user_tab_columns 
                WHERE table_name = :1 
                ORDER BY column_id
            """, [table_name])
            
            columns = []
            for col_name, data_type, nullable in cursor.fetchall():
                columns.append({
                    'name': col_name,
                    'type': data_type,
                    'nullable': nullable == 'Y'
                })
            
            return columns
    except Exception as e:
        print(f"⚌ Error getting table structure for {table_name}: {e}")
        return []

def get_table_data(table_name, limit=50):
    """Get limited data from table"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE ROWNUM <= {limit} ORDER BY 1")
            return cursor.fetchall()
    except Exception as e:
        print(f"⚌ Error getting table data for {table_name}: {e}")
        return []

def test_database_connection():
    """Test database connectivity"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 'Database connection successful' as status, SYSDATE as current_time FROM DUAL")
            result = cursor.fetchone()
            print(f"✅ Database test: {result[0]} at {result[1]}")
            return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False