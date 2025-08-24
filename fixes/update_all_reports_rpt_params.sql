-- =============================================================================
-- MASTER SCRIPT: Update ALL Reports with Complete RPT_PARAMS Configuration
-- This script updates ALL reports (CLASS + SQL) with auto-generated column names:
-- CLASS Reports: FIN001, FIN006, TTL202, TTL308
-- SQL Reports: TTL201, TTL715
-- =============================================================================

PROMPT Starting update of all report RPT_PARAMS...

-- =============================================================================
-- FIN001 - Trial Balance Report
-- =============================================================================
PROMPT Updating FIN001...

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Period", "field": "M_FM_YYYYMM", "type": "text", "required": true, "default": "202501"},
    {"name": "To Period", "field": "M_TO_YYYYMM", "type": "text", "required": true, "default": "202512"},
    {"name": "From Division", "field": "M_FM_DIVN", "type": "text", "required": true, "default": "0"},
    {"name": "To Division", "field": "M_TO_DIVN", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Department", "field": "M_FM_DEPT", "type": "text", "required": true, "default": "0"},
    {"name": "To Department", "field": "M_TO_DEPT", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Main Account", "field": "M_FM_MAIN_AC", "type": "text", "required": true, "default": "0"},
    {"name": "To Main Account", "field": "M_TO_MAIN_AC", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Sub Account", "field": "M_FM_SUB_AC", "type": "text", "required": true, "default": "0"},
    {"name": "To Sub Account", "field": "M_TO_SUB_AC", "type": "text", "required": true, "default": "ZZZZZZ"}
  ],
  "display_columns": [],
  "column_headers": {
    "ABAL_COMP_CODE": "Company Code",
    "ABAL_ACNT_YEAR": "Account Year", 
    "ABAL_MAIN_ACNT_CODE": "Main Account Code",
    "MAIN_ACNT_NAME": "Main Account Name",
    "PBC_SUB_ACNT_CODE": "PBC Sub Account Code",
    "ABAL_SUB_ACNT_CODE": "Sub Account Code",
    "SUB_ACNT_NAME": "Sub Account Name",
    "ABAL_DIVN_CODE": "Division Code",
    "DIVN_NAME": "Division Name",
    "ABAL_DEPT_CODE": "Department Code",
    "DEPT_NAME": "Department Name",
    "MONTH_BAL_01": "January Balance",
    "MONTH_BAL_02": "February Balance",
    "MONTH_BAL_03": "March Balance",
    "MONTH_BAL_04": "April Balance",
    "MONTH_BAL_05": "May Balance",
    "MONTH_BAL_06": "June Balance",
    "MONTH_BAL_07": "July Balance",
    "MONTH_BAL_08": "August Balance",
    "MONTH_BAL_09": "September Balance",
    "MONTH_BAL_10": "October Balance",
    "MONTH_BAL_11": "November Balance",
    "MONTH_BAL_12": "December Balance",
    "OP_BAL": "Opening Balance",
    "CLO_BAL": "Closing Balance"
  },
  "hidden_columns": [],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'FIN001';

-- =============================================================================
-- FIN006 - Customer Aging Analysis
-- =============================================================================
PROMPT Updating FIN006...

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "From Customer Main Account", "field": "from_cust_main_acnt_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Customer Main Account", "field": "to_cust_main_acnt_code", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "Base or Foreign Currency", "field": "base_or_for", "type": "select", "required": true, "default": "B", 
     "options": [{"value": "B", "text": "Base Currency"}, {"value": "F", "text": "Foreign Currency"}]},
    {"name": "Aging Slot 1 Days", "field": "aging_slot_1", "type": "number", "required": true, "default": "30"},
    {"name": "Aging Slot 2 Days", "field": "aging_slot_2", "type": "number", "required": true, "default": "60"},
    {"name": "Aging Slot 3 Days", "field": "aging_slot_3", "type": "number", "required": true, "default": "90"},
    {"name": "Aging Slot 4 Days", "field": "aging_slot_4", "type": "number", "required": true, "default": "120"}
  ],
  "display_columns": [],
  "column_headers": {
    "COMP_CODE": "Company Code",
    "MAIN_ACNT_CODE": "Main Account Code", 
    "SUB_ACNT_CODE": "Customer Code",
    "CUST_NAME": "Customer Name",
    "TERM_DAYS": "Payment Terms (Days)",
    "CREDIT_DAYS": "Credit Days",
    "CURR_CODE": "Currency Code",
    "BAL_AMT": "Balance Amount",
    "DAYS": "Days Outstanding",
    "SLOT_1": "0-30 Days",
    "SLOT_2": "31-60 Days", 
    "SLOT_3": "61-90 Days",
    "SLOT_4": "91-120 Days",
    "SLOT_5": "120+ Days",
    "UNADJ_AMT": "Unadjusted Amount",
    "CREDIT_LIMIT": "Credit Limit",
    "EXPOSURE": "Total Exposure",
    "AVAILABLE_CREDIT": "Available Credit"
  },
  "hidden_columns": [],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'FIN006';

