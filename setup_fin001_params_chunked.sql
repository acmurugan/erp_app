-- =============================================================================
-- Setup FIN001 Report Parameters (CHUNKED VERSION for Oracle 11g)
-- This script should be executed to configure FIN001 parameters in the database
-- 
-- GLOBAL VARIABLE MAPPING (Forms 6i to Web):
-- :GLOBAL.M_COMP_CODE  -> session['comp_code']  (Company Code)
-- :GLOBAL.M_USER_ID    -> session['user_id']    (User ID)  
-- :GLOBAL.M_LANG_CODE  -> session['lang_code']  (Language Code, default: 'EN')
-- :GLOBAL.M_DATE       -> system date          (Current Date)
-- =============================================================================

-- Check if FIN001 already exists
SET SERVEROUTPUT ON;

DECLARE
    v_count NUMBER;
    v_params CLOB;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM RPT_REPORT_MASTER
    WHERE RPT_ID = 'FIN001';
    
    -- Build the JSON in chunks to avoid string literal length limit
    v_params := '{' || CHR(10);
    v_params := v_params || '  "parameters": [' || CHR(10);
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "Global Flag",' || CHR(10);
    v_params := v_params || '      "field": "GLOBAL",' || CHR(10);
    v_params := v_params || '      "type": "select",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "0",' || CHR(10);
    v_params := v_params || '      "options": [' || CHR(10);
    v_params := v_params || '        {"value": "0", "text": "No"},' || CHR(10);
    v_params := v_params || '        {"value": "1", "text": "Yes"}' || CHR(10);
    v_params := v_params || '      ],' || CHR(10);
    v_params := v_params || '      "description": "Global analysis flag"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "Account Year",' || CHR(10);
    v_params := v_params || '      "field": "M_YEAR",' || CHR(10);
    v_params := v_params || '      "type": "number",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "2024",' || CHR(10);
    v_params := v_params || '      "description": "Financial account year"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "From Period (YYYYMM)",' || CHR(10);
    v_params := v_params || '      "field": "M_FM_YYYYMM",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "202401",' || CHR(10);
    v_params := v_params || '      "description": "Starting period in YYYYMM format"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "To Period (YYYYMM)",' || CHR(10);
    v_params := v_params || '      "field": "M_TO_YYYYMM",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "202412",' || CHR(10);
    v_params := v_params || '      "description": "Ending period in YYYYMM format"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "From Division",' || CHR(10);
    v_params := v_params || '      "field": "M_FM_DIVN",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "0",' || CHR(10);
    v_params := v_params || '      "description": "Starting division code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "To Division",' || CHR(10);
    v_params := v_params || '      "field": "M_TO_DIVN",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "ZZZZZZ",' || CHR(10);
    v_params := v_params || '      "description": "Ending division code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "From Department",' || CHR(10);
    v_params := v_params || '      "field": "M_FM_DEPT",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "0",' || CHR(10);
    v_params := v_params || '      "description": "Starting department code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "To Department",' || CHR(10);
    v_params := v_params || '      "field": "M_TO_DEPT",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "ZZZZZZ",' || CHR(10);
    v_params := v_params || '      "description": "Ending department code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "From Main Account",' || CHR(10);
    v_params := v_params || '      "field": "M_FM_MAIN_AC",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "0",' || CHR(10);
    v_params := v_params || '      "description": "Starting main account code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "To Main Account",' || CHR(10);
    v_params := v_params || '      "field": "M_TO_MAIN_AC",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "ZZZZZZ",' || CHR(10);
    v_params := v_params || '      "description": "Ending main account code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "From Sub Account",' || CHR(10);
    v_params := v_params || '      "field": "M_FM_SUB_AC",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "0",' || CHR(10);
    v_params := v_params || '      "description": "Starting sub account code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "To Sub Account",' || CHR(10);
    v_params := v_params || '      "field": "M_TO_SUB_AC",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "ZZZZZZ",' || CHR(10);
    v_params := v_params || '      "description": "Ending sub account code"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "Company Code",' || CHR(10);
    v_params := v_params || '      "field": "comp_code",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "TTM",' || CHR(10);
    v_params := v_params || '      "description": "Company code (:GLOBAL.M_COMP_CODE)",' || CHR(10);
    v_params := v_params || '      "global_variable": ":GLOBAL.M_COMP_CODE",' || CHR(10);
    v_params := v_params || '      "source": "session"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    
    v_params := v_params || '    {' || CHR(10);
    v_params := v_params || '      "name": "User ID",' || CHR(10);
    v_params := v_params || '      "field": "user_id",' || CHR(10);
    v_params := v_params || '      "type": "text",' || CHR(10);
    v_params := v_params || '      "required": true,' || CHR(10);
    v_params := v_params || '      "default": "SYSTEM",' || CHR(10);
    v_params := v_params || '      "description": "User ID (:GLOBAL.M_USER_ID)",' || CHR(10);
    v_params := v_params || '      "global_variable": ":GLOBAL.M_USER_ID",' || CHR(10);
    v_params := v_params || '      "source": "session"' || CHR(10);
    v_params := v_params || '    }' || CHR(10);
    
    v_params := v_params || '  ],' || CHR(10);
    v_params := v_params || '  "ui_config": {' || CHR(10);
    v_params := v_params || '    "date_format": "DD/MM/YYYY",' || CHR(10);
    v_params := v_params || '    "theme": "bootstrap",' || CHR(10);
    v_params := v_params || '    "form_layout": "grid"' || CHR(10);
    v_params := v_params || '  },' || CHR(10);
    v_params := v_params || '  "global_variables": {' || CHR(10);
    v_params := v_params || '    "comp_code": {' || CHR(10);
    v_params := v_params || '      "forms6i_mapping": ":GLOBAL.M_COMP_CODE",' || CHR(10);
    v_params := v_params || '      "web_mapping": "session[''comp_code'']",' || CHR(10);
    v_params := v_params || '      "description": "Company code from user session"' || CHR(10);
    v_params := v_params || '    },' || CHR(10);
    v_params := v_params || '    "user_id": {' || CHR(10);
    v_params := v_params || '      "forms6i_mapping": ":GLOBAL.M_USER_ID",' || CHR(10);
    v_params := v_params || '      "web_mapping": "session[''user_id'']",' || CHR(10);
    v_params := v_params || '      "description": "User ID from user session"' || CHR(10);
    v_params := v_params || '    }' || CHR(10);
    v_params := v_params || '  }' || CHR(10);
    v_params := v_params || '}';
    
    IF v_count > 0 THEN
        DBMS_OUTPUT.PUT_LINE('FIN001 exists. Updating...');
        
        -- Update existing record
        UPDATE RPT_REPORT_MASTER
        SET RPT_NAME = 'Trial Balance Report',
            RPT_DESC = 'Trial Balance Report with complete original query from Forms 6i',
            RPT_TYPE = 'CLASS',
            RPT_SOURCE = 'FIN001Report',
            RPT_OUTPUT_FORMATS = 'HTML,PDF,EXCEL',
            RPT_CATEGORY = 'FINANCE',
            RPT_PARAMS = v_params,
            RPT_ACTIVE_FLAG = 'Y',
            RPT_UPD_DT = SYSDATE,
            RPT_UPD_UID = 'SYSTEM'
        WHERE RPT_ID = 'FIN001';
        
        DBMS_OUTPUT.PUT_LINE('FIN001 updated successfully.');
        
    ELSE
        DBMS_OUTPUT.PUT_LINE('FIN001 does not exist. Inserting...');
        
        -- Insert new record
        INSERT INTO RPT_REPORT_MASTER (
            RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_PARAMS,
            RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_ACTIVE_FLAG, RPT_CR_DT, RPT_CR_UID
        ) VALUES (
            'FIN001', 
            'Trial Balance Report', 
            'Trial Balance Report with complete original query from Forms 6i',
            'CLASS', 
            'FIN001Report',
            v_params,
            'HTML,PDF,EXCEL', 
            'FINANCE', 
            'Y', 
            SYSDATE, 
            'SYSTEM'
        );
        
        DBMS_OUTPUT.PUT_LINE('FIN001 inserted successfully.');
    END IF;
    
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Transaction committed.');
END;
/

-- Verify the insert/update
PROMPT Verifying FIN001 configuration...
SELECT RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_ACTIVE_FLAG,
       RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_CR_DT, RPT_CR_UID 
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'FIN001';

PROMPT FIN001 setup completed!