-- =============================================================================
-- SQL Script to Update TTL202 RPT_PARAMS - Remove GLOBAL Variables
-- =============================================================================

-- Check current RPT_PARAMS for TTL202
SELECT RPT_ID, RPT_NAME, 
       SUBSTR(RPT_PARAMS, 1, 500) as RPT_PARAMS_PREVIEW
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'TTL202';

-- Update TTL202 RPT_PARAMS to remove comp_code and user_id parameters
-- Since they are now handled as session variables in the Python class
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "report_id": "TTL202",
  "report_name": "Item Wise Sales Analysis (TTL202)",
  "report_description": "Comprehensive sales analysis report with item details, cost calculations, margin analysis, and customer information. Converted from Forms 6i POPULATE_Q2 procedure.",
  "display_columns": [],
  "column_headers": {},
  "hidden_columns": [],
  "parameters": {
    "from_cust_anly_02": {
      "type": "text",
      "label": "FROM CUST ANLY 02",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "FROM CUST ANLY 02",
      "default_value": "0"
    },
    "to_cust_anly_02": {
      "type": "text",
      "label": "TO CUST ANLY 02",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "TO CUST ANLY 02",
      "default_value": "ZZZZZ"
    },
    "from_item_anly_12": {
      "type": "text",
      "label": "FROM ITEM ANLY 12",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "FROM ITEM ANLY 12",
      "default_value": "0"
    },
    "to_item_anly_12": {
      "type": "text",
      "label": "TO ITEM ANLY 12",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "TO ITEM ANLY 12",
      "default_value": "ZZZZZZ"
    },
    "from_cust_code": {
      "type": "text",
      "label": "FROM CUST CODE",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "FROM CUST CODE",
      "default_value": "0"
    },
    "to_cust_code": {
      "type": "text",
      "label": "TO CUST CODE",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "TO CUST CODE",
      "default_value": "ZZZZ"
    },
    "from_item_code": {
      "type": "text",
      "label": "FROM ITEM CODE",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "FROM ITEM CODE",
      "default_value": "0"
    },
    "to_item_code": {
      "type": "text",
      "label": "TO ITEM CODE",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "TO ITEM CODE",
      "default_value": "ZZZZZ"
    },
    "from_date": {
      "type": "date",
      "label": "FROM DATE",
      "required": true,
      "data_type": "DATE",
      "description": "FROM DATE",
      "default_value": "01/01/2024"
    },
    "to_date": {
      "type": "date",
      "label": "TO DATE",
      "required": true,
      "data_type": "DATE",
      "description": "TO DATE",
      "default_value": "31/12/2024"
    },
    "from_locn_code": {
      "type": "text",
      "label": "FROM LOCN CODE",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "FROM LOCN CODE",
      "default_value": "0"
    },
    "to_locn_code": {
      "type": "text",
      "label": "TO LOCN CODE",
      "required": true,
      "data_type": "VARCHAR2",
      "description": "TO LOCN CODE",
      "default_value": "ZZZZZZZ"
    }
  },
  "ui_config": {
    "default_page_size": 50,
    "enable_search": true,
    "enable_export": true,
    "export_formats": ["VIEW", "EXCEL", "PDF"],
    "date_format": "DD/MM/YYYY",
    "show_row_numbers": true,
    "enable_sorting": true,
    "sortable_columns": []
  },
  "metadata": {
    "generated_date": "2024-08-22T12:00:00Z",
    "source": "Forms 6i Production Converter - Updated",
    "version": "1.1",
    "parameter_count": 12,
    "syntax_validated": true,
    "update_reason": "Removed GLOBAL session variables (comp_code, user_id) - now handled in Python class"
  }
}'
WHERE RPT_ID = 'TTL202';

-- Verify the update
SELECT RPT_ID, RPT_NAME,
       CASE 
         WHEN RPT_PARAMS IS NOT NULL THEN 'Updated Successfully'
         ELSE 'Update Failed'
       END as UPDATE_STATUS
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'TTL202';

-- Commit the changes
COMMIT;

-- Show parameter count after update
SELECT 
    RPT_ID,
    JSON_VALUE(RPT_PARAMS, '$.metadata.parameter_count') as PARAM_COUNT,
    JSON_VALUE(RPT_PARAMS, '$.metadata.update_reason') as UPDATE_REASON
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'TTL202';