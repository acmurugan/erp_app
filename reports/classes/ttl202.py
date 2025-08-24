# =============================================================================
# File: reports/classes/TTL202.py
# Item Wise Sales Analysis Report Class
# Complete Original Query from Forms 6i POPULATE_Q2 Procedure
# =============================================================================

from database import get_db_connection
from datetime import datetime
import traceback

class TTL202Report:
    """Item Wise Sales Analysis Report Class - Complete Original Query"""
    
    def __init__(self):
        self.name = "Item Wise Sales Analysis (TTL202)"
        self.description = "Comprehensive sales analysis report with item details, cost calculations, margin analysis, and customer information. Converted from Forms 6i POPULATE_Q2 procedure."
        self.version = "1.0"
        self.report_id = "TTL202"
        print(f"[SUCCESS] TTL202Report initialized with complete original query")
    
    def execute(self, params, config=None):
        """Main execution method with complete original query"""
        try:
            print(f"[INFO] TTL202 - Starting execution with complete original query")
            print(f"[INFO] Parameters: {params}")
            
            # Extract user parameters
            from_cust_anly_02 = params.get('from_cust_anly_02', '0')
            to_cust_anly_02 = params.get('to_cust_anly_02', 'ZZZZZ')
            from_item_anly_12 = params.get('from_item_anly_12', '0')
            to_item_anly_12 = params.get('to_item_anly_12', 'ZZZZZZ')
            from_cust_code = params.get('from_cust_code', '0')
            to_cust_code = params.get('to_cust_code', 'ZZZZ')
            from_item_code = params.get('from_item_code', '0')
            to_item_code = params.get('to_item_code', 'ZZZZZ')
            from_date = params.get('from_date', '01/01/2024')
            to_date = params.get('to_date', '31/12/2024')
            from_locn_code = params.get('from_locn_code', '0')
            to_locn_code = params.get('to_locn_code', 'ZZZZZZZ')
            
            # Execute complete original analysis with extracted parameters
            extracted_params = {
                'from_cust_anly_02': from_cust_anly_02,
                'to_cust_anly_02': to_cust_anly_02,
                'from_item_anly_12': from_item_anly_12,
                'to_item_anly_12': to_item_anly_12,
                'from_cust_code': from_cust_code,
                'to_cust_code': to_cust_code,
                'from_item_code': from_item_code,
                'to_item_code': to_item_code,
                'from_date': from_date,
                'to_date': to_date,
                'from_locn_code': from_locn_code,
                'to_locn_code': to_locn_code,
                'comp_code': params.get('comp_code', 'TTM'),
                'user_id': params.get('user_id', 'SYSTEM')
            }
            result_data = self._execute_complete_original_analysis(extracted_params)
            
            # Format result
            formatted_result = self._format_result(result_data, params)
            
            print(f"[SUCCESS] TTL202 completed with original query. Records: {formatted_result['count']}")
            return formatted_result
            
        except Exception as e:
            print(f"[ERROR] TTL202 execution error: {e}")
            traceback.print_exc()
            
            return {
                'columns': ['Error_Type', 'Error_Message'],
                'data': [['TTL202_ERROR', str(e)]],
                'count': 1,
                'query': 'TTL202 execution failed',
                'error': True
            }
    
    def _execute_complete_original_analysis(self, params):
        """Execute complete original CURSOR C1 query from Forms 6i procedure"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Complete original CURSOR C1 query from Forms 6i procedure - FIXED bind variables
                complete_original_query = """
                SELECT SD_COMP_CODE, TO_CHAR(SD_DT, 'DD/MM/YYYY') SD_DT, SD_TXN_CODE||'-'||TO_CHAR(SD_NO) SD_TXN_NO, SD_TXN_TYPE, ITEM_NAME, ITEM_COST_LEVEL, ITEM_STK_YN_NUM, SD_DEL_LOCN_CODE, Z.LOCN_GROUP_CODE LOCN_GROUP_CODE, SD_ITEM_CODE, SD_GRADE_CODE, SD_CUST_CODE, SD_CUST_NAME, NVL(R.INVH_SM_CODE, S.CSRH_SM_CODE) SM_CODE, NVL(R.SM_NAME, S.SM_NAME) SM_NAME, SD_SALE_LOCN_CODE,C.AD_NAME CLASS_NAME, D.AD_NAME BRAND_NAME, E.AD_NAME MANF_NAME, F.AD_NAME TBU, G.AD_NAME CATG_NAME, H.AD_NAME RIM_SIZE, I.AD_NAME RAD_BIAS, J.AD_NAME PR_LINE, K.AD_NAME MANF_GRP, L.AD_NAME SALES_NAME, M.AD_NAME COS_NAME, N.AD_NAME TYRE_SIZE, O.AD_NAME OLD_CATG, P.AD_NAME GYR_VCODE, Q.AD_NAME GYR_IG, DECODE(SD_TXN_TYPE, 'INV', NVL(SD_QTY_BU,0)/IU_MAX_LOOSE_1, -1*(NVL(SD_QTY_BU,0)/IU_MAX_LOOSE_1)) QTY, DECODE(SD_TXN_TYPE, 'INV', NVL(SD_ITEM_VAL,0), -1*NVL(SD_ITEM_VAL,0)) ITEM_VAL, DECODE(SD_TXN_TYPE, 'INV', NVL(SD_DISC_VAL,0), -1*NVL(SD_DISC_VAL,0)) DISC_VAL, DECODE(SD_TXN_TYPE, 'INV', NVL(SD_VAT_VAL,0), -1*NVL(SD_VAT_VAL,0)) VAT_VAL, DECODE(SD_TXN_TYPE, 'INV', NVL(SD_EXP_VAL,0), -1*NVL(SD_EXP_VAL,0)) EXP_VAL, NVL(R.INVH_STATUS, NVL(S.CSRH_STATUS,0)) DOC_STATUS, SD_WAC COST, DECODE(SD_TXN_TYPE, 'INV', (NVL(SD_ITEM_VAL,0)-NVL(SD_DISC_VAL,0)+NVL(SD_VAT_VAL,0)), -1*(NVL(SD_ITEM_VAL,0)-NVL(SD_DISC_VAL,0)+NVL(SD_VAT_VAL,0))) SALES_VAL, DECODE(SD_TXN_TYPE, 'INV', (NVL(SD_ITEM_VAL,0)-NVL(SD_DISC_VAL,0)), -1*(NVL(SD_ITEM_VAL,0)-NVL(SD_DISC_VAL,0))) EXCL_VAT, TO_NUMBER(TO_CHAR(SD_DT,'YYYYMM')) YYYYMM, T.AD_NAME CUST_TYPE FROM OS_SALES_DETAIL, OM_ITEM, OM_ITEM_UOM, OM_CUSTOMER, (SELECT VSSV_VS_CODE, VSSV_CODE, VSSV_NAME FROM IM_VS_STATIC_VALUE ) A, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) C, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) D, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) E, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) F, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) G, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) H, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) I, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) J, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) K, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) L, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) M, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) N, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) O, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) P, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) Q, (SELECT INVH_SYS_ID, INVH_STATUS, INVH_SM_CODE, SM_NAME FROM OT_INVOICE_HEAD, OM_SALESMAN WHERE INVH_SM_CODE = SM_CODE) R, (SELECT CSRH_SYS_ID, CSRH_STATUS, CSRH_SM_CODE, SM_NAME FROM OT_CUST_SALE_RET_HEAD, OM_SALESMAN WHERE CSRH_SM_CODE = SM_CODE) S, (SELECT AD_ANLY_TYPE, AD_ANLY_NO, AD_CODE, AD_PARENT_CODE, AD_NAME FROM OM_ANALYSIS_DETAIL) T, (SELECT LOCN_CODE, LOCN_NAME, LOCN_GROUP_CODE FROM OM_LOCATION) Z WHERE SD_ITEM_ANLY_CODE_02 BETWEEN :M_FM_CUST_ANLY_02 AND :M_TO_CUST_ANLY_02 AND SD_ITEM_ANLY_CODE_04 BETWEEN :FM_ITEM_ANLY_12 AND :TO_ITEM_ANLY_12 AND SD_CUST_CODE BETWEEN :M_FM_SUB_ACNT AND :M_TO_SUB_ACNT AND SD_ITEM_CODE BETWEEN :M_FM_ITEM_CODE AND :M_TO_ITEM_CODE AND SD_COMP_CODE = :M_COMP_CODE AND SD_DT BETWEEN TO_DATE(:M_AS_OF_DT,'DD/MM/YYYY') AND TO_DATE(:M_TO_DT,'DD/MM/YYYY') AND SD_SALE_LOCN_CODE BETWEEN :M_FM_LOCN_CODE AND :M_TO_LOCN_CODE AND SD_SALE_LOCN_CODE IN (SELECT LUSR_LOCN_CODE FROM OM_LOCATION_USER WHERE LUSR_USER_ID = :M_USER_ID) AND SD_ITEM_CODE = ITEM_CODE AND ITEM_CODE = IU_ITEM_CODE AND ITEM_UOM_CODE = IU_UOM_CODE AND SD_DEL_LOCN_CODE = Z.LOCN_CODE AND SD_CUST_CODE = CUST_CODE AND ITEM_IG_CODE = A.VSSV_CODE(+) AND 'ITEM_GROUP' = A.VSSV_VS_CODE(+) AND 'ITEM' = C.AD_ANLY_TYPE(+) AND 1 = C.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_01 = C.AD_CODE(+) AND 'ITEM' = D.AD_ANLY_TYPE(+) AND 2 = D.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_02 = D.AD_CODE(+) AND 'ITEM' = E.AD_ANLY_TYPE(+) AND 3 = E.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_03 = E.AD_CODE(+) AND 'ITEM' = F.AD_ANLY_TYPE(+) AND 4 = F.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_04 = F.AD_CODE(+) AND 'ITEM' = G.AD_ANLY_TYPE(+) AND 5 = G.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_05 = G.AD_CODE(+) AND 'ITEM' = H.AD_ANLY_TYPE(+) AND 6 = H.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_06 = H.AD_CODE(+) AND 'ITEM' = I.AD_ANLY_TYPE(+) AND 7 = I.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_07 = I.AD_CODE(+) AND 'ITEM' = J.AD_ANLY_TYPE(+) AND 8 = J.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_08 = J.AD_CODE(+) AND 'ITEM' = K.AD_ANLY_TYPE(+) AND 9 = K.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_09 = K.AD_CODE(+) AND 'ITEM' = L.AD_ANLY_TYPE(+) AND 10 = L.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_10 = L.AD_CODE(+) AND 'ITEM' = M.AD_ANLY_TYPE(+) AND 11 = M.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_11 = M.AD_CODE(+) AND 'ITEM' = N.AD_ANLY_TYPE(+) AND 13 = N.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_13 = N.AD_CODE(+) AND 'ITEM' = O.AD_ANLY_TYPE(+) AND 15 = O.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_15 = O.AD_CODE(+) AND 'ITEM' = P.AD_ANLY_TYPE(+) AND 19 = P.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_19 = P.AD_CODE(+) AND 'ITEM' = Q.AD_ANLY_TYPE(+) AND 20 = Q.AD_ANLY_NO(+) AND ITEM_ANLY_CODE_20 = Q.AD_CODE(+) AND SD_H_SYS_ID = R.INVH_SYS_ID(+) AND SD_H_SYS_ID = S.CSRH_SYS_ID(+) AND 'CUSTOMER' = T.AD_ANLY_TYPE(+) AND 4 = T.AD_ANLY_NO(+) AND CUST_ANLY_CODE_04 = T.AD_CODE(+) ORDER BY ITEM_NAME
                """
                
                print(f"[INFO] Executing complete original query with 12 user parameters + 2 session variables...")
                
                # Extract parameters from the passed dictionary
                from_cust_anly_02 = params.get('from_cust_anly_02', '0')
                to_cust_anly_02 = params.get('to_cust_anly_02', 'ZZZZZ')
                from_item_anly_12 = params.get('from_item_anly_12', '0')
                to_item_anly_12 = params.get('to_item_anly_12', 'ZZZZZZ')
                from_cust_code = params.get('from_cust_code', '0')
                to_cust_code = params.get('to_cust_code', 'ZZZZ')
                from_item_code = params.get('from_item_code', '0')
                to_item_code = params.get('to_item_code', 'ZZZZZ')
                from_date = params.get('from_date', '01/01/2024')
                to_date = params.get('to_date', '31/12/2024')
                from_locn_code = params.get('from_locn_code', '0')
                to_locn_code = params.get('to_locn_code', 'ZZZZZZZ')
                comp_code = params.get('comp_code', 'TTM')
                user_id = params.get('user_id', 'SYSTEM')
                
                print(f"[DEBUG] Session variables: comp_code={comp_code}, user_id={user_id}")
                
                # Map additional GLOBAL variables from session if available
                global_comp_code = params.get('comp_code', comp_code)  # :GLOBAL.M_COMP_CODE
                global_user_id = params.get('user_id', user_id)        # :GLOBAL.M_USER_ID
                global_lang_code = params.get('lang_code', 'EN')       # :GLOBAL.M_LANG_CODE
                
                print(f"[DEBUG] GLOBAL variables mapped from Forms 6i:")
                print(f"  :GLOBAL.M_COMP_CODE -> {global_comp_code}")
                print(f"  :GLOBAL.M_USER_ID -> {global_user_id}")
                print(f"  :GLOBAL.M_LANG_CODE -> {global_lang_code}")
                
                # Parameter mapping - User parameters + Session variables (GLOBAL variables from Forms 6i)
                query_params = {
                    # User parameters from form
                    'M_FM_CUST_ANLY_02': from_cust_anly_02,
                    'M_TO_CUST_ANLY_02': to_cust_anly_02,
                    'FM_ITEM_ANLY_12': from_item_anly_12,
                    'TO_ITEM_ANLY_12': to_item_anly_12,
                    'M_FM_SUB_ACNT': from_cust_code,
                    'M_TO_SUB_ACNT': to_cust_code,
                    'M_FM_ITEM_CODE': from_item_code,
                    'M_TO_ITEM_CODE': to_item_code,
                    'M_AS_OF_DT': from_date,
                    'M_TO_DT': to_date,
                    'M_FM_LOCN_CODE': from_locn_code,
                    'M_TO_LOCN_CODE': to_locn_code,
                    # Session variables - Maps Forms 6i GLOBAL variables
                    # :GLOBAL.M_COMP_CODE -> session comp_code
                    'M_COMP_CODE': global_comp_code,
                    # :GLOBAL.M_USER_ID -> session user_id
                    'M_USER_ID': global_user_id
                }
                
                print(f"[DEBUG] All query parameters:")
                for key, value in query_params.items():
                    print(f"  {key} = {value}")
                
                print(f"[DEBUG] About to execute main query with {len(query_params)} parameters")
                
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
                'query': 'TTL202 main query execution failed',
                'error': True,
                'error_type': 'MAIN_QUERY_FAILURE'
            }
    
    def _format_result(self, data_results, params):
        """Format result for display"""
        columns = data_results.get('columns', [])
        data = data_results.get('data', [])
        
        return {
            'columns': [col.replace('_', ' ').title() for col in columns],
            'data': data,
            'count': len(data),
            'query': f'TTL202 Item Wise Sales Analysis - Complete Original Query',
            'parameters': params,
            'class_info': {
                'class_name': self.__class__.__name__,
                'version': self.version,
                'execution_method': 'Complete Original Query from Forms 6i'
            }
        }

# Alternative class names for compatibility
class TTL202(TTL202Report):
    """Alternative class name"""
    pass

class ReportProcessor(TTL202Report):
    """Generic class name"""
    pass

class Report(TTL202Report):
    """Simple class name"""
    pass

# Test locally
if __name__ == '__main__':
    test_params = {
        'from_cust_anly_02': '0',
        'to_cust_anly_02': 'ZZZZZ',
        'from_item_anly_12': '0',
        'to_item_anly_12': 'ZZZZZZ',
        'from_cust_code': '0',
        'to_cust_code': 'ZZZZ',
        'from_item_code': '0',
        'to_item_code': 'ZZZZZ',
        'GLOBAL': '0',
        'from_date': '01/01/2024',
        'to_date': '31/12/2024',
        'from_locn_code': '0',
        'to_locn_code': 'ZZZZZZZ'
    }
    
    try:
        report = TTL202Report()
        result = report.execute(test_params)
        print(f"[SUCCESS] Test completed with original query. Records: {result['count']}")
        print(f"[SUCCESS] Columns from original query: {len(result['columns'])}")
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        traceback.print_exc()