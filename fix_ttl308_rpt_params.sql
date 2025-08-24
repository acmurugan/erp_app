-- =============================================================================
-- FIX TTL308 RPT_PARAMS - Align with TTL308 class expectations  
-- The class expects: from_date, to_date, cur_prv (required)
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
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
      "name": "Period Type", 
      "field": "cur_prv", 
      "type": "select", 
      "required": true, 
      "default": "C",
      "options": [
        {"value": "C", "text": "Current Period"}, 
        {"value": "P", "text": "Previous Period"}
      ],
      "description": "Current or Previous period analysis"
    }
  ],
  "display_columns": [],
  "column_headers": {
    "ORD": "Order",
    "HEAD": "Account Head",
    "TH_COMP_CODE": "Company Code",
    "TH_ACNT_YEAR": "Account Year",
    "GH_TXN_CODE": "Transaction Code", 
    "GH_NO": "Document Number",
    "GH_DT": "Document Date",
    "ACNT_NAME": "Account Name",
    "GH_TXN_NO": "Transaction Number",
    "GH_SUPP_CODE": "Supplier/Customer Code",
    "GH_AMT": "Gross Amount",
    "NETT_AMT": "Net Amount",
    "VAT_AMT": "VAT Amount",
    "REF": "Reference"
  },
  "hidden_columns": ["ORD"],
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
}'
WHERE RPT_ID = 'TTL308';

COMMIT;

-- Verify the update
SELECT RPT_ID, RPT_NAME, 
       CASE 
         WHEN RPT_PARAMS IS NOT NULL THEN 'UPDATED'
         ELSE 'MISSING'
       END as STATUS
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'TTL308';