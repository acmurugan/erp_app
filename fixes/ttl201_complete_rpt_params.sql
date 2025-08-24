-- =============================================================================
-- AUTO-GENERATED RPT_PARAMS for TTL201 - Sales Detail Report (SQL)
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From SDM Code", "field": "from_sdm_code", "type": "text", "required": false, "default": "0"},
    {"name": "To SDM Code", "field": "to_sdm_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Flash Code", "field": "from_flash_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Flash Code", "field": "to_flash_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": false, "default": "0"},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": false, "default": "ZZZZZZ"},
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024"}
  ],
  "display_columns": [],
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
    "Class Name": "Product Class",
    "Brand Name": "Brand Name",
    "Manufacturer Name": "Manufacturer",
    "TBU": "TBU",
    "Category Name": "Category",
    "Rim Size": "Rim Size",
    "Radial Bias": "Radial/Bias",
    "Product Line": "Product Line",
    "Manufacturer Group": "Manufacturer Group",
    "Sales Name": "Sales Category",
    "COS Name": "COS Category",
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