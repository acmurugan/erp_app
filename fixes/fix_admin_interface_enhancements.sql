-- =============================================================================
-- POPULATE DISPLAY COLUMNS FOR ALL REPORTS IN ADMIN INTERFACE
-- =============================================================================

-- Update FIN001 with display columns (if not already set)
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"display_columns": ["Customer Code", "Customer Name", "Due Days", "Current", "Days 1-30", "Days 31-60", "Days 61-90", "Over 90", "Total Outstanding"]}'
)
WHERE RPT_ID = 'FIN001' AND JSON_VALUE(RPT_PARAMS, '$.display_columns') IS NULL;

-- Update TTL202 with display columns (if not already set)
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"display_columns": ["Sd Cust Name", "Item Name", "Sm Name", "Sd Dt", "Qty", "Sales Val", "Sd Item Code", "Class Name", "Brand Name"]}'
)
WHERE RPT_ID = 'TTL202' AND JSON_VALUE(RPT_PARAMS, '$.display_columns') IS NULL;

-- Update TTL308 with display columns (if not already set)  
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"display_columns": ["Head", "Gh Amt", "Vat Amt", "Total Amt", "Cur Prv"]}'
)
WHERE RPT_ID = 'TTL308' AND JSON_VALUE(RPT_PARAMS, '$.display_columns') IS NULL;

-- Update TTL715 with display columns (if not already set)
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"display_columns": ["DT", "TXN", "NUM", "LOCN", "CODE", "NAME", "ITEM", "TXN_TYPE", "UID"]}'
)
WHERE RPT_ID = 'TTL715' AND JSON_VALUE(RPT_PARAMS, '$.display_columns') IS NULL;

-- Update TTL201 with display columns (if not already set)
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"display_columns": ["Customer Name", "Customer Code", "SM Name", "Sale Date", "Transaction No", "Item Name", "Item Code", "Quantity", "Item Value", "Sales Value"]}'
)
WHERE RPT_ID = 'TTL201' AND JSON_VALUE(RPT_PARAMS, '$.display_columns') IS NULL;

-- Update FIN006 with display columns (if not already set)
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"display_columns": ["Customer Code", "Customer Name", "Current", "Days 1-30", "Days 31-60", "Days 61-90", "Over 90", "Total Outstanding"]}'
)
WHERE RPT_ID = 'FIN006' AND JSON_VALUE(RPT_PARAMS, '$.display_columns') IS NULL;

COMMIT;

-- =============================================================================
-- ADD AVAILABLE COLUMNS CONFIGURATION FOR REPORTS
-- =============================================================================

-- Add available_columns to all reports so admin interface can populate the Available Columns box
UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"available_columns": ["Customer Code", "Customer Name", "Due Days", "Current", "Days 1-30", "Days 31-60", "Days 61-90", "Over 90", "Total Outstanding", "Credit Limit", "Balance"]}'
)
WHERE RPT_ID = 'FIN001';

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"available_columns": ["Sd Comp Code", "Sd Dt", "Sd Txn No", "Sd Txn Type", "Item Name", "Item Cost Level", "Item Stk Yn Num", "Sd Del Locn Code", "Locn Group Code", "Sd Item Code", "Sd Grade Code", "Sd Cust Code", "Sd Cust Name", "Sm Code", "Sm Name", "Sd Sale Locn Code", "Class Name", "Brand Name", "Manf Name", "Tbu", "Catg Name", "Rim Size", "Rad Bias", "Pr Line", "Manf Grp", "Sales Name", "Cos Name", "Tyre Size", "Old Catg", "Gyr Vcode", "Gyr Ig", "Qty", "Item Val", "Disc Val", "Vat Val", "Exp Val", "Doc Status", "Cost", "Sales Val", "Excl Vat", "Yyyymm", "Cust Type"]}'
)
WHERE RPT_ID = 'TTL202';

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"available_columns": ["Ord", "Head", "Gh Amt", "Vat Amt", "Total Amt", "Cur Prv"]}'
)
WHERE RPT_ID = 'TTL308';

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"available_columns": ["ORD", "SYS_ID", "DT", "TXN", "NUM", "LOCN", "CODE", "NAME", "ITEM", "TXN_TYPE", "UID"]}'
)
WHERE RPT_ID = 'TTL715';

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"available_columns": ["Customer Name", "Customer Code", "SM Code", "SM Name", "Sale Date", "Transaction No", "Location Code", "Item Code", "Item Name", "Grade Code", "Class Name", "Brand Name", "Manufacturer Name", "TBU", "Category Name", "Rim Size", "Radial Bias", "Product Line", "Manufacturer Group", "Sales Name", "COS Name", "Tyre Size", "Old Category", "GYR VCODE", "GYR IG", "Quantity", "Item Value", "Discount Value", "VAT Value", "Cost", "Sales Value", "Excl VAT", "Contribution", "Margin %", "YYYYMM", "Customer Type"]}'
)
WHERE RPT_ID = 'TTL201';

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = JSON_MERGE_PATCH(
    RPT_PARAMS,
    '{"available_columns": ["Customer Code", "Customer Name", "Due Days", "Current", "Days 1-30", "Days 31-60", "Days 61-90", "Over 90", "Total Outstanding", "Credit Limit", "Balance"]}'
)
WHERE RPT_ID = 'FIN006';

COMMIT;