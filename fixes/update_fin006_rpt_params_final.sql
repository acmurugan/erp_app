-- =============================================================================
-- FINAL FIN006 RPT_PARAMS UPDATE - Customer Aging Analysis
-- Updated: 24/08/2025 by Claude Code
-- Changes:
-- 1. Changed from_date to as_of_date parameter (more intuitive for aging reports)
-- 2. Column headers match actual FIN006.py output columns
-- 3. Session variables (comp_code, user_id) excluded from parameter form
-- 4. Proper display_columns configuration for column filtering
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {
      "name": "As of Date", 
      "field": "as_of_date", 
      "type": "date", 
      "required": true, 
      "default": "24/08/2025",
      "description": "Report date for aging analysis calculation"
    },
    {
      "name": "From Customer Main Account", 
      "field": "from_cust_main_acnt_code", 
      "type": "text", 
      "required": true, 
      "default": "0",
      "description": "Starting main account code range"
    },
    {
      "name": "To Customer Main Account", 
      "field": "to_cust_main_acnt_code", 
      "type": "text", 
      "required": true, 
      "default": "ZZZZZZ",
      "description": "Ending main account code range"
    },
    {
      "name": "From Customer Code", 
      "field": "from_cust_code", 
      "type": "text", 
      "required": true, 
      "default": "0",
      "description": "Starting customer code range"
    },
    {
      "name": "To Customer Code", 
      "field": "to_cust_code", 
      "type": "text", 
      "required": true, 
      "default": "ZZZZZZ",
      "description": "Ending customer code range"
    },
    {
      "name": "Base or Foreign Currency", 
      "field": "base_or_for", 
      "type": "select", 
      "required": true, 
      "default": "B", 
      "options": [
        {"value": "B", "text": "Base Currency"}, 
        {"value": "F", "text": "Foreign Currency"}
      ],
      "description": "Currency basis for amounts"
    },
    {
      "name": "Aging Slot 1 Days", 
      "field": "aging_slot_1", 
      "type": "number", 
      "required": true, 
      "default": "30",
      "description": "First aging period in days"
    },
    {
      "name": "Aging Slot 2 Days", 
      "field": "aging_slot_2", 
      "type": "number", 
      "required": true, 
      "default": "60",
      "description": "Second aging period in days"
    },
    {
      "name": "Aging Slot 3 Days", 
      "field": "aging_slot_3", 
      "type": "number", 
      "required": true, 
      "default": "90",
      "description": "Third aging period in days"
    },
    {
      "name": "Aging Slot 4 Days", 
      "field": "aging_slot_4", 
      "type": "number", 
      "required": true, 
      "default": "120",
      "description": "Fourth aging period in days"
    }
  ],
  "display_columns": [
    "MAIN_AC", 
    "SUB_AC", 
    "SUB_AC_DESC", 
    "TERM_DAYS", 
    "CURR", 
    "ABOVE_120_DAYS", 
    "90_TO_120_DAYS", 
    "60_TO_90_DAYS", 
    "30_TO_60_DAYS", 
    "UPTO_30_DAYS", 
    "NET_VAL", 
    "CR_LIMIT"
  ],
  "column_headers": {
    "MAIN_AC": "Main Account",
    "SUB_AC": "Customer Code", 
    "SUB_AC_DESC": "Customer Name",
    "TERM_DAYS": "Payment Terms (Days)",
    "CURR": "Currency",
    "ABOVE_120_DAYS": "Above 120 Days",
    "90_TO_120_DAYS": "90-120 Days",
    "60_TO_90_DAYS": "60-90 Days", 
    "30_TO_60_DAYS": "30-60 Days",
    "UPTO_30_DAYS": "Up to 30 Days",
    "NET_VAL": "Net Outstanding",
    "CR_LIMIT": "Credit Limit"
  },
  "hidden_columns": [],
  "ui_config": {
    "date_format": "DD/MM/YYYY", 
    "theme": "bootstrap",
    "report_title": "Customer Aging Analysis",
    "show_totals": true,
    "export_formats": ["HTML", "EXCEL", "PDF"]
  },
  "global_variables": {
    "comp_code": {
      "forms6i_mapping": ":GLOBAL.M_COMP_CODE", 
      "web_mapping": "session[comp_code]",
      "description": "Company code from user session"
    },
    "user_id": {
      "forms6i_mapping": ":GLOBAL.M_USER_ID", 
      "web_mapping": "session[user_id]",
      "description": "User ID from user session"
    }
  }
}'
WHERE RPT_ID = 'FIN006';

-- Verify the update
SELECT RPT_ID, RPT_NAME, 
       CASE 
         WHEN RPT_PARAMS IS NOT NULL THEN 'RPT_PARAMS Updated'
         ELSE 'RPT_PARAMS Missing'
       END as STATUS,
       LENGTH(RPT_PARAMS) as PARAMS_LENGTH
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'FIN006';

COMMIT;

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================

-- Check parameter extraction
SELECT 'Parameter Check' as VERIFICATION,
       JSON_VALUE(RPT_PARAMS, '$.parameters[0].field') as FIRST_PARAM_FIELD,
       JSON_VALUE(RPT_PARAMS, '$.parameters[0].name') as FIRST_PARAM_NAME,
       JSON_VALUE(RPT_PARAMS, '$.display_columns[0]') as FIRST_DISPLAY_COLUMN
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'FIN006';

-- Check column headers
SELECT 'Column Headers Check' as VERIFICATION,
       JSON_VALUE(RPT_PARAMS, '$.column_headers.MAIN_AC') as MAIN_AC_HEADER,
       JSON_VALUE(RPT_PARAMS, '$.column_headers.SUB_AC_DESC') as CUSTOMER_NAME_HEADER
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'FIN006';