-- =============================================================================
-- FIX TTL715 AND TTL201 PARAMETER CONFIGURATION
-- =============================================================================

-- Fix TTL715 - All Transactions Pending For Approval
-- Requires 4 parameters: FM_DT, TO_DT, FM_TXN_CODE, TO_TXN_CODE
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "FM_DT", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "TO_DT", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "From Transaction Code", "field": "FM_TXN_CODE", "type": "text", "required": true, "default": "0"},
    {"name": "To Transaction Code", "field": "TO_TXN_CODE", "type": "text", "required": true, "default": "ZZZZZZ"}
  ],
  "display_columns": ["DT", "TXN", "NUM", "LOCN", "CODE", "NAME", "ITEM", "TXN_TYPE", "UID"],
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

-- Fix TTL201 - Item Wise Sales Analysis
-- Requires 10 parameters based on SQL file analysis
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "From Salesman Code", "field": "from_sdm_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Salesman Code", "field": "to_sdm_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Flash Code", "field": "from_flash_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Flash Code", "field": "to_flash_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": false, "default": "ZZZZZZ"}
  ],
  "display_columns": ["Customer Name", "Customer Code", "SM Name", "Sale Date", "Transaction No", "Item Name", "Item Code", "Quantity", "Item Value", "Sales Value"],
  "column_headers": {
    "Customer Name": "Customer Name",
    "Customer Code": "Customer Code", 
    "SM Code": "Salesman Code",
    "SM Name": "Salesman Name",
    "Sale Date": "Sale Date",
    "Transaction No": "Transaction Number",
    "Location Code": "Location Code",
    "Item Code": "Item Code",
    "Item Name": "Item Name",
    "Grade Code": "Grade Code",
    "Class Name": "Class Name",
    "Brand Name": "Brand Name",
    "Manufacturer Name": "Manufacturer Name",
    "TBU": "TBU",
    "Category Name": "Category Name",
    "Rim Size": "Rim Size",
    "Radial Bias": "Radial Bias",
    "Product Line": "Product Line",
    "Manufacturer Group": "Manufacturer Group",
    "Sales Name": "Sales Name",
    "COS Name": "COS Name",
    "Tyre Size": "Tyre Size",
    "Old Category": "Old Category",
    "GYR VCODE": "GYR V Code",
    "GYR IG": "GYR IG",
    "Quantity": "Quantity",
    "Item Value": "Item Value",
    "Discount Value": "Discount Value",
    "VAT Value": "VAT Value",
    "Cost": "Cost",
    "Sales Value": "Sales Value",
    "Excl VAT": "Excluding VAT",
    "Contribution": "Contribution",
    "Margin %": "Margin %",
    "YYYYMM": "Year Month",
    "Customer Type": "Customer Type"
  },
  "hidden_columns": ["YYYYMM"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL201';

COMMIT;