-- =============================================================================
-- TTL308 COLUMN HEADERS - CASE CORRECTED TO MATCH CLASS OUTPUT
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
    "Ord": "Order",
    "Head": "Account Head",
    "Th Comp Code": "Company Code",
    "Th Acnt Year": "Account Year",
    "Gh Txn Code": "Transaction Code", 
    "Gh No": "Document Number",
    "Gh Dt": "Document Date",
    "Acnt Name": "Account Name",
    "Gh Txn No": "Transaction Number",
    "Gh Supp Code": "Supplier/Customer Code",
    "Gh Amt": "Gross Amount",
    "Nett Amt": "Net Amount",
    "Vat Amt": "VAT Amount",
    "Ref": "Reference"
  },
  "hidden_columns": ["Ord"],
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