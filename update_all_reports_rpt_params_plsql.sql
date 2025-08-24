-- =============================================================================
-- COMPREHENSIVE RPT_PARAMS UPDATE FOR ALL REPORTS - PL/SQL VERSION
-- Updated: 24/08/2025 by Claude Code
-- 
-- This script updates all reports with proper RPT_PARAMS configuration
-- Uses PL/SQL to handle CLOB columns properly
-- =============================================================================

SET SERVEROUTPUT ON

DECLARE
    v_params CLOB;
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== Updating RPT_PARAMS for All Reports ===');
    
    -- =============================================================================
    -- UPDATE FIN001 - Trial Balance Report (CLASS)
    -- =============================================================================
    v_params := '{
  "parameters": [
    {
      "name": "From Period", 
      "field": "M_FM_YYYYMM", 
      "type": "text", 
      "required": true, 
      "default": "202501",
      "description": "Starting period in YYYYMM format"
    },
    {
      "name": "To Period", 
      "field": "M_TO_YYYYMM", 
      "type": "text", 
      "required": true, 
      "default": "202512",
      "description": "Ending period in YYYYMM format"
    },
    {
      "name": "From Division", 
      "field": "M_FM_DIVN", 
      "type": "text", 
      "required": true, 
      "default": "0",
      "description": "Starting division code range"
    },
    {
      "name": "To Division", 
      "field": "M_TO_DIVN", 
      "type": "text", 
      "required": true, 
      "default": "ZZZZZZ",
      "description": "Ending division code range"
    },
    {
      "name": "From Department", 
      "field": "M_FM_DEPT", 
      "type": "text", 
      "required": true, 
      "default": "0",
      "description": "Starting department code range"
    },
    {
      "name": "To Department", 
      "field": "M_TO_DEPT", 
      "type": "text", 
      "required": true, 
      "default": "ZZZZZZ",
      "description": "Ending department code range"
    },
    {
      "name": "From Main Account", 
      "field": "M_FM_MAIN_AC", 
      "type": "text", 
      "required": true, 
      "default": "0",
      "description": "Starting main account code range"
    },
    {
      "name": "To Main Account", 
      "field": "M_TO_MAIN_AC", 
      "type": "text", 
      "required": true, 
      "default": "ZZZZZZ",
      "description": "Ending main account code range"
    },
    {
      "name": "From Sub Account", 
      "field": "M_FM_SUB_AC", 
      "type": "text", 
      "required": true, 
      "default": "0",
      "description": "Starting sub account code range"
    },
    {
      "name": "To Sub Account", 
      "field": "M_TO_SUB_AC", 
      "type": "text", 
      "required": true, 
      "default": "ZZZZZZ",
      "description": "Ending sub account code range"
    }
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
    "OPN_BAL_AMT": "Opening Balance",
    "DR_AMT": "Debit Amount",
    "CR_AMT": "Credit Amount",
    "CLS_BAL_AMT": "Closing Balance"
  },
  "hidden_columns": [],
  "ui_config": {
    "date_format": "DD/MM/YYYY", 
    "theme": "bootstrap",
    "report_title": "Trial Balance Report"
  },
  "global_variables": {
    "comp_code": {
      "forms6i_mapping": ":GLOBAL.M_COMP_CODE", 
      "web_mapping": "session[comp_code]"
    },
    "user_id": {
      "forms6i_mapping": ":GLOBAL.M_USER_ID", 
      "web_mapping": "session[user_id]"
    }
  }
}';

    UPDATE RPT_REPORT_MASTER 
    SET RPT_PARAMS = v_params
    WHERE RPT_ID = 'FIN001';
    
    DBMS_OUTPUT.PUT_LINE('✓ Updated FIN001 - Trial Balance Report');

    -- =============================================================================
    -- UPDATE TTL202 - Item Wise Sales Analysis (CLASS)
    -- =============================================================================
    v_params := '{
  "parameters": [
    {
      "name": "From Date", 
      "field": "from_date", 
      "type": "date", 
      "required": true, 
      "default": "01/01/2024",
      "description": "Start date for sales analysis"
    },
    {
      "name": "To Date", 
      "field": "to_date", 
      "type": "date", 
      "required": true, 
      "default": "31/12/2024",
      "description": "End date for sales analysis"
    },
    {
      "name": "From Item Code", 
      "field": "from_item_code", 
      "type": "text", 
      "required": false, 
      "default": "0",
      "description": "Starting item code range"
    },
    {
      "name": "To Item Code", 
      "field": "to_item_code", 
      "type": "text", 
      "required": false, 
      "default": "ZZZZZZ",
      "description": "Ending item code range"
    },
    {
      "name": "From Customer Code", 
      "field": "from_cust_code", 
      "type": "text", 
      "required": false, 
      "default": "0",
      "description": "Starting customer code range"
    },
    {
      "name": "To Customer Code", 
      "field": "to_cust_code", 
      "type": "text", 
      "required": false, 
      "default": "ZZZZZZ",
      "description": "Ending customer code range"
    }
  ],
  "display_columns": [],
  "column_headers": {
    "ITEM_CODE": "Item Code",
    "ITEM_NAME": "Item Description",
    "CUST_CODE": "Customer Code",
    "CUST_NAME": "Customer Name",
    "SALE_DATE": "Sale Date",
    "DOC_NO": "Document Number",
    "QTY_SOLD": "Quantity Sold",
    "UNIT_PRICE": "Unit Price",
    "TOTAL_AMOUNT": "Total Amount",
    "COST_AMOUNT": "Cost Amount",
    "MARGIN_AMOUNT": "Margin Amount",
    "MARGIN_PERCENT": "Margin %"
  },
  "hidden_columns": [],
  "ui_config": {
    "date_format": "DD/MM/YYYY", 
    "theme": "bootstrap",
    "report_title": "Item Wise Sales Analysis"
  },
  "global_variables": {
    "comp_code": {
      "forms6i_mapping": ":GLOBAL.M_COMP_CODE", 
      "web_mapping": "session[comp_code]"
    },
    "user_id": {
      "forms6i_mapping": ":GLOBAL.M_USER_ID", 
      "web_mapping": "session[user_id]"
    }
  }
}';

    UPDATE RPT_REPORT_MASTER 
    SET RPT_PARAMS = v_params
    WHERE RPT_ID = 'TTL202';
    
    DBMS_OUTPUT.PUT_LINE('✓ Updated TTL202 - Item Wise Sales Analysis');

    -- =============================================================================
    -- UPDATE TTL308 - VAT Analysis Report (CLASS)
    -- =============================================================================
    v_params := '{
  "parameters": [
    {
      "name": "From Date", 
      "field": "from_date", 
      "type": "date", 
      "required": true, 
      "default": "01/01/2024",
      "description": "Start date for VAT analysis"
    },
    {
      "name": "To Date", 
      "field": "to_date", 
      "type": "date", 
      "required": true, 
      "default": "31/12/2024",
      "description": "End date for VAT analysis"
    },
    {
      "name": "VAT Type", 
      "field": "vat_type", 
      "type": "select", 
      "required": true, 
      "default": "ALL", 
      "options": [
        {"value": "ALL", "text": "All VAT Types"}, 
        {"value": "INPUT", "text": "Input VAT"}, 
        {"value": "OUTPUT", "text": "Output VAT"}
      ],
      "description": "Type of VAT analysis"
    }
  ],
  "display_columns": [],
  "column_headers": {
    "DOC_DATE": "Document Date",
    "DOC_NO": "Document Number",
    "SUPPLIER_NAME": "Supplier/Customer Name",
    "TAXABLE_AMOUNT": "Taxable Amount",
    "VAT_AMOUNT": "VAT Amount",
    "TOTAL_AMOUNT": "Total Amount",
    "VAT_RATE": "VAT Rate %",
    "VAT_TYPE": "VAT Type"
  },
  "hidden_columns": [],
  "ui_config": {
    "date_format": "DD/MM/YYYY", 
    "theme": "bootstrap",
    "report_title": "VAT Analysis Report"
  },
  "global_variables": {
    "comp_code": {
      "forms6i_mapping": ":GLOBAL.M_COMP_CODE", 
      "web_mapping": "session[comp_code]"
    },
    "user_id": {
      "forms6i_mapping": ":GLOBAL.M_USER_ID", 
      "web_mapping": "session[user_id]"
    }
  }
}';

    UPDATE RPT_REPORT_MASTER 
    SET RPT_PARAMS = v_params
    WHERE RPT_ID = 'TTL308';
    
    DBMS_OUTPUT.PUT_LINE('✓ Updated TTL308 - VAT Analysis Report');

    -- =============================================================================
    -- UPDATE TTL201 - Sales Detail Report (SQL)
    -- =============================================================================
    v_params := '{
  "parameters": [
    {
      "name": "From SDM Code", 
      "field": "from_sdm_code", 
      "type": "text", 
      "required": false, 
      "default": "0",
      "description": "Starting salesman code range"
    },
    {
      "name": "To SDM Code", 
      "field": "to_sdm_code", 
      "type": "text", 
      "required": false, 
      "default": "ZZZZZZ",
      "description": "Ending salesman code range"
    },
    {
      "name": "From Customer Code", 
      "field": "from_cust_code", 
      "type": "text", 
      "required": false, 
      "default": "0",
      "description": "Starting customer code range"
    },
    {
      "name": "To Customer Code", 
      "field": "to_cust_code", 
      "type": "text", 
      "required": false, 
      "default": "ZZZZZZ",
      "description": "Ending customer code range"
    },
    {
      "name": "From Item Code", 
      "field": "from_item_code", 
      "type": "text", 
      "required": false, 
      "default": "0",
      "description": "Starting item code range"
    },
    {
      "name": "To Item Code", 
      "field": "to_item_code", 
      "type": "text", 
      "required": false, 
      "default": "ZZZZZZ",
      "description": "Ending item code range"
    },
    {
      "name": "From Date", 
      "field": "from_date", 
      "type": "date", 
      "required": true, 
      "default": "01/01/2024",
      "description": "Start date for sales detail"
    },
    {
      "name": "To Date", 
      "field": "to_date", 
      "type": "date", 
      "required": true, 
      "default": "31/12/2024",
      "description": "End date for sales detail"
    }
  ],
  "display_columns": [],
  "column_headers": {
    "CUST_NAME": "Customer Name",
    "CUST_CODE": "Customer Code",
    "SM_CODE": "Salesman Code",
    "SM_NAME": "Salesman Name",
    "SALE_DATE": "Sale Date",
    "TRAN_NO": "Transaction Number",
    "LOCN_CODE": "Location Code",
    "ITEM_CODE": "Item Code",
    "ITEM_NAME": "Item Description",
    "QTY": "Quantity",
    "RATE": "Unit Rate",
    "AMOUNT": "Amount"
  },
  "hidden_columns": [],
  "ui_config": {
    "date_format": "DD/MM/YYYY", 
    "theme": "bootstrap",
    "report_title": "Sales Detail Report"
  },
  "global_variables": {
    "comp_code": {
      "forms6i_mapping": ":GLOBAL.M_COMP_CODE", 
      "web_mapping": "session[comp_code]"
    },
    "user_id": {
      "forms6i_mapping": ":GLOBAL.M_USER_ID", 
      "web_mapping": "session[user_id]"
    }
  }
}';

    UPDATE RPT_REPORT_MASTER 
    SET RPT_PARAMS = v_params
    WHERE RPT_ID = 'TTL201';
    
    DBMS_OUTPUT.PUT_LINE('✓ Updated TTL201 - Sales Detail Report');

    -- =============================================================================
    -- UPDATE TTL715 - Generic SQL Report
    -- =============================================================================
    v_params := '{
  "parameters": [
    {
      "name": "From Date", 
      "field": "from_date", 
      "type": "date", 
      "required": true, 
      "default": "01/01/2024",
      "description": "Start date for analysis"
    },
    {
      "name": "To Date", 
      "field": "to_date", 
      "type": "date", 
      "required": true, 
      "default": "31/12/2024",
      "description": "End date for analysis"
    }
  ],
  "display_columns": [],
  "column_headers": {},
  "hidden_columns": [],
  "ui_config": {
    "date_format": "DD/MM/YYYY", 
    "theme": "bootstrap"
  },
  "global_variables": {
    "comp_code": {
      "forms6i_mapping": ":GLOBAL.M_COMP_CODE", 
      "web_mapping": "session[comp_code]"
    },
    "user_id": {
      "forms6i_mapping": ":GLOBAL.M_USER_ID", 
      "web_mapping": "session[user_id]"
    }
  }
}';

    UPDATE RPT_REPORT_MASTER 
    SET RPT_PARAMS = v_params
    WHERE RPT_ID = 'TTL715';
    
    DBMS_OUTPUT.PUT_LINE('✓ Updated TTL715 - Generic Report');

    -- Commit all changes
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('=== All Updates Committed Successfully ===');

