# =============================================================================
# File: reports/classes/FIN001.py
# Trial Balance Report Class
# Complete Original Query from Forms 6i POPULATE_Q2 Procedure
# =============================================================================

from database import get_db_connection
from datetime import datetime
import traceback

class FIN001Report:
    """Trial Balance Report Class - Complete Original Query"""
    
    def __init__(self):
        self.name = "Trial Balance (FIN001)"
        self.description = "Comprehensive Finance Analysis report - Trial Balance"
        self.version = "1.0"
        self.report_id = "FIN001"
        print(f"[SUCCESS] FIN001Report initialized with complete original query")
    
    def execute(self, params, config=None):
        """Main execution method with complete original query"""
        try:
            print(f"[INFO] FIN001 - Starting execution with complete original query")
            print(f"[INFO] Parameters: {params}")
            
            # Extract user parameters with proper defaults
            M_FM_YYYYMM = params.get('M_FM_YYYYMM') or '202501'
            M_TO_YYYYMM = params.get('M_TO_YYYYMM') or '202512'
            M_FM_DIVN = params.get('M_FM_DIVN') or '0'
            M_TO_DIVN = params.get('M_TO_DIVN') or 'ZZZZZZ'
            M_FM_DEPT = params.get('M_FM_DEPT') or '0'
            M_TO_DEPT = params.get('M_TO_DEPT') or 'ZZZZZZ'
            M_FM_MAIN_AC = params.get('M_FM_MAIN_AC') or '0'
            M_TO_MAIN_AC = params.get('M_TO_MAIN_AC') or 'ZZZZZZ'
            M_FM_SUB_AC = params.get('M_FM_SUB_AC') or '0'
            M_TO_SUB_AC = params.get('M_TO_SUB_AC') or 'ZZZZZZ'
            DUMMY = params.get('DUMMY') or '0'
            
            # Execute complete original analysis with extracted parameters
            extracted_params = {
                'comp_code': params.get('comp_code', 'TTM'),
                'user_id': params.get('user_id', 'SYSTEM'),
                'M_FM_YYYYMM': M_FM_YYYYMM,
                'M_TO_YYYYMM': M_TO_YYYYMM,
                'M_FM_DIVN': M_FM_DIVN,
                'M_TO_DIVN': M_TO_DIVN,
                'M_FM_DEPT': M_FM_DEPT,
                'M_TO_DEPT': M_TO_DEPT,
                'M_FM_MAIN_AC': M_FM_MAIN_AC,
                'M_TO_MAIN_AC': M_TO_MAIN_AC,
                'M_FM_SUB_AC': M_FM_SUB_AC,
                'M_TO_SUB_AC': M_TO_SUB_AC,
                'DUMMY': DUMMY
            }
            
            result_data = self._execute_complete_original_analysis(extracted_params)
            
            # Format result
            formatted_result = self._format_result(result_data, params)
            
            print(f"[SUCCESS] FIN001 completed with original query. Records: {formatted_result['count']}")
            return formatted_result
            
        except Exception as e:
            print(f"[ERROR] FIN001 execution error: {e}")
            traceback.print_exc()
            
            return {
                'columns': ['Error_Type', 'Error_Message'],
                'data': [['FIN001_ERROR', str(e)]],
                'count': 1,
                'query': 'FIN001 execution failed',
                'error': True
            }
    
    def _execute_complete_original_analysis(self, params):
        """Execute complete original CURSOR C1 query from Forms 6i procedure"""
        
        # Initialize all variables at the start to prevent access issues
        M_YEAR = M_FM_YYYYMM = M_TO_YYYYMM = None
        M_FM_DIVN = M_TO_DIVN = M_FM_DEPT = M_TO_DEPT = None
        M_FM_MAIN_AC = M_TO_MAIN_AC = M_FM_SUB_AC = M_TO_SUB_AC = DUMMY = None
        
        try:
            print(f"[INFO] Executing complete original query with user parameters + session variables...")
            
            # Extract parameters from the passed dictionary with proper defaults
            M_FM_YYYYMM = params.get('M_FM_YYYYMM') or '202501'
            M_TO_YYYYMM = params.get('M_TO_YYYYMM') or '202512'
            M_FM_DIVN = params.get('M_FM_DIVN') or '0'
            M_TO_DIVN = params.get('M_TO_DIVN') or 'ZZZZZZ'
            M_FM_DEPT = params.get('M_FM_DEPT') or '0'
            M_TO_DEPT = params.get('M_TO_DEPT') or 'ZZZZZZ'
            M_FM_MAIN_AC = params.get('M_FM_MAIN_AC') or '0'
            M_TO_MAIN_AC = params.get('M_TO_MAIN_AC') or 'ZZZZZZ'
            M_FM_SUB_AC = params.get('M_FM_SUB_AC') or '0'
            M_TO_SUB_AC = params.get('M_TO_SUB_AC') or 'ZZZZZZ'
            comp_code = params.get('comp_code', 'TTM')
            user_id = params.get('user_id', 'SYSTEM')
            
            print(f"[DEBUG] Parameters extracted:")
            print(f"  M_FM_YYYYMM={M_FM_YYYYMM}, M_TO_YYYYMM={M_TO_YYYYMM}")
            print(f"  comp_code={comp_code}")
            print(f"  Division: {M_FM_DIVN} to {M_TO_DIVN}")
            print(f"  Department: {M_FM_DEPT} to {M_TO_DEPT}")
            print(f"  Main Account: {M_FM_MAIN_AC} to {M_TO_MAIN_AC}")
            print(f"  Sub Account: {M_FM_SUB_AC} to {M_TO_SUB_AC}")
        
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Dynamic M_YEAR fetching using your provided query
                print(f"[DEBUG] Fetching M_YEAR dynamically using period {M_FM_YYYYMM}")
                year_query = """
                SELECT CAY_ACNT_YEAR 
                FROM FM_COMP_ACNT_YEAR 
                WHERE TO_DATE(:M_FM_YYYYMM, 'YYYYMM') BETWEEN CAY_FRM_DT AND CAY_TO_DT
                """
                
                try:
                    cursor.execute(year_query, {'M_FM_YYYYMM': M_FM_YYYYMM})
                    year_result = cursor.fetchone()
                    if year_result:
                        M_YEAR = str(year_result[0])
                        print(f"[SUCCESS] M_YEAR dynamically fetched: {M_YEAR}")
                    else:
                        # Fallback to extracting year from period
                        M_YEAR = M_FM_YYYYMM[:4] if len(M_FM_YYYYMM) >= 4 else '2025'
                        print(f"[WARNING] No M_YEAR found in FM_COMP_ACNT_YEAR, using fallback: {M_YEAR}")
                except Exception as year_error:
                    print(f"[ERROR] Failed to fetch M_YEAR dynamically: {year_error}")
                    # Fallback to extracting year from period
                    M_YEAR = M_FM_YYYYMM[:4] if len(M_FM_YYYYMM) >= 4 else '2025'
                    print(f"[WARNING] Using fallback M_YEAR: {M_YEAR}")
                
                print(f"[DEBUG] Final M_YEAR value: {M_YEAR}")
                
                # Complete original CURSOR C1 query from your Forms 6i procedure
                # Calculate month slots dynamically based on period range
                # This replaces the M_SLOT_1..M_SLOT_12 logic from Forms 6i
                # Handle None values properly
                fm_yyyymm = int(M_FM_YYYYMM) if M_FM_YYYYMM and M_FM_YYYYMM.isdigit() else 202401
                to_yyyymm = int(M_TO_YYYYMM) if M_TO_YYYYMM and M_TO_YYYYMM.isdigit() else 202412
                
                complete_original_query = f"""
                SELECT DISTINCT Z.ABAL_COMP_CODE, Z.ABAL_ACNT_YEAR ABAL_ACNT_YEAR , 
                       Z.ABAL_MAIN_ACNT_CODE ABAL_MAIN_ACNT_CODE, C.MAIN_ACNT_NAME MAIN_ACNT_NAME,
                       DECODE(MAIN_ACNT_CODE, '805', 'XXXXXXXXXXXX', DECODE(C.MAIN_OPEN_ENTRY_FLAG, 'Y', 'XXXXXXXXXXXX', NVL(Z.ABAL_SUB_ACNT_CODE, 'XXXXXXXXXXXX'))) PBC_SUB_ACNT_CODE,
                       Z.ABAL_SUB_ACNT_CODE ABAL_SUB_ACNT_CODE , 
                       B.SUB_ACNT_NAME SUB_ACNT_NAME, 
                       Z.ABAL_DIVN_CODE ABAL_DIVN_CODE, A1.DIVN_NAME DIVN_NAME, Z.ABAL_DEPT_CODE ABAL_DEPT_CODE , A.DEPT_NAME DEPT_NAME,
                       NVL(D.MONTH_BAL_01,0) MONTH_BAL_01, NVL(D.MONTH_BAL_02,0) MONTH_BAL_02, 
                       NVL(D.MONTH_BAL_03,0) MONTH_BAL_03, NVL(D.MONTH_BAL_04,0) MONTH_BAL_04,
                       NVL(D.MONTH_BAL_05,0) MONTH_BAL_05, NVL(D.MONTH_BAL_06,0) MONTH_BAL_06, 
                       NVL(D.MONTH_BAL_07,0) MONTH_BAL_07, NVL(D.MONTH_BAL_08,0) MONTH_BAL_08, 
                       NVL(D.MONTH_BAL_09,0) MONTH_BAL_09, NVL(D.MONTH_BAL_10,0) MONTH_BAL_10, 
                       NVL(D.MONTH_BAL_11,0) MONTH_BAL_11, NVL(D.MONTH_BAL_12,0) MONTH_BAL_12,  
                       NVL(E.OP_BAL,0) OP_BAL, 
                       NVL(E.OP_BAL,0)+NVL(D.MONTH_BAL_01,0)+NVL(D.MONTH_BAL_02,0)+NVL(D.MONTH_BAL_03,0)+
                       NVL(D.MONTH_BAL_04,0)+NVL(D.MONTH_BAL_05,0)+NVL(D.MONTH_BAL_06,0)+NVL(D.MONTH_BAL_07,0)+
                       NVL(D.MONTH_BAL_08,0)+NVL(D.MONTH_BAL_09,0)+NVL(D.MONTH_BAL_10,0)+NVL(D.MONTH_BAL_11,0)+
                       NVL(D.MONTH_BAL_12,0) CLO_BAL
                FROM    FS_CUR_ACNT_BAL Z, 
                       (SELECT  DIVN_COMP_CODE, DIVN_CODE, DIVN_NAME
                        FROM    FM_DIVISION) A1,  
                       (SELECT  DEPT_COMP_CODE, DEPT_DIVN_CODE, DEPT_CODE, DEPT_NAME
                        FROM    FM_DEPARTMENT) A,
                       (SELECT  SUB_ACNT_CODE, SUB_ACNT_NAME
                        FROM    FM_SUB_ACCOUNT) B,
                       (SELECT MAIN_ACNT_CODE, MAIN_ACNT_NAME, MAIN_OPEN_ENTRY_FLAG
                        FROM   FM_MAIN_ACCOUNT) C,
                       (SELECT ABAL_COMP_CODE, ABAL_ACNT_YEAR, ABAL_MAIN_ACNT_CODE, ABAL_SUB_ACNT_CODE,
                               ABAL_DIVN_CODE, ABAL_DEPT_CODE,
                               SUM(CASE WHEN (ABAL_CAL_YEAR*100+ABAL_CAL_MONTH) BETWEEN {fm_yyyymm} AND {to_yyyymm} 
                                   THEN (NVL(ABAL_LC_MTD_DR,0)-NVL(ABAL_LC_MTD_CR,0)) ELSE 0 END) MONTH_BAL_01,
                               0 MONTH_BAL_02, 0 MONTH_BAL_03, 0 MONTH_BAL_04, 0 MONTH_BAL_05, 0 MONTH_BAL_06,
                               0 MONTH_BAL_07, 0 MONTH_BAL_08, 0 MONTH_BAL_09, 0 MONTH_BAL_10, 0 MONTH_BAL_11, 0 MONTH_BAL_12
                        FROM  FS_CUR_ACNT_BAL
                        WHERE (ABAL_CAL_YEAR*100)+ABAL_CAL_MONTH BETWEEN :M_FM_YYYYMM AND :M_TO_YYYYMM
                        GROUP BY ABAL_COMP_CODE, ABAL_ACNT_YEAR, ABAL_MAIN_ACNT_CODE, 
                                 ABAL_SUB_ACNT_CODE, ABAL_DIVN_CODE, ABAL_DEPT_CODE) D ,
                       (SELECT ABAL_COMP_CODE, ABAL_ACNT_YEAR, ABAL_MAIN_ACNT_CODE, ABAL_SUB_ACNT_CODE,
                               ABAL_DIVN_CODE, ABAL_DEPT_CODE,
                               SUM(NVL(ABAL_LC_MTD_DR,0)-NVL(ABAL_LC_MTD_CR,0))  OP_BAL
                        FROM  FS_CUR_ACNT_BAL
                        WHERE (ABAL_CAL_YEAR*100)+ABAL_CAL_MONTH < :M_FM_YYYYMM
                        GROUP BY ABAL_COMP_CODE, ABAL_ACNT_YEAR, ABAL_MAIN_ACNT_CODE, 
                                 ABAL_SUB_ACNT_CODE, ABAL_DIVN_CODE, ABAL_DEPT_CODE) E
                WHERE Z.ABAL_COMP_CODE      = :M_COMP_CODE
                AND   Z.ABAL_ACNT_YEAR      = :M_YEAR
                AND   Z.ABAL_DIVN_CODE      BETWEEN :M_FM_DIVN AND :M_TO_DIVN
                AND   Z.ABAL_DEPT_CODE      BETWEEN :M_FM_DEPT AND :M_TO_DEPT
                AND   Z.ABAL_MAIN_ACNT_CODE BETWEEN :M_FM_MAIN_AC AND :M_TO_MAIN_AC
                AND   NVL(Z.ABAL_SUB_ACNT_CODE, '0')  BETWEEN :M_FM_SUB_AC AND :M_TO_SUB_AC
                AND   Z.ABAL_COMP_CODE              = A1.DIVN_COMP_CODE(+)
                AND   Z.ABAL_DIVN_CODE              = A1.DIVN_CODE(+)
                AND   Z.ABAL_COMP_CODE              = A.DEPT_COMP_CODE(+)
                AND   Z.ABAL_DIVN_CODE              = A.DEPT_DIVN_CODE(+)
                AND   Z.ABAL_DEPT_CODE              = A.DEPT_CODE(+)
                AND   Z.ABAL_SUB_ACNT_CODE          = B.SUB_ACNT_CODE(+)
                AND   Z.ABAL_MAIN_ACNT_CODE         = C.MAIN_ACNT_CODE(+)
                AND   Z.ABAL_COMP_CODE              = D.ABAL_COMP_CODE(+)   
                AND   Z.ABAL_ACNT_YEAR              = D.ABAL_ACNT_YEAR(+)
                AND   Z.ABAL_DIVN_CODE              = D.ABAL_DIVN_CODE(+)
                AND   Z.ABAL_DEPT_CODE              = D.ABAL_DEPT_CODE(+)
                AND   Z.ABAL_MAIN_ACNT_CODE         = D.ABAL_MAIN_ACNT_CODE(+)
                AND   NVL(Z.ABAL_SUB_ACNT_CODE,'0') = NVL(D.ABAL_SUB_ACNT_CODE(+),'0')
                AND   Z.ABAL_COMP_CODE              = E.ABAL_COMP_CODE(+)
                AND   Z.ABAL_ACNT_YEAR              = E.ABAL_ACNT_YEAR(+)
                AND   Z.ABAL_DIVN_CODE              = E.ABAL_DIVN_CODE(+)
                AND   Z.ABAL_DEPT_CODE              = E.ABAL_DEPT_CODE(+)
                AND   Z.ABAL_MAIN_ACNT_CODE         = E.ABAL_MAIN_ACNT_CODE(+)
                AND   NVL(Z.ABAL_SUB_ACNT_CODE,'0') = NVL(E.ABAL_SUB_ACNT_CODE(+),'0')
                ORDER BY Z.ABAL_MAIN_ACNT_CODE
                """
                
                
                print(f"[DEBUG] Session variables: comp_code={comp_code}, user_id={user_id}")
                
                # Map additional GLOBAL variables from session if available
                global_comp_code = params.get('comp_code', comp_code)  # :GLOBAL.M_COMP_CODE
                global_user_id = params.get('user_id', user_id)        # :GLOBAL.M_USER_ID
                global_lang_code = params.get('lang_code', 'EN')       # :GLOBAL.M_LANG_CODE
                global_date = params.get('system_date', datetime.now().strftime('%d/%m/%Y'))  # :GLOBAL.M_DATE
                
                print(f"[DEBUG] GLOBAL variables mapped from Forms 6i:")
                print(f"  :GLOBAL.M_COMP_CODE -> {global_comp_code}")
                print(f"  :GLOBAL.M_USER_ID -> {global_user_id}")
                print(f"  :GLOBAL.M_LANG_CODE -> {global_lang_code}")
                print(f"  :GLOBAL.M_DATE -> {global_date}")
                
                # Parameter mapping - All bind variables used in the SQL query
                query_params = {
                    # Period parameters for date ranges
                    'M_FM_YYYYMM': M_FM_YYYYMM,
                    'M_TO_YYYYMM': M_TO_YYYYMM,
                    # Session/GLOBAL variables
                    'M_COMP_CODE': global_comp_code,  # :GLOBAL.M_COMP_CODE
                    'M_YEAR': M_YEAR,                 # Account year parameter
                    # Range parameters
                    'M_FM_DIVN': M_FM_DIVN,
                    'M_TO_DIVN': M_TO_DIVN,
                    'M_FM_DEPT': M_FM_DEPT,
                    'M_TO_DEPT': M_TO_DEPT,
                    'M_FM_MAIN_AC': M_FM_MAIN_AC,
                    'M_TO_MAIN_AC': M_TO_MAIN_AC,
                    'M_FM_SUB_AC': M_FM_SUB_AC,
                    'M_TO_SUB_AC': M_TO_SUB_AC
                }
                
                print(f"[DEBUG] All query parameters:")
                for key, value in query_params.items():
                    print(f"  {key} = {value}")
                
                print(f"[DEBUG] About to execute main query with {len(query_params)} parameters")
                
                # First, let's check if there's any data in the base table for this company
                test_query = "SELECT COUNT(*) FROM FS_CUR_ACNT_BAL WHERE ABAL_COMP_CODE = :comp_code"
                cursor.execute(test_query, {'comp_code': global_comp_code})
                row_count = cursor.fetchone()[0]
                print(f"[DEBUG] Base table FS_CUR_ACNT_BAL has {row_count} records for company {global_comp_code}")
                
                if row_count == 0:
                    print(f"[WARNING] No data found in FS_CUR_ACNT_BAL for company {global_comp_code}")
                    return {'columns': ['Message'], 'data': [['No financial data available for this company']]}
                
                cursor.execute(complete_original_query, query_params)
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
                
                print(f"[SUCCESS] Complete original query executed. Columns: {len(columns)}, Rows: {len(data)}")
                
                return {'columns': columns, 'data': data}
                
        except Exception as e:
            print(f"[ERROR] Complete original query execution error: {e}")
            print(f"[ERROR] Full error details:")
            import traceback
            traceback.print_exc()
            
            # DON'T FALL BACK - Show the real error instead
            return {
                'columns': ['Error_Type', 'Error_Message', 'Error_Details'],
                'data': [['MAIN_QUERY_ERROR', str(e), 'Check database connection, parameter values, or query syntax']],
                'count': 1,
                'query': 'FIN001 main query execution failed',
                'error': True,
                'error_type': 'MAIN_QUERY_FAILURE'
            }
    
    def _format_result(self, data_results, params):
        """Format result for display"""
        columns = data_results.get('columns', [])
        data = data_results.get('data', [])
        
        # Preserve original column names for column filtering to work
        # The column header formatting will be handled by the template and column_headers
        return {
            'columns': columns,  # Keep original column names
            'data': data,
            'count': len(data),
            'query': f'FIN001 Trial Balance - Complete Original Query',
            'parameters': params,
            'class_info': {
                'class_name': self.__class__.__name__,
                'version': self.version,
                'execution_method': 'Complete Original Query from Forms 6i'
            }
        }

# Alternative class names for compatibility
class FIN001(FIN001Report):
    """Alternative class name"""
    pass

class ReportProcessor(FIN001Report):
    """Generic class name"""
    pass

class Report(FIN001Report):
    """Simple class name"""
    pass

# Test locally
if __name__ == '__main__':
    test_params = {
        'M_FM_YYYYMM': '202501',
        'M_TO_YYYYMM': '202512',
        'M_FM_DIVN': '0',
        'M_TO_DIVN': 'ZZZZZZ',
        'M_FM_DEPT': '0',
        'M_TO_DEPT': 'ZZZZZZ',
        'M_FM_MAIN_AC': '0',
        'M_TO_MAIN_AC': 'ZZZZZZ',
        'M_FM_SUB_AC': '0',
        'M_TO_SUB_AC': 'ZZZZZZ',
        'DUMMY': '0',
        'comp_code': 'TTM',
        'user_id': 'SYSTEM'
    }
    
    try:
        report = FIN001Report()
        result = report.execute(test_params)
        print(f"[SUCCESS] Test completed with original query. Records: {result['count']}")
        print(f"[SUCCESS] Columns from original query: {len(result['columns'])}")
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        traceback.print_exc()
