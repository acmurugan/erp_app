-- =============================================================================
-- Setup FIN001 Report Parameters (SIMPLE VERSION for Oracle 11g)
-- GLOBAL VARIABLE MAPPING (Forms 6i to Web):
-- :GLOBAL.M_COMP_CODE  -> session['comp_code']  (Company Code)
-- :GLOBAL.M_USER_ID    -> session['user_id']    (User ID)  
-- =============================================================================

-- Delete existing FIN001 if exists
DELETE FROM RPT_REPORT_MASTER WHERE RPT_ID = 'FIN001';

-- Insert FIN001 with basic configuration
INSERT INTO RPT_REPORT_MASTER (
    RPT_ID, 
    RPT_NAME, 
    RPT_DESC, 
    RPT_TYPE, 
    RPT_SOURCE, 
    RPT_OUTPUT_FORMATS, 
    RPT_CATEGORY, 
    RPT_ACTIVE_FLAG, 
    RPT_CR_DT, 
    RPT_CR_UID
) VALUES (
    'FIN001', 
    'Trial Balance Report', 
    'Trial Balance Report with GLOBAL variable support',
    'CLASS', 
    'FIN001Report',
    'HTML,PDF,EXCEL', 
    'FINANCE', 
    'Y', 
    SYSDATE, 
    'SYSTEM'
);

-- Now update the CLOB column separately using simple JSON
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Period", "field": "M_FM_YYYYMM", "type": "text", "required": true, "default": "202401"},
    {"name": "To Period", "field": "M_TO_YYYYMM", "type": "text", "required": true, "default": "202412"},
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
  "column_headers": {},
  "hidden_columns": [],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'FIN001';

COMMIT;

-- Verify the configuration
SELECT RPT_ID, RPT_NAME, RPT_TYPE, RPT_SOURCE, RPT_ACTIVE_FLAG
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'FIN001';

PROMPT FIN001 configured with GLOBAL variables support!