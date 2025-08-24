-- =============================================================================
-- FIX ALL REMAINING ADMIN INTERFACE ISSUES - Oracle 11g Compatible
-- =============================================================================

-- Fix TTL201 parameter issue - seems the update didn't apply correctly
-- Let's verify and fix with the correct parameter mapping
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024", "visible": true},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024", "visible": true},
    {"name": "From Salesman Code", "field": "from_sdm_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Salesman Code", "field": "to_sdm_code", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true},
    {"name": "From Flash Code", "field": "from_flash_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Flash Code", "field": "to_flash_code", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true}
  ],
  "display_columns": ["Customer Name", "Customer Code", "SM Name", "Sale Date", "Transaction No", "Item Name", "Item Code", "Quantity", "Item Value", "Sales Value"],
  "available_columns": ["Customer Name", "Customer Code", "SM Code", "SM Name", "Sale Date", "Transaction No", "Location Code", "Item Code", "Item Name", "Grade Code", "Class Name", "Brand Name", "Manufacturer Name", "TBU", "Category Name", "Rim Size", "Radial Bias", "Product Line", "Manufacturer Group", "Sales Name", "COS Name", "Tyre Size", "Old Category", "GYR VCODE", "GYR IG", "Quantity", "Item Value", "Discount Value", "VAT Value", "Cost", "Sales Value", "Excl VAT", "Contribution", "Margin %", "YYYYMM", "Customer Type"],
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

-- Add visible property to all existing parameters for other reports
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "FM_DT", "type": "date", "required": true, "default": "01/01/2024", "visible": true},
    {"name": "To Date", "field": "TO_DT", "type": "date", "required": true, "default": "31/12/2024", "visible": true},
    {"name": "From Transaction Code", "field": "FM_TXN_CODE", "type": "text", "required": true, "default": "0", "visible": true},
    {"name": "To Transaction Code", "field": "TO_TXN_CODE", "type": "text", "required": true, "default": "ZZZZZZ", "visible": true}
  ],
  "display_columns": ["DT", "TXN", "NUM", "LOCN", "CODE", "NAME", "ITEM", "TXN_TYPE", "UID"],
  "available_columns": ["ORD", "SYS_ID", "DT", "TXN", "NUM", "LOCN", "CODE", "NAME", "ITEM", "TXN_TYPE", "UID"],
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

-- Update TTL202 with visible property
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Customer Analysis 02", "field": "from_cust_anly_02", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Customer Analysis 02", "field": "to_cust_anly_02", "type": "text", "required": false, "default": "ZZZZZ", "visible": true},
    {"name": "From Item Analysis 12", "field": "from_item_anly_12", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Item Analysis 12", "field": "to_item_anly_12", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true},
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZ", "visible": true},
    {"name": "From Item Code", "field": "from_item_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Item Code", "field": "to_item_code", "type": "text", "required": false, "default": "ZZZZZ", "visible": true},
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024", "visible": true},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024", "visible": true},
    {"name": "From Location Code", "field": "from_locn_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Location Code", "field": "to_locn_code", "type": "text", "required": false, "default": "ZZZZZZZ", "visible": true}
  ],
  "display_columns": ["Sd Cust Name", "Item Name", "Sm Name", "Sd Dt", "Qty", "Sales Val", "Sd Item Code", "Class Name", "Brand Name"],
  "available_columns": ["Sd Comp Code", "Sd Dt", "Sd Txn No", "Sd Txn Type", "Item Name", "Item Cost Level", "Item Stk Yn Num", "Sd Del Locn Code", "Locn Group Code", "Sd Item Code", "Sd Grade Code", "Sd Cust Code", "Sd Cust Name", "Sm Code", "Sm Name", "Sd Sale Locn Code", "Class Name", "Brand Name", "Manf Name", "Tbu", "Catg Name", "Rim Size", "Rad Bias", "Pr Line", "Manf Grp", "Sales Name", "Cos Name", "Tyre Size", "Old Catg", "Gyr Vcode", "Gyr Ig", "Qty", "Item Val", "Disc Val", "Vat Val", "Exp Val", "Doc Status", "Cost", "Sales Val", "Excl Vat", "Yyyymm", "Cust Type"],
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

