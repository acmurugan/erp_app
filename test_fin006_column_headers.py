#!/usr/bin/env python3
"""
Test script to check FIN006 column headers processing
"""

import json
from reports.class_executor import get_display_columns

# Test the column headers configuration that should match FIN006
test_columns = [
    'MAIN_AC', 'SUB_AC', 'SUB_AC_DESC', 'TERM_DAYS', 'CURR',
    'ABOVE_120_DAYS', '90_TO_120_DAYS', '60_TO_90_DAYS', '30_TO_60_DAYS', 'UPTO_30_DAYS', 
    'NET_VAL', 'CR_LIMIT'
]

test_rpt_params = {
    "parameters": [
        {
            "name": "As of Date", 
            "field": "as_of_date", 
            "type": "date", 
            "required": True, 
            "default": "24/08/2025"
        }
    ],
    "display_columns": [
        "MAIN_AC", "SUB_AC", "SUB_AC_DESC", "TERM_DAYS", "CURR", 
        "ABOVE_120_DAYS", "90_TO_120_DAYS", "60_TO_90_DAYS", "30_TO_60_DAYS", "UPTO_30_DAYS", 
        "NET_VAL", "CR_LIMIT"
    ],
    "column_headers": {
        "MAIN_AC": "Main Account",
        "SUB_AC": "Customer Code", 
        "SUB_AC_DESC": "Customer Name",
        "TERM_DAYS": "Payment Terms (Days)",
        "CURR": "Currency",
        "ABOVE_120_DAYS": "Above 120 Days",
        "90_TO_120_DAYS": "90-120 Days",
        "60_TO_90_DAYS": "60-90 Days", 
        "30_TO_60_DAYS": "30-60 Days",
        "UPTO_30_DAYS": "Up to 30 Days",
        "NET_VAL": "Net Outstanding",
        "CR_LIMIT": "Credit Limit"
    },
    "hidden_columns": []
}

print("=== FIN006 Column Headers Test ===")
print(f"Test columns: {test_columns}")

# Test the get_display_columns function
try:
    display_columns, column_headers = get_display_columns(test_rpt_params, test_columns)
    
    print(f"\nResults:")
    print(f"Display columns: {display_columns}")
    print(f"Column headers: {column_headers}")
    print(f"Display columns == test columns: {display_columns == test_columns}")
    print(f"Column headers count: {len(column_headers)}")
    
    # Test specific column header mappings
    for col in ['MAIN_AC', 'SUB_AC_DESC', 'NET_VAL']:
        if col in column_headers:
            print(f"✓ {col} → {column_headers[col]}")
        else:
            print(f"✗ Missing header for {col}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== JSON Configuration ===")
json_config = json.dumps(test_rpt_params, indent=2)
print("RPT_PARAMS JSON to update in database:")
print(json_config)