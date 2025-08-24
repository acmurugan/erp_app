-- =============================================================================
-- UPDATE PARAMETER VISIBILITY FOR ALL REPORTS
-- Adds visible property to all parameters for proper checkbox functionality
-- =============================================================================

-- Update FIN001 with parameter visibility
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "As Of Date", "field": "as_of_date", "type": "date", "required": true, "default": "31/12/2024", "visible": true},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0", "visible": false},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true}
  ],
  "display_columns": ["Customer Code", "Customer Name", "Due Days", "Current", "Days 1-30", "Days 31-60", "Days 61-90", "Over 90", "Total Outstanding"],
  "available_columns": ["Customer Code", "Customer Name", "Due Days", "Current", "Days 1-30", "Days 31-60", "Days 61-90", "Over 90", "Total Outstanding", "Credit Limit", "Balance"],
  "column_headers": {
    "Customer Code": "Customer Code",
    "Customer Name": "Customer Name", 
    "Due Days": "Due Days",
    "Current": "Current",
    "Days 1-30": "1-30 Days",
    "Days 31-60": "31-60 Days", 
    "Days 61-90": "61-90 Days",
    "Over 90": "Over 90 Days",
    "Total Outstanding": "Total Outstanding",
    "Credit Limit": "Credit Limit",
    "Balance": "Balance"
  },
  "hidden_columns": ["Due Days"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"web_mapping": "session[comp_code]"},
    "user_id": {"web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'FIN001';

-- Update TTL202 with mixed visibility (some visible, some hidden)
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Customer Analysis 02", "field": "from_cust_anly_02", "type": "text", "required": false, "default": "0", "visible": false},
    {"name": "To Customer Analysis 02", "field": "to_cust_anly_02", "type": "text", "required": false, "default": "ZZZZZ", "visible": false},
    {"name": "From Item Analysis 12", "field": "from_item_anly_12", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Item Analysis 12", "field": "to_item_anly_12", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZ", "visible": true},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": false, "default": "ZZZZZ", "visible": true},
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024", "visible": true},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024", "visible": true},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": false, "default": "0", "visible": false},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": false, "default": "ZZZZZZZ", "visible": false}
  ],
  "display_columns": ["Sd Cust Name", "Item Name", "Sm Name", "Sd Dt", "Qty", "Sales Val", "Sd Item Code", "Class Name", "Brand Name"],
  "available_columns": ["Sd Comp Code", "Sd Dt", "Sd Txn No", "Sd Txn Type", "Item Name", "Item Cost Level", "Item Stk Yn Num", "Sd Del Locn Code", "Locn Group Code", "Sd Item Code", "Sd Grade Code", "Sd Cust Code", "Sd Cust Name", "Sm Code", "Sm Name", "Sd Sale Locn Code", "Class Name", "Brand Name", "Manf Name", "Tbu", "Catg Name", "Rim Size", "Rad Bias", "Pr Line", "Manf Grp", "Sales Name", "Cos Name", "Tyre Size", "Old Catg", "Gyr Vcode", "Gyr Ig", "Qty", "Item Val", "Disc Val", "Vat Val", "Exp Val", "Doc Status", "Cost", "Sales Val", "Excl Vat", "Yyyymm", "Cust Type"],
  "column_headers": {
    "Sd Comp Code": "Company Code",
    "Sd Dt": "Sale Date", 
    "Sd Txn No": "Transaction Number",
    "Sd Txn Type": "Transaction Type",
    "Item Name": "Item Description",
    "Sd Item Code": "Item Code",
    "Sd Cust Name": "Customer Name",
    "Sm Name": "Salesman Name",
    "Class Name": "Product Class",
    "Brand Name": "Brand Name",
    "Qty": "Quantity",
    "Sales Val": "Sales Value"
  },
  "hidden_columns": ["Yyyymm"],
  "ui_config": {
    "date_format": "DD/MM/YYYY", 
    "theme": "bootstrap",
    "report_title": "Item Wise Sales Analysis"
  },
  "global_variables": {
    "comp_code": {"web_mapping": "session[comp_code]"},
    "user_id": {"web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL202';

COMMIT;