END;
/

-- =============================================================================
-- VERIFICATION QUERY
-- =============================================================================
PROMPT
PROMPT === Verification: Check All Updated Reports ===
PROMPT

SELECT RPT_ID, 
       RPT_NAME,
       CASE 
         WHEN RPT_PARAMS IS NOT NULL THEN 'UPDATED'
         ELSE 'MISSING'
       END as STATUS,
       LENGTH(RPT_PARAMS) as PARAMS_LENGTH
FROM RPT_REPORT_MASTER 
WHERE RPT_ID IN ('FIN001', 'FIN006', 'TTL201', 'TTL202', 'TTL308', 'TTL715')
ORDER BY RPT_ID;

PROMPT
PROMPT === Update Summary ===
PROMPT Reports Updated:
PROMPT - FIN001: Trial Balance Report (period-based parameters)
PROMPT - FIN006: Customer Aging Analysis (already updated with as_of_date)
PROMPT - TTL201: Sales Detail Report (comprehensive filters) 
PROMPT - TTL202: Item Wise Sales Analysis (date + item/customer filters)
PROMPT - TTL308: VAT Analysis Report (date + VAT type dropdown)
PROMPT - TTL715: Generic Report Template (basic date range)
PROMPT
PROMPT Key Features:
PROMPT - Session variables excluded from parameter forms
PROMPT - User-friendly column headers
PROMPT - Parameter descriptions and validation
PROMPT - Consistent UI configuration
PROMPT