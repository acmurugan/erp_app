-- =============================================================================
-- AUTO-GENERATED RPT_PARAMS for TTL202 with ALL COLUMN NAMES  
-- This is a complete example showing how to auto-generate ALL column headers
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Customer Analysis 02", "field": "from_cust_anly_02", "type": "text", "required": true, "default": "0"},
    {"name": "To Customer Analysis 02", "field": "to_cust_anly_02", "type": "text", "required": true, "default": "ZZZZZ"},
    {"name": "From Item Analysis 12", "field": "from_item_anly_12", "type": "text", "required": true, "default": "0"},
    {"name": "To Item Analysis 12", "field": "to_item_anly_12", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": true, "default": "ZZZZZZ"},
    {"name": "As Of Date", "field": "as_of_dt", "type": "date", "required": true, "default": "01/01/2024"},
    {"name": "To Date", "field": "to_dt", "type": "date", "required": true, "default": "31/12/2024"},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": true, "default": "0"},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": true, "default": "ZZZZZZ"}
  ],
  "display_columns": [],
  "column_headers": {
    "SD_COMP_CODE": "Company Code",
    "SD_DT": "Sale Date",
    "SD_TXN_NO": "Transaction Number",
    "SD_TXN_TYPE": "Transaction Type",
    "ITEM_NAME": "Item Name",
    "ITEM_COST_LEVEL": "Item Cost Level",
    "ITEM_STK_YN_NUM": "Stock Y/N Number",
    "SD_DEL_LOCN_CODE": "Delivery Location Code",
    "LOCN_GROUP_CODE": "Location Group Code",
    "SD_ITEM_CODE": "Item Code",
    "SD_GRADE_CODE": "Grade Code",
    "SD_CUST_CODE": "Customer Code",
    "SD_CUST_NAME": "Customer Name",
    "SM_CODE": "Salesman Code",
    "SM_NAME": "Salesman Name",
    "SD_SALE_LOCN_CODE": "Sale Location Code",
    "CLASS_NAME": "Class Name",
    "BRAND_NAME": "Brand Name",
    "MANF_NAME": "Manufacturer Name",
    "TBU": "TBU",
    "CATG_NAME": "Category Name",
    "RIM_SIZE": "Rim Size",
    "RAD_BIAS": "Radial Bias",
    "PR_LINE": "Product Line",
    "MANF_GRP": "Manufacturer Group",
    "SALES_NAME": "Sales Name",
    "COS_NAME": "COS Name",
    "TYRE_SIZE": "Tyre Size",
    "OLD_CATG": "Old Category",
    "GYR_VCODE": "GYR V Code",
    "GYR_IG": "GYR IG",
    "QTY": "Quantity",
    "ITEM_VAL": "Item Value",
    "DISC_VAL": "Discount Value",
    "VAT_VAL": "VAT Value",
    "EXP_VAL": "Expense Value",
    "DOC_STATUS": "Document Status",
    "COST": "Cost",
    "SALES_VAL": "Sales Value",
    "EXCL_VAT": "Excluding VAT",
    "YYYYMM": "Year Month",
    "CUST_TYPE": "Customer Type"
  },
  "hidden_columns": [],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL202';

COMMIT;

-- =============================================================================
-- CUSTOMIZATION EXAMPLES FOR TTL202:
-- 
-- 1. Hide system/technical columns:
-- "hidden_columns": ["SD_COMP_CODE", "ITEM_STK_YN_NUM", "YYYYMM", "DOC_STATUS"]
--
-- 2. Show only key business columns:
-- "display_columns": ["ITEM_NAME", "SD_CUST_NAME", "SM_NAME", "QTY", "SALES_VAL", "SD_DT"]
-- 
-- 3. Simplify column names (just change what you want):
-- "column_headers": {
--   "SD_CUST_NAME": "Customer",
--   "ITEM_NAME": "Product", 
--   "SALES_VAL": "Sales Amount",
--   "SD_DT": "Date"
-- }
-- 
-- 4. Keep original technical names:
-- "column_headers": {}
-- =============================================================================