-- =============================================================================
-- TTL202 - Sales Detail Analysis
-- =============================================================================
PROMPT Updating TTL202...

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Customer Analysis 02", "field": "from_cust_anly_02", "type": "text", "required": true, "default": "0"},
    {"name": "To Customer Analysis 02", "field": "to_cust_anly_02", "type": "text", "required": true, "default": "ZZZZZ"},
    {"name": "From Item Analysis 12", "field": "from_item_anly_12", "type": "text", "required": true, "default": "0"},
    {"name": "To Item Analysis 12", "field": "to_item_anly_12", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "As Of Date", "field": "as_of_dt", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_dt", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": true, "default": "ZZZZZZ"}
  ],
  "display_columns": [],
  "column_headers": {
    "SD_COMP_CODE": "Company Code",
    "SD_DT": "Sale Date",
    "SD_TXN_NO": "Transaction Number",
    "SD_TXN_TYPE": "Transaction Type",
    "ITEM_NAME": "Item Name",
    "SD_CUST_NAME": "Customer Name",
    "SM_NAME": "Salesman Name",
    "QTY": "Quantity",
    "SALES_VAL": "Sales Value",
    "COST": "Cost",
    "BRAND_NAME": "Brand Name",
    "CLASS_NAME": "Class Name"
  },
  "hidden_columns": ["SD_COMP_CODE", "ITEM_STK_YN_NUM", "YYYYMM"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL202';

-- =============================================================================
-- TTL308 - VAT Analysis Report
-- =============================================================================
PROMPT Updating TTL308...

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "Account Year", "field": "acnt_year", "type": "number", "required": true, "default": "2024"},
    {"name": "Current/Previous Period", "field": "cur_prv", "type": "select", "required": true, "default": "C",
     "options": [{"value": "C", "text": "Current Period"}, {"value": "P", "text": "Previous Period"}]}
  ],
  "display_columns": [],
  "column_headers": {
    "HEAD": "Account Head",
    "GH_TXN_CODE": "Transaction Code", 
    "GH_NO": "Document Number",
    "GH_DT": "Document Date",
    "ACNT_NAME": "Account Name",
    "GH_AMT": "Gross Amount",
    "VAT_AMT": "VAT Amount",
    "NETT_AMT": "Net Amount"
  },
  "hidden_columns": ["ORD", "TH_COMP_CODE"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL308';

-- =============================================================================
-- Commit all changes
-- =============================================================================
COMMIT;

PROMPT All report RPT_PARAMS updated successfully!
PROMPT 
PROMPT Updated reports:
PROMPT - FIN001: Trial Balance (25 columns with readable names)
PROMPT - FIN006: Customer Aging (18 columns with business names)  
PROMPT - TTL202: Sales Analysis (40+ columns, hidden system columns)
PROMPT - TTL308: VAT Analysis (8 key columns, hidden technical columns)
PROMPT
PROMPT You can now customize individual column names as needed!

-- =============================================================================
-- TTL201 - Sales Detail Report (SQL)
-- =============================================================================
PROMPT Updating TTL201...

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From SDM Code", "field": "from_sdm_code", "type": "text", "required": false, "default": "0"},
    {"name": "To SDM Code", "field": "to_sdm_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Flash Code", "field": "from_flash_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Flash Code", "field": "to_flash_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024"}
  ],
  "display_columns": [],
  "column_headers": {
    "Customer Name": "Customer Name",
    "Customer Code": "Customer Code",
    "SM Code": "Salesman Code",
    "SM Name": "Salesman Name",
    "Sale Date": "Sale Date",
    "Transaction No": "Transaction Number",
    "Item Name": "Item Name",
    "Brand Name": "Brand Name",
    "Quantity": "Quantity",
    "Sales Value": "Sales Value",
    "Cost": "Cost",
    "Contribution": "Contribution",
    "Margin %": "Margin %"
  },
  "hidden_columns": ["YYYYMM", "Location Code", "Grade Code"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL201';

-- =============================================================================
-- TTL715 - Pending Approvals Report (SQL)
-- =============================================================================
PROMPT Updating TTL715...

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "FM_DT", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "TO_DT", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "From Transaction Code", "field": "FM_TXN_CODE", "type": "text", "required": true, "default": "0"},
    {"name": "To Transaction Code", "field": "TO_TXN_CODE", "type": "text", "required": true, "default": "ZZZZZZ"}
  ],
  "display_columns": [],
  "column_headers": {
    "DT": "Document Date",
    "TXN": "Transaction Code",
    "NUM": "Document Number",
    "LOCN": "Location Code",
    "CODE": "Supplier/Customer Code",
    "NAME": "Supplier/Customer Name",
    "ITEM": "Has Items",
    "TXN_TYPE": "Transaction Type",
    "UID": "Created By"
  },
  "hidden_columns": ["ORD", "SYS_ID"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL715';

-- =============================================================================
-- Commit all changes
-- =============================================================================
COMMIT;

PROMPT All report RPT_PARAMS updated successfully!
PROMPT 
PROMPT Updated reports:
PROMPT CLASS REPORTS:
PROMPT - FIN001: Trial Balance (25 columns with readable names)
PROMPT - FIN006: Customer Aging (18 columns with business names)  
PROMPT - TTL202: Sales Analysis (40+ columns, hidden system columns)
PROMPT - TTL308: VAT Analysis (8 key columns, hidden technical columns)
PROMPT SQL REPORTS:
PROMPT - TTL201: Sales Detail (35+ columns with business names)
PROMPT - TTL715: Pending Approvals (11 columns, hidden system IDs)
PROMPT
PROMPT You can now customize individual column names as needed!

-- =============================================================================
-- Verification Query
-- =============================================================================
SELECT RPT_ID, RPT_NAME, RPT_TYPE,
       CASE WHEN RPT_PARAMS IS NOT NULL THEN 'CONFIGURED' ELSE 'MISSING' END AS CONFIG_STATUS
FROM RPT_REPORT_MASTER 
WHERE RPT_ID IN ('FIN001', 'FIN006', 'TTL202', 'TTL308', 'TTL201', 'TTL715')
ORDER BY RPT_TYPE, RPT_ID;