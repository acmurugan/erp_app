-- =============================================================================
-- Setup FIN001 Report Parameters  
-- This script should be executed to configure FIN001 parameters in the database
-- 
-- GLOBAL VARIABLE MAPPING (Forms 6i to Web):
-- :GLOBAL.M_COMP_CODE  -> session['comp_code']  (Company Code)
-- :GLOBAL.M_USER_ID    -> session['user_id']    (User ID)  
-- :GLOBAL.M_LANG_CODE  -> session['lang_code']  (Language Code, default: 'EN')
-- :GLOBAL.M_DATE       -> system date          (Current Date)
-- =============================================================================

-- Insert or Update FIN001 configuration
MERGE INTO RPT_REPORT_MASTER rm
USING (
  SELECT 'FIN001' as rpt_id FROM dual
) src
ON (rm.RPT_ID = src.rpt_id)
WHEN MATCHED THEN
  UPDATE SET
    RPT_NAME = 'Trial Balance Report',
    RPT_DESC = 'Trial Balance Report with complete original query from Forms 6i',
    RPT_TYPE = 'CLASS',
    RPT_SOURCE = 'FIN001Report',
    RPT_OUTPUT_FORMATS = 'HTML,PDF,EXCEL',
    RPT_CATEGORY = 'FINANCE',
    RPT_PARAMS = '{
      "parameters": [
        {
          "name": "Global Flag",
          "field": "GLOBAL",
          "type": "select",
          "required": true,
          "default": "0",
          "options": [
            {"value": "0", "text": "No"},
            {"value": "1", "text": "Yes"}
          ],
          "description": "Global analysis flag"
        },
        {
          "name": "Account Year",
          "field": "M_YEAR",
          "type": "number",
          "required": true,
          "default": "2024",
          "description": "Financial account year"
        },
        {
          "name": "From Period (YYYYMM)",
          "field": "M_FM_YYYYMM",
          "type": "text",
          "required": true,
          "default": "202401",
          "description": "Starting period in YYYYMM format"
        },
        {
          "name": "To Period (YYYYMM)",
          "field": "M_TO_YYYYMM",
          "type": "text",
          "required": true,
          "default": "202412",
          "description": "Ending period in YYYYMM format"
        },
        {
          "name": "From Division",
          "field": "M_FM_DIVN",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting division code"
        },
        {
          "name": "To Division",
          "field": "M_TO_DIVN",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending division code"
        },
        {
          "name": "From Department",
          "field": "M_FM_DEPT",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting department code"
        },
        {
          "name": "To Department",
          "field": "M_TO_DEPT",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending department code"
        },
        {
          "name": "From Main Account",
          "field": "M_FM_MAIN_AC",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting main account code"
        },
        {
          "name": "To Main Account",
          "field": "M_TO_MAIN_AC",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending main account code"
        },
        {
          "name": "From Sub Account",
          "field": "M_FM_SUB_AC",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting sub account code"
        },
        {
          "name": "To Sub Account",
          "field": "M_TO_SUB_AC",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending sub account code"
        },
        {
          "name": "Dummy Parameter",
          "field": "DUMMY",
          "type": "text",
          "required": false,
          "default": "0",
          "description": "Dummy parameter for compatibility"
        },
        {
          "name": "Company Code",
          "field": "comp_code",
          "type": "text",
          "required": true,
          "default": "TTM",
          "description": "Company code (:GLOBAL.M_COMP_CODE)",
          "global_variable": ":GLOBAL.M_COMP_CODE",
          "source": "session"
        },
        {
          "name": "User ID",
          "field": "user_id",
          "type": "text",
          "required": true,
          "default": "SYSTEM",
          "description": "User ID (:GLOBAL.M_USER_ID)",
          "global_variable": ":GLOBAL.M_USER_ID",
          "source": "session"
        },
        {
          "name": "Language Code",
          "field": "lang_code",
          "type": "text",
          "required": false,
          "default": "EN",
          "description": "Language code (:GLOBAL.M_LANG_CODE)",
          "global_variable": ":GLOBAL.M_LANG_CODE",
          "source": "session"
        }
      ],
      "ui_config": {
        "date_format": "DD/MM/YYYY",
        "theme": "bootstrap",
        "form_layout": "grid"
      },
      "global_variables": {
        "comp_code": {
          "forms6i_mapping": ":GLOBAL.M_COMP_CODE",
          "web_mapping": "session['comp_code']",
          "description": "Company code from user session"
        },
        "user_id": {
          "forms6i_mapping": ":GLOBAL.M_USER_ID",
          "web_mapping": "session['user_id']", 
          "description": "User ID from user session"
        },
        "lang_code": {
          "forms6i_mapping": ":GLOBAL.M_LANG_CODE",
          "web_mapping": "session['lang_code']",
          "description": "Language code from user session"
        }
      }
    }',
    RPT_ACTIVE_FLAG = 'Y',
    RPT_UPD_DT = SYSDATE,
    RPT_UPD_UID = 'SYSTEM'
