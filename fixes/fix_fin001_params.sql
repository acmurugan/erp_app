-- =============================================================================
-- Fix FIN001 RPT_PARAMS - Restore missing parameters
-- =============================================================================

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

COMMIT;