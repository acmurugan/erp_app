-- =============================================================================
-- AUTO-GENERATED RPT_PARAMS for TTL308 - VAT Analysis Report
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "Account Year", "field": "acnt_year", "type": "number", "required": true, "default": "2024"},
    {"name": "Current/Previous Period", "field": "cur_prv", "type": "select", "required": true, "default": "C",
     "options": [{"value": "C", "text": "Current Period"}, {"value": "P", "text": "Previous Period"}]},
    {"name": "Report Type", "field": "report_type", "type": "select", "required": true, "default": "SUMMARY",
     "options": [{"value": "SUMMARY", "text": "Summary Report"}, {"value": "DETAILED", "text": "Detailed Report"}]}
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
    "GH_SUPP_CODE": "Supplier Code",
    "GH_AMT": "Gross Amount",
    "NETT_AMT": "Net Amount",
    "VAT_AMT": "VAT Amount",
    "REF": "Reference",
    "VAT_RATE": "VAT Rate %",
    "TAXABLE_AMT": "Taxable Amount",
    "INPUT_VAT": "Input VAT",
    "OUTPUT_VAT": "Output VAT",
    "VAT_PAYABLE": "VAT Payable",
    "VAT_REFUND": "VAT Refund"
  },
  "hidden_columns": ["ORD"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL308';

COMMIT;