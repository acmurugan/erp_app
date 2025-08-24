-- =============================================================================
-- TTL202 COLUMN HEADERS - CASE CORRECTED TO MATCH CLASS OUTPUT
-- TTL202 class converts "ITEM_CODE" to "Item Code" with .replace('_', ' ').title()
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Customer Analysis 02", "field": "from_cust_anly_02", "type": "text", "required": false, "default": "0"},
    {"name": "To Customer Analysis 02", "field": "to_cust_anly_02", "type": "text", "required": false, "default": "ZZZZZ"},
    {"name": "From Item Analysis 12", "field": "from_item_anly_12", "type": "text", "required": false, "default": "0"},
    {"name": "To Item Analysis 12", "field": "to_item_anly_12", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZ"},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": false, "default": "ZZZZZ"},
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": false, "default": "ZZZZZZZ"}
  ],
  "display_columns": [],
  "column_headers": {
    "Sd Comp Code": "Company Code",
    "Sd Dt": "Sale Date", 
    "Sd Txn No": "Transaction Number",
    "Sd Txn Type": "Transaction Type",
    "Item Name": "Item Description",
    "Item Cost Level": "Item Cost Level",
    "Item Stk Yn Num": "Stock Y/N Number",
    "Sd Del Locn Code": "Delivery Location Code",
    "Locn Group Code": "Location Group Code", 
    "Sd Item Code": "Item Code",
    "Sd Grade Code": "Grade Code",
    "Sd Cust Code": "Customer Code", 
    "Sd Cust Name": "Customer Name",
    "Sm Code": "Salesman Code",
    "Sm Name": "Salesman Name",
    "Sd Sale Locn Code": "Sale Location Code",
    "Class Name": "Product Class",
    "Brand Name": "Brand Name", 
    "Manf Name": "Manufacturer Name",
    "Tbu": "TBU",
    "Catg Name": "Category Name",
    "Rim Size": "Rim Size",
    "Rad Bias": "Radial/Bias",
    "Pr Line": "Product Line", 
    "Manf Grp": "Manufacturer Group",
    "Sales Name": "Sales Category",
    "Cos Name": "COS Category",
    "Tyre Size": "Tyre Size",
    "Old Catg": "Old Category",
    "Gyr Vcode": "GYR V Code",
    "Gyr Ig": "GYR IG",
    "Qty": "Quantity",
    "Item Val": "Item Value",
    "Disc Val": "Discount Value",
    "Vat Val": "VAT Value",
    "Exp Val": "Expense Value",
    "Doc Status": "Document Status",
    "Cost": "Cost",
    "Sales Val": "Sales Value",
    "Excl Vat": "Excluding VAT",
    "Yyyymm": "Year Month",
    "Cust Type": "Customer Type"
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