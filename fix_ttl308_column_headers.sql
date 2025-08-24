-- =============================================================================
-- TTL308 WITH PROPER COLUMN HEADERS
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {
      "name": "From Date", 
      "field": "from_date", 
      "type": "date", 
      "required": true, 
      "default": "01/01/2024"
    },
    {
      "name": "To Date", 
      "field": "to_date", 
      "type": "date", 
      "required": true, 
      "default": "31/12/2024"
    },
    {
      "name": "Period", 
      "field": "cur_prv", 
      "type": "select", 
      "required": true, 
      "default": "C",
      "options": [
        {"value": "C", "text": "Current"}, 
        {"value": "P", "text": "Previous"}
      ]
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
    "comp_code": {"web_mapping": "session[comp_code]"},
    "user_id": {"web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL308';

COMMIT;

-- Verify the update
SELECT RPT_ID, RPT_NAME, 
       CASE 
         WHEN RPT_PARAMS IS NOT NULL THEN 'UPDATED'
         ELSE 'MISSING'
       END as STATUS,
       LENGTH(RPT_PARAMS) as PARAMS_LENGTH
FROM RPT_REPORT_MASTER 
WHERE RPT_ID = 'TTL308';