-- Update TTL308 with visible property
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Date", "field": "from_date", "type": "date", "required": true, "default": "01/01/2024", "visible": true},
    {"name": "To Date", "field": "to_date", "type": "date", "required": true, "default": "31/12/2024", "visible": true},
    {"name": "Current/Previous", "field": "cur_prv", "type": "text", "required": true, "default": "C", "visible": true}
  ],
  "display_columns": ["Head", "Gh Amt", "Vat Amt", "Total Amt", "Cur Prv"],
  "available_columns": ["Ord", "Head", "Gh Amt", "Vat Amt", "Total Amt", "Cur Prv"],
  "column_headers": {
    "Ord": "Order",
    "Head": "Account Head", 
    "Gh Amt": "Gross Amount",
    "Vat Amt": "VAT Amount",
    "Total Amt": "Total Amount",
    "Cur Prv": "Current/Previous"
  },
  "hidden_columns": ["Ord"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"web_mapping": "session[comp_code]"},
    "user_id": {"web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL308';

-- Update FIN001 with available columns and visible property
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Period", "field": "M_FM_YYYYMM", "type": "text", "required": true, "default": "202501", "visible": true},
    {"name": "To Period", "field": "M_TO_YYYYMM", "type": "text", "required": true, "default": "202512", "visible": true},
    {"name": "From Division", "field": "M_FM_DIVN", "type": "text", "required": true, "default": "0", "visible": true},
    {"name": "To Division", "field": "M_TO_DIVN", "type": "text", "required": true, "default": "ZZZZZZ", "visible": true},
    {"name": "From Department", "field": "M_FM_DEPT", "type": "text", "required": true, "default": "0", "visible": true},
    {"name": "To Department", "field": "M_TO_DEPT", "type": "text", "required": true, "default": "ZZZZZZ", "visible": true},
    {"name": "From Main Account", "field": "M_FM_MAIN_AC", "type": "text", "required": true, "default": "0", "visible": true},
    {"name": "To Main Account", "field": "M_TO_MAIN_AC", "type": "text", "required": true, "default": "ZZZZZZ", "visible": true},
    {"name": "From Sub Account", "field": "M_FM_SUB_AC", "type": "text", "required": true, "default": "0", "visible": true},
    {"name": "To Sub Account", "field": "M_TO_SUB_AC", "type": "text", "required": true, "default": "ZZZZZZ", "visible": true}
  ],
  "display_columns": ["MAIN_ACNT_NAME", "SUB_ACNT_NAME", "OPN_BAL_AMT", "DR_AMT", "CR_AMT", "CLS_BAL_AMT"],
  "available_columns": ["ABAL_ACNT_YEAR", "ABAL_COMP_CODE", "ABAL_DEPT_CODE", "ABAL_DIVN_CODE", "ABAL_MAIN_ACNT_CODE", "ABAL_SUB_ACNT_CODE", "CLS_BAL_AMT", "CR_AMT", "DEPT_NAME", "DIVN_NAME", "DR_AMT", "MAIN_ACNT_NAME", "OPN_BAL_AMT", "PBC_SUB_ACNT_CODE", "SUB_ACNT_NAME"],
  "column_headers": {
    "ABAL_ACNT_YEAR": "Account Year",
    "ABAL_COMP_CODE": "Company Code",
    "ABAL_DEPT_CODE": "Department Code",
    "ABAL_DIVN_CODE": "Division Code",
    "ABAL_MAIN_ACNT_CODE": "Main Account Code",
    "ABAL_SUB_ACNT_CODE": "Sub Account Code",
    "CLS_BAL_AMT": "Closing Balance",
    "CR_AMT": "Credit Amount",
    "DEPT_NAME": "Department Name",
    "DIVN_NAME": "Division Name",
    "DR_AMT": "Debit Amount",
    "MAIN_ACNT_NAME": "Main Account Name",
    "OPN_BAL_AMT": "Opening Balance",
    "PBC_SUB_ACNT_CODE": "PBC Sub Account Code",
    "SUB_ACNT_NAME": "Sub Account Name"
  },
  "hidden_columns": ["ABAL_ACNT_YEAR", "ABAL_COMP_CODE"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap", "report_title": "Trial Balance Report"},
  "global_variables": {
    "comp_code": {"forms6i_mapping": ":GLOBAL.M_COMP_CODE", "web_mapping": "session[comp_code]"},
    "user_id": {"forms6i_mapping": ":GLOBAL.M_USER_ID", "web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'FIN001';

-- Update FIN006 with visible property
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {"name": "From Customer Code", "field": "from_cust_code", "type": "text", "required": false, "default": "0", "visible": true},
    {"name": "To Customer Code", "field": "to_cust_code", "type": "text", "required": false, "default": "ZZZZZZ", "visible": true},
    {"name": "As Of Date", "field": "as_of_date", "type": "date", "required": true, "default": "31/12/2024", "visible": true}
  ],
  "display_columns": ["SUB_AC", "SUB_AC_DESC", "UPTO_30_DAYS", "30_TO_60_DAYS", "60_TO_90_DAYS", "90_TO_120_DAYS", "ABOVE_120_DAYS", "NET_VAL"],
  "available_columns": ["MAIN_AC", "SUB_AC", "SUB_AC_DESC", "TERM_DAYS", "CURR", "ABOVE_120_DAYS", "90_TO_120_DAYS", "60_TO_90_DAYS", "30_TO_60_DAYS", "UPTO_30_DAYS", "NET_VAL", "CR_LIMIT"],
  "column_headers": {
    "30_TO_60_DAYS": "30-60 Days",
    "60_TO_90_DAYS": "60-90 Days", 
    "90_TO_120_DAYS": "90-120 Days",
    "ABOVE_120_DAYS": "Above 120 Days",
    "CR_LIMIT": "Credit Limit",
    "CURR": "Currency",
    "MAIN_AC": "Main Account",
    "NET_VAL": "Net Outstanding",
    "SUB_AC": "Customer Code",
    "SUB_AC_DESC": "Customer Name",
    "TERM_DAYS": "Payment Terms (Days)",
    "UPTO_30_DAYS": "Up to 30 Days"
  },
  "hidden_columns": ["MAIN_AC", "CURR"],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap", "report_title": "Customer Aging Analysis"},
  "global_variables": {
    "comp_code": {"web_mapping": "session[comp_code]"},
    "user_id": {"web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'FIN006';

COMMIT;