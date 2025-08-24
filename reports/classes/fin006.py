"""
FIN006 - Aging Analysis Report
File: reports/classes/FIN006.py

Converts Forms 6i POPULATE_Q2 procedure to Python class
Handles customer aging analysis with multiple time slots
"""

import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import traceback

class FIN006:
    """
    FIN006 - Customer Aging Analysis Report
    Converts Forms 6i procedure POPULATE_Q2 to Python class
    """
    
    def __init__(self):
        self.report_name = "Customer Aging Analysis"
        self.report_description = "Detailed aging analysis of customer outstanding amounts with configurable aging slots"
        
        # Initialize class variables (equivalent to Forms 6i variables)
        self.p_slot_1 = 0
        self.p_slot_2 = 0
        self.p_slot_3 = 0
        self.p_slot_4 = 0
        self.base_currency = 'INR'
        self.base_decimal = 2
        
        # Totals tracking
        self.reset_totals()
        
        # Setup logging
        self.logger = logging.getLogger("FIN006")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def reset_totals(self):
        """Reset all total variables"""
        self.tot_bal_amt = 0
        self.tot_unadj = 0
        self.tot_slot_1 = 0
        self.tot_slot_2 = 0
        self.tot_slot_3 = 0
        self.tot_slot_4 = 0
        self.tot_slot_5 = 0
        
        self.gtot_bal_amt = 0
        self.gtot_unadj = 0
        self.gtot_slot_1 = 0
        self.gtot_slot_2 = 0
        self.gtot_slot_3 = 0
        self.gtot_slot_4 = 0
        self.gtot_slot_5 = 0
    
    def execute_sql(self, sql, params=None):
        """Execute SQL query and return columns and rows"""
        try:
            from database import get_db_connection
            
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                
                # Get column names
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                
                # Fetch all rows
                rows = cursor.fetchall()
                
                return columns, rows
                
        except Exception as e:
            self.logger.error(f"ERROR SQL execution error: {str(e)}")
            self.logger.error(f"SQL: {sql}")
            self.logger.error(f"Params: {params}")
            raise
    
    def execute(self, params, config=None):
        """Main execution method - matches your existing system pattern"""
        try:
            self.logger.info("ROCKET Starting execution of FIN006 Customer Aging Analysis")
            self.logger.info(f"INFO Parameters: {params}")
            
            # Map GLOBAL variables from session if available (Forms 6i compatibility)
            global_comp_code = params.get('comp_code', 'TTM')       # :GLOBAL.M_COMP_CODE
            global_user_id = params.get('user_id', 'SYSTEM')       # :GLOBAL.M_USER_ID
            global_lang_code = params.get('lang_code', 'EN')       # :GLOBAL.M_LANG_CODE
            
            self.logger.info(f"INFO GLOBAL variables mapped from Forms 6i:")
            self.logger.info(f"  :GLOBAL.M_COMP_CODE -> {global_comp_code}")
            self.logger.info(f"  :GLOBAL.M_USER_ID -> {global_user_id}")
            self.logger.info(f"  :GLOBAL.M_LANG_CODE -> {global_lang_code}")
            
            # Update params with mapped GLOBAL variables
            params['comp_code'] = global_comp_code
            params['user_id'] = global_user_id
            
            # Step 1: Validate parameters
            if not self._validate_parameters(params):
                return {
                    'count': 1,
                    'columns': ['Status', 'Error'],
                    'data': [['ERROR', 'Missing required parameters. Check comp_code and date parameters.']],
                    'report_id': 'FIN006'
                }
            
            # Step 2: Preprocess parameters
            processed_params = self._preprocess_parameters(params)
            
            # Step 3: Get aging slot configuration
            self._get_aging_slots(processed_params)
            
            # Step 4: Get outstanding data with aging calculation
            aging_data = self._get_outstanding_aging_data(processed_params)
            
            # Step 5: Process aging buckets and calculate totals
            processed_data = self._process_aging_buckets(aging_data)
            
            # Step 6: Format results for display
            final_results = self._format_aging_results(processed_data)
            
            self.logger.info(f"SUCCESS FIN006 execution completed successfully")
            self.logger.info(f"CHART/INFO Records returned: {final_results.get('count', 0)}")
            
            return final_results
            
        except Exception as e:
            self.logger.error(f"ERROR FIN006 execution failed: {str(e)}")
            self.logger.error(f"STEP Traceback: {traceback.format_exc()}")
            
            # Return error result
            return {
                'count': 1,
                'columns': ['Status', 'Error', 'Traceback'],
                'data': [['ERROR', str(e), traceback.format_exc()[:500]]],
                'report_id': 'FIN006'
            }
    
    def _validate_parameters(self, params):
        """Validate required parameters"""
        required = ['comp_code']
        
        for param in required:
            if not params.get(param):
                self.logger.error(f"Missing required parameter: {param}")
                return False
        
        # Check for date parameters (either 'date' or 'as_of_date')
        has_date = params.get('date') or params.get('as_of_date')
        if not has_date:
            self.logger.error("Missing required parameter: date (or as_of_date)")
            return False
        
        # Validate date format for whichever date parameter exists
        try:
            date_value = params.get('date') or params.get('as_of_date')
            if date_value and date_value != 'ZZZZZZ':
                datetime.strptime(date_value, '%d/%m/%Y')
        except ValueError as e:
            self.logger.error(f"Invalid date format: {e}")
            return False
        
        return True
    
    def _preprocess_parameters(self, params):
        """Preprocess parameters for aging analysis"""
        processed = params.copy()
        
        # Set defaults for aging parameters
        processed['base_or_for'] = processed.get('base_or_for', 'B')
        processed['age_dr_cr'] = processed.get('age_dr_cr', 'D')
        processed['doc_or_due'] = processed.get('doc_or_due', 'D')
        
        # Set customer code defaults
        if not processed.get('from_cust_main_acnt_code'):
            processed['from_cust_main_acnt_code'] = '0'
        if not processed.get('to_cust_main_acnt_code'):
            processed['to_cust_main_acnt_code'] = 'ZZZZZZ'
        if not processed.get('from_cust_code'):
            processed['from_cust_code'] = '0'
        if not processed.get('to_cust_code'):
            processed['to_cust_code'] = 'ZZZZZZ'
        
        # Set aging slots from parameters (from the form)
        processed['aging_slot_1'] = int(processed.get('aging_slot_1', 30))
        processed['aging_slot_2'] = int(processed.get('aging_slot_2', 60))
        processed['aging_slot_3'] = int(processed.get('aging_slot_3', 90))
        processed['aging_slot_4'] = int(processed.get('aging_slot_4', 120))
        
        # Use 'date' parameter instead of 'as_of_date' for consistency with form
        if 'date' in processed and 'as_of_date' not in processed:
            processed['as_of_date'] = processed['date']
        
        return processed
    
    def _get_aging_slots(self, params):
        """Get aging slot configuration"""
        self.logger.info("CHART/INFO Setting aging slot configuration")
        
        # Use aging slots from parameters (from the form)
        self.p_slot_1 = params.get('aging_slot_1', 30)
        self.p_slot_2 = params.get('aging_slot_2', 60)
        self.p_slot_3 = params.get('aging_slot_3', 90)
        self.p_slot_4 = params.get('aging_slot_4', 120)
        
        self.logger.info(f"CHART/INFO Aging slots: {self.p_slot_1}, {self.p_slot_2}, {self.p_slot_3}, {self.p_slot_4}")
    
    def _get_outstanding_aging_data(self, params):
        """Get outstanding data with aging calculation - PRODUCTION SQL QUERY"""
        self.logger.info("CHART/INFO Fetching outstanding aging data from production tables")
        
        # PRODUCTION SQL QUERY - Uses your actual database tables
        sql = """
        SELECT  A.OST_COMP_CODE AS COMP_CODE,
                A.OST_MAIN_ACNT_CODE AS MAIN_ACNT_CODE,
                A.OST_SUB_ACNT_CODE AS SUB_ACNT_CODE,
                SUB_ACNT_NAME AS CUST_NAME,
                30 AS TERM_DAYS,
                NVL(Y.CREDIT_DAYS,0) AS CREDIT_DAYS,
                DECODE(:base_or_for,'B',PARA_VALUE,
                    NVL(A.OST_CURR_CODE,PARA_VALUE)) AS CURR_CODE,
                (DECODE(:base_or_for,'B',
                    DECODE(A.OST_TYPE,'P',A.OST_LC_ORG_AMT,A.OST_LC_AMT),
                    DECODE(A.OST_TYPE,'P',A.OST_FC_ORG_AMT,A.OST_FC_AMT))
                    - DECODE(:base_or_for,'B',
                    SUM(NVL(B.OST_LC_AMT,0)),SUM(NVL(B.OST_FC_AMT,0)))) *
                    DECODE(A.OST_DRCR_FLAG,'D',1,-1) AS BAL_AMT,
                ROUND((TO_DATE(:as_of_date, 'DD/MM/YYYY') - A.OST_DOC_DT)) AS DAYS
        FROM    FM_COMPANY, FM_SUB_ACCOUNT, FM_MAIN_ACCOUNT, FP_PARAMETER,
                FT_OS A, FT_OS B,
                (SELECT CPT_CUST_CODE, NVL(PTD_CREDIT_DAYS,0) AS CREDIT_DAYS
                 FROM   OM_CUST_PAYMENT_TERM, OM_PAYMENT_TERM_DETAIL
                 WHERE  CPT_TERM_CODE = PTD_PT_CODE
                 AND    NVL(CPT_FRZ_FLAG_NUM,1) = 2) Y
        WHERE   A.OST_COMP_CODE = :comp_code
        AND     A.OST_MAIN_ACNT_CODE BETWEEN :from_cust_main_acnt_code 
                AND :to_cust_main_acnt_code
        AND     A.OST_SUB_ACNT_CODE BETWEEN :from_cust_code 
                AND :to_cust_code
        AND     A.OST_DOC_DT <= TO_DATE(:as_of_date, 'DD/MM/YYYY')
        AND     (((NVL(A.OST_LAST_MATCH_DT,A.OST_DOC_DT)) 
                > TO_DATE(:as_of_date, 'DD/MM/YYYY') AND NVL(A.OST_TYPE,'Z') = 'P') 
                OR (NVL(A.OST_LC_AMT,0) != NVL(A.OST_LC_ADJ_AMT,0)) 
                OR (NVL(A.OST_FC_AMT,0) != NVL(A.OST_FC_ADJ_AMT,0)))
        AND     NVL(A.OST_TYPE,'Z') IN ('P','Z')
        AND     A.OST_MAIN_ACNT_CODE = MAIN_ACNT_CODE
        AND     MAIN_ACNT_CATG IN (SELECT SUBSTR(PARA_VALUE,1,2) 
                FROM FP_PARAMETER
                WHERE PARA_ID = 'AGE.CATEGORY' 
                AND SUBSTR(PARA_VALUE,4,1) = 'D')
        AND     PARA_ID = 'BASE.CURR'
        AND     B.OST_REF_KEY_NO (+) = A.OST_KEY_NO
        AND     B.OST_TYPE (+) = 'R'
        AND     B.OST_DOC_DT (+) <= TO_DATE(:as_of_date, 'DD/MM/YYYY')
        AND     COMP_CODE = :comp_code
        AND     SUB_ACNT_CODE = A.OST_SUB_ACNT_CODE
        AND     Y.CPT_CUST_CODE(+) = NVL(A.OST_SUB_ACNT_CODE,'*')
        GROUP BY A.OST_COMP_CODE, COMP_NAME, A.OST_MAIN_ACNT_CODE,
                A.OST_SUB_ACNT_CODE, SUB_ACNT_NAME, A.OST_CURR_CODE, PARA_VALUE,
                A.OST_LC_ORG_AMT, A.OST_FC_ORG_AMT,
                A.OST_TYPE, A.OST_LC_AMT, A.OST_FC_AMT,
                A.OST_DRCR_FLAG, A.OST_DOC_DT, A.OST_DUE_DT,
                A.OST_TRAN_CODE, A.OST_DOC_NO,
                A.OST_REF_TRAN_CODE, A.OST_REF_DOC_NO,
                A.OST_REF_DOC_DT, A.OST_KEY_NO, Y.CREDIT_DAYS
        HAVING  (NVL(A.OST_LC_AMT,0) - SUM(NVL(B.OST_LC_AMT,0))) != 0
        
        UNION ALL
        
        SELECT  A.OST_COMP_CODE AS COMP_CODE,
                A.OST_MAIN_ACNT_CODE AS MAIN_ACNT_CODE,
                A.OST_SUB_ACNT_CODE AS SUB_ACNT_CODE,
                SUB_ACNT_NAME AS CUST_NAME,
                30 AS TERM_DAYS,
                NVL(Y.CREDIT_DAYS,0) AS CREDIT_DAYS,
                DECODE(:base_or_for,'B',PARA_VALUE,
                    NVL(A.OST_CURR_CODE,PARA_VALUE)) AS CURR_CODE,
                (DECODE(:base_or_for,'B',
                    DECODE(A.OST_TYPE,'P',A.OST_LC_ORG_AMT,A.OST_LC_AMT),
                    DECODE(A.OST_TYPE,'P',A.OST_FC_ORG_AMT,A.OST_FC_AMT))) *
                    DECODE(A.OST_DRCR_FLAG,'D',1,-1) AS BAL_AMT,
                ROUND((TO_DATE(:as_of_date, 'DD/MM/YYYY') - A.OST_DOC_DT)) AS DAYS
        FROM    FM_COMPANY, FM_MAIN_ACCOUNT, FM_SUB_ACCOUNT, FP_PARAMETER, FT_OS A,
                (SELECT CPT_CUST_CODE, NVL(PTD_CREDIT_DAYS,0) AS CREDIT_DAYS
                 FROM   OM_CUST_PAYMENT_TERM, OM_PAYMENT_TERM_DETAIL
                 WHERE  CPT_TERM_CODE = PTD_PT_CODE
                 AND    NVL(CPT_FRZ_FLAG_NUM,1) = 2) Y
        WHERE   A.OST_COMP_CODE = :comp_code
        AND     A.OST_MAIN_ACNT_CODE BETWEEN :from_cust_main_acnt_code 
                AND :to_cust_main_acnt_code
        AND     A.OST_SUB_ACNT_CODE BETWEEN :from_cust_code 
                AND :to_cust_code
        AND     A.OST_DOC_DT <= TO_DATE(:as_of_date, 'DD/MM/YYYY')
        AND     NVL(A.OST_TYPE,'Z') = 'R'
        AND     A.OST_REF_DOC_DT > TO_DATE(:as_of_date, 'DD/MM/YYYY')
        AND     A.OST_MAIN_ACNT_CODE = MAIN_ACNT_CODE
        AND     MAIN_ACNT_CATG IN (SELECT SUBSTR(PARA_VALUE,1,2) 
                FROM FP_PARAMETER
                WHERE PARA_ID = 'AGE.CATEGORY' 
                AND SUBSTR(PARA_VALUE,4,1) = 'D')
        AND     PARA_ID = 'BASE.CURR'
        AND     COMP_CODE = :comp_code
        AND     SUB_ACNT_CODE = A.OST_SUB_ACNT_CODE
        AND     Y.CPT_CUST_CODE(+) = NVL(A.OST_SUB_ACNT_CODE,'*')
        GROUP BY A.OST_COMP_CODE, COMP_NAME, A.OST_MAIN_ACNT_CODE,
                A.OST_SUB_ACNT_CODE, SUB_ACNT_NAME, A.OST_CURR_CODE,
                PARA_VALUE, A.OST_LC_ORG_AMT, A.OST_FC_ORG_AMT,
                A.OST_TYPE, A.OST_LC_AMT, A.OST_FC_AMT,
                A.OST_DRCR_FLAG, A.OST_DOC_DT, A.OST_DUE_DT,
                A.OST_TRAN_CODE, A.OST_DOC_NO,
                A.OST_REF_TRAN_CODE, A.OST_REF_DOC_NO,
                A.OST_REF_DOC_DT, A.OST_KEY_NO, Y.CREDIT_DAYS
        ORDER BY 1,2,3,4
        """
        
        # Parameters for the production query
        query_params = {
            'comp_code': params['comp_code'],
            'as_of_date': params.get('date', params.get('as_of_date')),
            'base_or_for': params['base_or_for'],
            'from_cust_main_acnt_code': params['from_cust_main_acnt_code'],
            'to_cust_main_acnt_code': params['to_cust_main_acnt_code'],
            'from_cust_code': params['from_cust_code'],
            'to_cust_code': params['to_cust_code']
        }
        
        columns, rows = self.execute_sql(sql, query_params)
        self.logger.info(f"CHART/INFO Retrieved {len(rows)} outstanding records from production tables")
        return {'columns': columns, 'data': rows}
    
    def _get_currency_decimal(self, curr_code):
        """Get currency decimal places"""
        try:
            sql = "SELECT CURR_DECIMAL FROM FM_CURRENCY WHERE CURR_CODE = :curr_code"
            columns, rows = self.execute_sql(sql, {'curr_code': curr_code})
            
            if rows:
                return rows[0][0] or 2
            else:
                return 2
                
        except:
            return 2
    
    def _get_credit_limit(self, comp_code, cust_code):
        """Get customer credit limit"""
        try:
            sql = """
            SELECT NVL(CCO_CREDIT_LIMIT,0) + NVL(CCO_EXPOSURE_LIMIT,0)
            FROM   OM_CUST_COMP
            WHERE  CCO_COMP_CODE = :comp_code
            AND    CCO_CUST_CODE = :cust_code
            """
            
            columns, rows = self.execute_sql(sql, {
                'comp_code': comp_code,
                'cust_code': cust_code
            })
            
            if rows:
                return rows[0][0] or 0
            else:
                return 50000.00  # Default demo value
                
        except:
            return 50000.00  # Default demo value
    
    def _process_aging_buckets(self, aging_data):
        """Process aging data into buckets (main business logic)"""
        self.logger.info("LINK Processing aging buckets")
        
        result_data = []
        current_group = None
        self.reset_totals()
        
        for row in aging_data['data']:
            # Extract row data
            comp_code = row[0]
            main_acnt_code = row[1]
            sub_acnt_code = row[2]
            cust_name = row[3]
            term_days = row[4]
            credit_days = row[5]
            curr_code = row[6]
            bal_amt = float(row[7]) if row[7] else 0
            days = int(row[8]) if row[8] else 0
            
            # Create group key
            group_key = f"{main_acnt_code}|{sub_acnt_code}|{curr_code}"
            
            # Check if we need to process previous group
            if current_group and current_group != group_key:
                # Add previous group summary
                self._add_customer_summary(result_data, current_group_data)
                self.reset_totals()
            
            # Initialize new group if needed
            if current_group != group_key:
                current_group = group_key
                current_group_data = {
                    'comp_code': comp_code,
                    'main_acnt_code': main_acnt_code,
                    'sub_acnt_code': sub_acnt_code,
                    'cust_name': cust_name,
                    'term_days': str(credit_days) if credit_days else str(term_days),
                    'curr_code': curr_code,
                    'credit_limit': self._get_credit_limit(comp_code, sub_acnt_code)
                }
            
            # Calculate aging slots based on days
            slot_1_amt = bal_amt if days > self.p_slot_4 else 0  # Above 120 days
            slot_2_amt = bal_amt if self.p_slot_3 < days <= self.p_slot_4 else 0  # 90-120 days
            slot_3_amt = bal_amt if self.p_slot_2 < days <= self.p_slot_3 else 0  # 60-90 days
            slot_4_amt = bal_amt if self.p_slot_1 < days <= self.p_slot_2 else 0  # 30-60 days
            slot_5_amt = bal_amt if days <= self.p_slot_1 else 0  # Up to 30 days
            
            # Calculate unadjusted amount (negative balances)
            unadj_amt = bal_amt if bal_amt < 0 else 0
            
            # Add to totals
            self.tot_bal_amt += bal_amt
            self.tot_unadj += unadj_amt
            self.tot_slot_1 += slot_1_amt
            self.tot_slot_2 += slot_2_amt
            self.tot_slot_3 += slot_3_amt
            self.tot_slot_4 += slot_4_amt
            self.tot_slot_5 += slot_5_amt
            
            # Add to grand totals
            self.gtot_bal_amt += bal_amt
            self.gtot_unadj += unadj_amt
            self.gtot_slot_1 += slot_1_amt
            self.gtot_slot_2 += slot_2_amt
            self.gtot_slot_3 += slot_3_amt
            self.gtot_slot_4 += slot_4_amt
            self.gtot_slot_5 += slot_5_amt
        
        # Add final group
        if current_group:
            self._add_customer_summary(result_data, current_group_data)
        
        # Add grand total
        self._add_grand_total(result_data)
        
        return result_data
    
    def _add_customer_summary(self, result_data, group_data):
        """Add customer summary row"""
        decimal_places = self._get_currency_decimal(group_data['curr_code'])
        
        summary_row = {
            'MAIN_AC': group_data['main_acnt_code'],
            'SUB_AC': group_data['sub_acnt_code'],
            'SUB_AC_DESC': group_data['cust_name'],
            'TERM_DAYS': group_data['term_days'],
            'CURR': group_data['curr_code'],
            'NET_VAL': round(self.tot_bal_amt, decimal_places),
            'SLOT_1': round(self.tot_slot_1, decimal_places),
            'SLOT_2': round(self.tot_slot_2, decimal_places),
            'SLOT_3': round(self.tot_slot_3, decimal_places),
            'SLOT_4': round(self.tot_slot_4, decimal_places),
            'SLOT_5': round(self.tot_slot_5, decimal_places),
            'CR_LIMIT': group_data['credit_limit'],
            'ROW_TYPE': 'CUSTOMER'
        }
        
        result_data.append(summary_row)
    
    def _add_grand_total(self, result_data):
        """Add grand total row"""
        total_row = {
            'MAIN_AC': '',
            'SUB_AC': '',
            'SUB_AC_DESC': 'Grand Total',
            'TERM_DAYS': '',
            'CURR': self.base_currency,
            'NET_VAL': round(self.gtot_bal_amt, 2),
            'SLOT_1': round(self.gtot_slot_1, 2),
            'SLOT_2': round(self.gtot_slot_2, 2),
            'SLOT_3': round(self.gtot_slot_3, 2),
            'SLOT_4': round(self.gtot_slot_4, 2),
            'SLOT_5': round(self.gtot_slot_5, 2),
            'CR_LIMIT': 0,
            'ROW_TYPE': 'TOTAL'
        }
        
        result_data.append(total_row)
    
    def _format_aging_results(self, processed_data):
        """Format results for display"""
        self.logger.info("TOOL Formatting aging results")
        
        if not processed_data:
            return {
                'columns': ['Message'],
                'data': [['No aging data found for the selected criteria']],
                'count': 1
            }
        
        # Define columns with consistent aging slot headers (for RPT_PARAMS matching)
        # Use standardized column names that match the RPT_PARAMS configuration
        columns = [
            'MAIN_AC', 'SUB_AC', 'SUB_AC_DESC', 'TERM_DAYS', 'CURR',
            'ABOVE_120_DAYS', '90_TO_120_DAYS', '60_TO_90_DAYS', '30_TO_60_DAYS', 'UPTO_30_DAYS', 
            'NET_VAL', 'CR_LIMIT'
        ]
        
        # Convert data to list format
        data_rows = []
        for row in processed_data:
            data_row = [
                row['MAIN_AC'],
                row['SUB_AC'],
                row['SUB_AC_DESC'],
                row['TERM_DAYS'],
                row['CURR'],
                row['SLOT_1'],
                row['SLOT_2'],
                row['SLOT_3'],
                row['SLOT_4'],
                row['SLOT_5'],
                row['NET_VAL'],
                row['CR_LIMIT']
            ]
            data_rows.append(data_row)
        
        # Add metadata for your system
        return {
            'columns': columns,
            'data': data_rows,
            'count': len(data_rows),
            'query': f'FIN006 Customer Aging Analysis with slots: {self.p_slot_1}, {self.p_slot_2}, {self.p_slot_3}, {self.p_slot_4}',
            'report_id': 'FIN006',
            'is_modular': True,
            'report_type': 'CLASS',
            'aging_config': {
                'slot_1': self.p_slot_1,
                'slot_2': self.p_slot_2,
                'slot_3': self.p_slot_3,
                'slot_4': self.p_slot_4
            },
            'summary': {
                'total_customers': len([row for row in processed_data if row['ROW_TYPE'] == 'CUSTOMER']),
                'total_outstanding': round(self.gtot_bal_amt, 2),
                'aging_slots': f"{self.p_slot_1}, {self.p_slot_2}, {self.p_slot_3}, {self.p_slot_4} days"
            }
        }