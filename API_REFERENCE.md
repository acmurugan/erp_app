# ERP Application - API Reference

## Authentication APIs

### POST /login
Login user and create session.

**Request:**
```json
{
    "comp_code": "TTM",
    "user_id": "ADMIN", 
    "password": "admin",
    "branch_code": "001"
}
```

**Response (Success):**
```json
{
    "success": true,
    "message": "Login successful",
    "redirect": "/dashboard"
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "Invalid credentials"
}
```

---

## Report Management APIs

### GET /reports/admin/config/{report_id}
Get report configuration.

**Parameters:**
- `report_id` (string): Report identifier (e.g., "FIN001", "TTL715")

**Response:**
```json
{
    "success": true,
    "data": {
        "rpt_id": "FIN001",
        "rpt_name": "Trial Balance Report",
        "rpt_type": "CLASS",
        "rpt_source": "FIN001", 
        "rpt_params": {
            "parameters": [...],
            "display_columns": [...],
            "hidden_columns": [...],
            "column_headers": {...}
        }
    }
}
```

### PUT /reports/admin/config/{report_id}
Update report configuration.

**Request Body:**
```json
{
    "rpt_id": "FIN001",
    "rpt_name": "Updated Report Name",
    "rpt_type": "CLASS",
    "rpt_source": "FIN001",
    "rpt_params": {
        "parameters": [
            {
                "field": "fm_dt",
                "name": "From Date",
                "type": "date",
                "required": true,
                "visible": true,
                "default": "01/01/2024"
            }
        ],
        "display_columns": ["COL1", "COL2"],
        "hidden_columns": ["COL3"],
        "column_headers": {
            "COL1": "Column 1 Display Name"
        }
    }
}
```

**Response:**
```json
{
    "success": true,
    "message": "Report updated successfully"
}
```

### POST /reports/{report_id}/{menu_id}/generate
Generate report with parameters.

**Form Data:**
```
menu_id: T020101
report_id: FIN001
fm_dt: 01/01/2024
to_dt: 31/12/2024
outputFormat: view|excel|pdf
```

**Response (View):** HTML report display
**Response (Excel):** Binary Excel file download
**Response (Error):**
```json
{
    "error": "Parameter validation failed",
    "details": "Missing required parameter: fm_dt"
}
```

---

## Data Formats

### RPT_PARAMS JSON Schema
```json
{
    "type": "object",
    "properties": {
        "parameters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "name": {"type": "string"},
                    "type": {"enum": ["text", "date", "number", "select"]},
                    "required": {"type": "boolean"},
                    "visible": {"type": "boolean"},
                    "default": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"},
                                "label": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["field", "name", "type"]
            }
        },
        "display_columns": {
            "type": "array",
            "items": {"type": "string"}
        },
        "hidden_columns": {
            "type": "array", 
            "items": {"type": "string"}
        },
        "column_headers": {
            "type": "object",
            "patternProperties": {
                "^[A-Z_]+$": {"type": "string"}
            }
        },
        "global_variables": {
            "type": "object",
            "properties": {
                "comp_code": {
                    "type": "object",
                    "properties": {
                        "forms6i_mapping": {"type": "string"},
                        "web_mapping": {"type": "string"}
                    }
                }
            }
        }
    },
    "required": ["parameters"]
}
```

---

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid request format or missing parameters |
| 401 | Unauthorized | User not logged in or session expired |
| 404 | Not Found | Report ID not found or resource doesn't exist |
| 500 | Internal Server Error | Database connection error or server exception |
| 1001 | Parameter Validation Failed | Required parameter missing or invalid format |
| 1002 | Report Execution Failed | Error during report generation |
| 1003 | Database Query Failed | SQL execution error or Oracle exception |

---

## Rate Limits

- **Report Generation**: 10 requests per minute per user
- **Admin Updates**: 20 requests per minute per user  
- **Login Attempts**: 5 attempts per minute per IP

---

## Response Headers

All API responses include:
```
Content-Type: application/json
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
X-Session-Timeout: 1800
```