-- =============================================================================
-- AUTO-GENERATED RPT_PARAMS for FIN006 - Customer Aging Analysis
-- FIXED: Column headers match actual report output, session variables excluded
-- =============================================================================

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
  "display_columns": [
    "MAIN_AC", "SUB_AC", "SUB_AC_DESC", "TERM_DAYS", "CURR", 
    "ABOVE_120_DAYS", "90_TO_120_DAYS", "60_TO_90_DAYS", "30_TO_60_DAYS", "UPTO_30_DAYS", 
    "NET_VAL", "CR_LIMIT"
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
    "NET_VAL": "Net Value",
    "CR_LIMIT": "Credit Limit"
  },
  "hidden_columns": [],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'FIN006';

COMMIT;