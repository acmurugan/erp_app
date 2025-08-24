-- =============================================================================
-- MINIMAL TTL308 CONFIGURATION - EXACT CLASS MATCH
-- =============================================================================

UPDATE RPT_REPORT_MASTER 
SET RPT_PARAMS = '{
  "parameters": [
    {
      "name": "From Date", 
      "field": "from_date", 
      "type": "date", 
      "required": true, 
      "default": "01/01/2024"
    },
    {
      "name": "To Date", 
      "field": "to_date", 
      "type": "date", 
      "required": true, 
      "default": "31/12/2024"
    },
    {
      "name": "Period", 
      "field": "cur_prv", 
      "type": "select", 
      "required": true, 
      "default": "C",
      "options": [
        {"value": "C", "text": "Current"}, 
        {"value": "P", "text": "Previous"}
      ]
    }
  ],
  "display_columns": [],
  "column_headers": {},
  "hidden_columns": [],
  "ui_config": {"date_format": "DD/MM/YYYY", "theme": "bootstrap"},
  "global_variables": {
    "comp_code": {"web_mapping": "session[comp_code]"},
    "user_id": {"web_mapping": "session[user_id]"}
  }
}'
WHERE RPT_ID = 'TTL308';

COMMIT;