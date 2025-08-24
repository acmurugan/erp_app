-- =============================================================================
-- AUTO-GENERATED RPT_PARAMS for TTL715 - All Transactions Pending For Approval (SQL)
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "FM_DT", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "TO_DT", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "From Transaction Code", "field": "FM_TXN_CODE", "type": "text", "required": true, "default": "0"},
    {"name": "To Transaction Code", "field": "TO_TXN_CODE", "type": "text", "required": true, "default": "ZZZZZZ"}
  ],
  "display_columns": [],
  "column_headers": {
    "ORD": "Order",
    "SYS_ID": "System ID",
    "DT": "Document Date",
    "TXN": "Transaction Code",
    "NUM": "Document Number",
    "LOCN": "Location Code",
    "CODE": "Supplier/Customer Code",
    "NAME": "Supplier/Customer Name",
    "ITEM": "Has Items",
    "TXN_TYPE": "Transaction Type",
    "UID": "Created By"
  },
  "hidden_columns": ["ORD", "SYS_ID"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL715';

COMMIT;