WHEN NOT MATCHED THEN
  INSERT (
    RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_PARAMS,
    RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_ACTIVE_FLAG, RPT_CR_DT, RPT_CR_UID
  )
  VALUES (
    'FIN001', 'Trial Balance Report', 'Trial Balance Report with complete original query from Forms 6i', 
    'CLASS', 'FIN001Report',
    '{
      "parameters": [
        {
          "name": "Global Flag",
          "field": "GLOBAL",
          "type": "select",
          "required": true,
          "default": "0",
          "options": [
            {"value": "0", "text": "No"},
            {"value": "1", "text": "Yes"}
          ],
          "description": "Global analysis flag"
        },
        {
          "name": "Account Year",
          "field": "M_YEAR",
          "type": "number",
          "required": true,
          "default": "2024",
          "description": "Financial account year"
        },
        {
          "name": "From Period (YYYYMM)",
          "field": "M_FM_YYYYMM",
          "type": "text",
          "required": true,
          "default": "202401",
          "description": "Starting period in YYYYMM format"
        },
        {
          "name": "To Period (YYYYMM)",
          "field": "M_TO_YYYYMM",
          "type": "text",
          "required": true,
          "default": "202412",
          "description": "Ending period in YYYYMM format"
        },
        {
          "name": "From Division",
          "field": "M_FM_DIVN",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting division code"
        },
        {
          "name": "To Division",
          "field": "M_TO_DIVN",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending division code"
        },
        {
          "name": "From Department",
          "field": "M_FM_DEPT",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting department code"
        },
        {
          "name": "To Department",
          "field": "M_TO_DEPT",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending department code"
        },
        {
          "name": "From Main Account",
          "field": "M_FM_MAIN_AC",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting main account code"
        },
        {
          "name": "To Main Account",
          "field": "M_TO_MAIN_AC",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending main account code"
        },
        {
          "name": "From Sub Account",
          "field": "M_FM_SUB_AC",
          "type": "text",
          "required": true,
          "default": "0",
          "description": "Starting sub account code"
        },
        {
          "name": "To Sub Account",
          "field": "M_TO_SUB_AC",
          "type": "text",
          "required": true,
          "default": "ZZZZZZ",
          "description": "Ending sub account code"
        },
        {
          "name": "Dummy Parameter",
          "field": "DUMMY",
          "type": "text",
          "required": false,
          "default": "0",
          "description": "Dummy parameter for compatibility"
        },
        {
          "name": "Company Code",
          "field": "comp_code",
          "type": "text",
          "required": true,
          "default": "TTM",
          "description": "Company code (:GLOBAL.M_COMP_CODE)",
          "global_variable": ":GLOBAL.M_COMP_CODE",
          "source": "session"
        },
        {
          "name": "User ID",
          "field": "user_id",
          "type": "text",
          "required": true,
          "default": "SYSTEM",
          "description": "User ID (:GLOBAL.M_USER_ID)",
          "global_variable": ":GLOBAL.M_USER_ID",
          "source": "session"
        },
        {
          "name": "Language Code",
          "field": "lang_code",
          "type": "text",
          "required": false,
          "default": "EN",
          "description": "Language code (:GLOBAL.M_LANG_CODE)",
          "global_variable": ":GLOBAL.M_LANG_CODE",
          "source": "session"
        }
      ],
      "ui_config": {
        "date_format": "DD/MM/YYYY",
        "theme": "bootstrap",
        "form_layout": "grid"
      },
      "global_variables": {
        "comp_code": {
          "forms6i_mapping": ":GLOBAL.M_COMP_CODE",
          "web_mapping": "session['comp_code']",
          "description": "Company code from user session"
        },
        "user_id": {
          "forms6i_mapping": ":GLOBAL.M_USER_ID",
          "web_mapping": "session['user_id']", 
          "description": "User ID from user session"
        },
        "lang_code": {
          "forms6i_mapping": ":GLOBAL.M_LANG_CODE",
          "web_mapping": "session['lang_code']",
          "description": "Language code from user session"
        }
      }
    }',
    'HTML,PDF,EXCEL', 'FINANCE', 'Y', SYSDATE, 'SYSTEM'
  );

COMMIT;

-- Verify the insert/update
SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_ACTIVE_FLAG,
       RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_CR_DT, RPT_CR_UID 
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'FIN001';