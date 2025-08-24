# ERP Application - Database Schema Documentation

## Oracle 11g XE Database Schema

### Connection Configuration
```
Host: localhost
Port: 1521
SID: XE
Driver: oracledb (thin mode)
Compatibility: Oracle 11g XE
```

---

## Core Tables

### 1. RPT_REPORT_MASTER
Primary table storing all report configurations.

```sql
CREATE TABLE RPT_REPORT_MASTER (
    RPT_ID VARCHAR2(20) CONSTRAINT PK_RPT_MASTER PRIMARY KEY,
    RPT_NAME VARCHAR2(100) NOT NULL,
    RPT_DESC VARCHAR2(500),
    RPT_TYPE VARCHAR2(10) NOT NULL CHECK (RPT_TYPE IN ('CLASS', 'SQL', 'PROCEDURE', 'TEMPLATE')),
    RPT_SOURCE CLOB,
    RPT_PARAMS CLOB,
    RPT_OUTPUT_FORMATS VARCHAR2(100) DEFAULT 'view,excel',
    RPT_CATEGORY VARCHAR2(50),
    RPT_ACTIVE_FLAG CHAR(1) DEFAULT 'Y' CHECK (RPT_ACTIVE_FLAG IN ('Y', 'N')),
    CREATED_BY VARCHAR2(30) DEFAULT USER,
    CREATED_DATE DATE DEFAULT SYSDATE,
    UPDATED_BY VARCHAR2(30),
    UPDATED_DATE DATE
);

-- Indexes
CREATE INDEX IDX_RPT_MASTER_TYPE ON RPT_REPORT_MASTER(RPT_TYPE);
CREATE INDEX IDX_RPT_MASTER_ACTIVE ON RPT_REPORT_MASTER(RPT_ACTIVE_FLAG);
CREATE INDEX IDX_RPT_MASTER_CATEGORY ON RPT_REPORT_MASTER(RPT_CATEGORY);

-- Comments
COMMENT ON TABLE RPT_REPORT_MASTER IS 'Master table for all report definitions and configurations';
COMMENT ON COLUMN RPT_REPORT_MASTER.RPT_ID IS 'Unique report identifier (e.g., FIN001, TTL715)';
COMMENT ON COLUMN RPT_REPORT_MASTER.RPT_SOURCE IS 'Python class name for CLASS reports, SQL query for SQL reports';
COMMENT ON COLUMN RPT_REPORT_MASTER.RPT_PARAMS IS 'JSON configuration containing parameters, columns, and metadata';
```

### 2. SYS_MENU_MASTER
Hierarchical menu structure for navigation.

```sql
CREATE TABLE SYS_MENU_MASTER (
    MENU_ID VARCHAR2(20) CONSTRAINT PK_MENU_MASTER PRIMARY KEY,
    MENU_NAME VARCHAR2(100) NOT NULL,
    PARENT_MENU_ID VARCHAR2(20),
    MENU_LEVEL NUMBER(2) DEFAULT 1,
    MENU_TYPE CHAR(1) DEFAULT 'M' CHECK (MENU_TYPE IN ('M', 'R', 'F')), -- Menu/Report/Form
    MENU_URL VARCHAR2(200),
    MENU_ORDER NUMBER(4) DEFAULT 0,
    ACTIVE_FLAG CHAR(1) DEFAULT 'Y' CHECK (ACTIVE_FLAG IN ('Y', 'N')),
    ICON_CLASS VARCHAR2(50),
    CREATED_BY VARCHAR2(30) DEFAULT USER,
    CREATED_DATE DATE DEFAULT SYSDATE,
    
    CONSTRAINT FK_MENU_PARENT FOREIGN KEY (PARENT_MENU_ID) REFERENCES SYS_MENU_MASTER(MENU_ID)
);

-- Indexes
CREATE INDEX IDX_MENU_PARENT ON SYS_MENU_MASTER(PARENT_MENU_ID);
CREATE INDEX IDX_MENU_LEVEL ON SYS_MENU_MASTER(MENU_LEVEL);
CREATE INDEX IDX_MENU_ORDER ON SYS_MENU_MASTER(MENU_ORDER);

-- Comments
COMMENT ON TABLE SYS_MENU_MASTER IS 'Hierarchical menu structure for application navigation';
COMMENT ON COLUMN SYS_MENU_MASTER.MENU_TYPE IS 'M=Menu Container, R=Report, F=Form';
```

### 3. SYS_USER_MASTER
User authentication and profile information.

```sql
CREATE TABLE SYS_USER_MASTER (
    USER_ID VARCHAR2(30) NOT NULL,
    COMP_CODE VARCHAR2(10) NOT NULL,
    USER_NAME VARCHAR2(100),
    PASSWORD_HASH VARCHAR2(255),
    EMAIL VARCHAR2(100),
    PHONE VARCHAR2(20),
    DEFAULT_BRANCH VARCHAR2(10),
    ACTIVE_FLAG CHAR(1) DEFAULT 'Y',
    LAST_LOGIN_DATE DATE,
    PASSWORD_EXPIRY_DATE DATE,
    FAILED_LOGIN_ATTEMPTS NUMBER(2) DEFAULT 0,
    ACCOUNT_LOCKED_FLAG CHAR(1) DEFAULT 'N',
    CREATED_BY VARCHAR2(30) DEFAULT USER,
    CREATED_DATE DATE DEFAULT SYSDATE,
    
    CONSTRAINT PK_USER_MASTER PRIMARY KEY (USER_ID, COMP_CODE)
);

-- Comments
COMMENT ON TABLE SYS_USER_MASTER IS 'User master data with authentication credentials';
```

### 4. SYS_COMPANY_MASTER
Company/organization master data.

```sql
CREATE TABLE SYS_COMPANY_MASTER (
    COMP_CODE VARCHAR2(10) CONSTRAINT PK_COMPANY_MASTER PRIMARY KEY,
    COMP_NAME VARCHAR2(100) NOT NULL,
    COMP_SHORT_NAME VARCHAR2(20),
    ADDRESS_LINE1 VARCHAR2(100),
    ADDRESS_LINE2 VARCHAR2(100),
    CITY VARCHAR2(50),
    STATE VARCHAR2(50),
    COUNTRY VARCHAR2(50),
    POSTAL_CODE VARCHAR2(20),
    PHONE VARCHAR2(20),
    EMAIL VARCHAR2(100),
    WEBSITE VARCHAR2(100),
    TAX_ID VARCHAR2(50),
    CURRENCY_CODE VARCHAR2(3) DEFAULT 'USD',
    ACTIVE_FLAG CHAR(1) DEFAULT 'Y',
    CREATED_BY VARCHAR2(30) DEFAULT USER,
    CREATED_DATE DATE DEFAULT SYSDATE
);

-- Comments
COMMENT ON TABLE SYS_COMPANY_MASTER IS 'Company master data for multi-company operations';
```

---

## Sample Data Scripts

### Insert Core Menu Structure
```sql
-- Root menus
INSERT INTO SYS_MENU_MASTER (MENU_ID, MENU_NAME, MENU_LEVEL, MENU_TYPE, MENU_ORDER, ICON_CLASS) 
VALUES ('FINANCIAL', 'Financial Reports', 1, 'M', 1, 'fas fa-chart-line');

INSERT INTO SYS_MENU_MASTER (MENU_ID, MENU_NAME, MENU_LEVEL, MENU_TYPE, MENU_ORDER, ICON_CLASS)
VALUES ('INVENTORY', 'Inventory Reports', 1, 'M', 2, 'fas fa-boxes');

INSERT INTO SYS_MENU_MASTER (MENU_ID, MENU_NAME, MENU_LEVEL, MENU_TYPE, MENU_ORDER, ICON_CLASS)
VALUES ('ADMIN', 'Administration', 1, 'M', 9, 'fas fa-cogs');

-- Financial report menus
INSERT INTO SYS_MENU_MASTER (MENU_ID, MENU_NAME, PARENT_MENU_ID, MENU_LEVEL, MENU_TYPE, MENU_URL, MENU_ORDER)
VALUES ('T020101', 'Trial Balance', 'FINANCIAL', 2, 'R', '/reports/:form_id/:id', 1);

INSERT INTO SYS_MENU_MASTER (MENU_ID, MENU_NAME, PARENT_MENU_ID, MENU_LEVEL, MENU_TYPE, MENU_URL, MENU_ORDER)
VALUES ('T030101', 'Profit & Loss', 'FINANCIAL', 2, 'R', '/reports/:form_id/:id', 2);

-- Admin menus
INSERT INTO SYS_MENU_MASTER (MENU_ID, MENU_NAME, PARENT_MENU_ID, MENU_LEVEL, MENU_TYPE, MENU_URL, MENU_ORDER)
VALUES ('A1020615', 'Reports Configurator', 'ADMIN', 2, 'F', '/reports/admin/', 1);

COMMIT;
```

### Insert Sample Reports
```sql
-- FIN001 - Trial Balance Report (CLASS type)
INSERT INTO RPT_REPORT_MASTER (
    RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_PARAMS,
    RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_ACTIVE_FLAG
) VALUES (
    'FIN001',
    'Trial Balance Report',
    'Trial Balance Report with GLOBAL variable support',
    'CLASS',
    'FIN001',
    '{
        "parameters": [
            {
                "field": "M_FM_YYYYMM",
                "name": "From Year-Month",
                "type": "text",
                "required": true,
                "default": "202501",
                "visible": true
            },
            {
                "field": "M_TO_YYYYMM", 
                "name": "To Year-Month",
                "type": "text",
                "required": true,
                "default": "202512",
                "visible": true
            },
            {
                "field": "CUR_PRV",
                "name": "Period Type",
                "type": "select",
                "required": true,
                "default": "C",
                "visible": true,
                "options": [
                    {"value": "C", "label": "Current Period"},
                    {"value": "P", "label": "Previous Period"}
                ]
            }
        ],
        "display_columns": [
            "MAIN_ACNT_NAME", "SUB_ACNT_NAME", "OP_BAL", 
            "MONTH_BAL_01", "MONTH_BAL_02", "MONTH_BAL_03", "CLO_BAL"
        ],
        "hidden_columns": [
            "ABAL_ACNT_YEAR", "ABAL_COMP_CODE", "ABAL_MAIN_ACNT_CODE",
            "ABAL_SUB_ACNT_CODE", "ABAL_DIVN_CODE", "ABAL_DEPT_CODE"
        ],
        "column_headers": {
            "MAIN_ACNT_NAME": "Main Account Name",
            "SUB_ACNT_NAME": "Sub Account Name",
            "OP_BAL": "Opening Balance",
            "MONTH_BAL_01": "Jan Balance",
            "MONTH_BAL_02": "Feb Balance",
            "MONTH_BAL_03": "Mar Balance",
            "CLO_BAL": "Closing Balance",
            "ABAL_ACNT_YEAR": "Account Year",
            "ABAL_COMP_CODE": "Company Code"
        },
        "global_variables": {
            "comp_code": {
                "forms6i_mapping": ":GLOBAL.M_COMP_CODE",
                "web_mapping": "session[comp_code]"
            },
            "user_id": {
                "forms6i_mapping": ":GLOBAL.M_USER_ID",
                "web_mapping": "session[user_id]"
            }
        },
        "ui_config": {
            "date_format": "DD/MM/YYYY",
            "theme": "bootstrap"
        }
    }',
    'view,excel',
    'FINANCIAL',
    'Y'
);

-- TTL715 - Pending Transactions (SQL type)
INSERT INTO RPT_REPORT_MASTER (
    RPT_ID, RPT_NAME, RPT_DESC, RPT_TYPE, RPT_SOURCE, RPT_PARAMS,
    RPT_OUTPUT_FORMATS, RPT_CATEGORY, RPT_ACTIVE_FLAG
) VALUES (
    'TTL715',
    'Transactions Pending For Approval',
    'Comprehensive report showing all types of transactions pending for approval',
    'SQL',
    'TTL715',
    '{
        "parameters": [
            {
                "default": "01/01/2024",
                "field": "FM_DT",
                "name": "From Date",
                "required": true,
                "type": "date",
                "visible": false
            },
            {
                "default": "31/12/2024",
                "field": "TO_DT",
                "name": "To Date",
                "required": true,
                "type": "date",
                "visible": true
            },
            {
                "default": "0",
                "field": "FM_TXN_CODE",
                "name": "From Transaction Code",
                "required": true,
                "type": "text",
                "visible": true
            },
            {
                "default": "ZZZZZZ",
                "field": "TO_TXN_CODE",
                "name": "To Transaction Code",
                "required": true,
                "type": "text", 
                "visible": true
            }
        ],
        "display_columns": [
            "TXN", "DT", "NUM", "LOCN", "CODE", "NAME", "ITEM", "TXN_TYPE", "UID"
        ],
        "column_headers": {
            "CODE": "Supplier/Customer Code",
            "DT": "Document Date",
            "ITEM": "Items Yes/No",
            "LOCN": "Location Code",
            "NAME": "Supplier/Customer Name",
            "NUM": "Document Number",
            "TXN": "Transaction Code",
            "TXN_TYPE": "Transaction Type",
            "UID": "Created By"
        },
        "hidden_columns": [],
        "ui_config": {
            "date_format": "DD/MM/YYYY",
            "theme": "bootstrap"
        },
        "global_variables": {
            "comp_code": {
                "forms6i_mapping": ":GLOBAL.M_COMP_CODE",
                "web_mapping": "session[comp_code]"
            },
            "user_id": {
                "forms6i_mapping": ":GLOBAL.M_USER_ID", 
                "web_mapping": "session[user_id]"
            }
        }
    }',
    'view,excel',
    'TRANSACTIONS',
    'Y'
);

COMMIT;
```

### Insert Sample Company Data
```sql
INSERT INTO SYS_COMPANY_MASTER (
    COMP_CODE, COMP_NAME, COMP_SHORT_NAME, CITY, COUNTRY, CURRENCY_CODE
) VALUES (
    'TTM', 'Tech Solutions Inc', 'TTM', 'New York', 'USA', 'USD'
);

INSERT INTO SYS_COMPANY_MASTER (
    COMP_CODE, COMP_NAME, COMP_SHORT_NAME, CITY, COUNTRY, CURRENCY_CODE  
) VALUES (
    'ABC', 'ABC Corporation', 'ABC', 'London', 'UK', 'GBP'
);

COMMIT;
```

### Insert Sample Users
```sql
-- Default admin user (password: admin)
INSERT INTO SYS_USER_MASTER (
    USER_ID, COMP_CODE, USER_NAME, PASSWORD_HASH, EMAIL, ACTIVE_FLAG
) VALUES (
    'ADMIN', 'TTM', 'System Administrator', 
    'admin', -- In production, use proper password hashing
    'admin@company.com', 'Y'
);

INSERT INTO SYS_USER_MASTER (
    USER_ID, COMP_CODE, USER_NAME, PASSWORD_HASH, EMAIL, ACTIVE_FLAG
) VALUES (
    'ORION', 'TTM', 'Orion User',
    'orion123',  -- In production, use proper password hashing
    'orion@company.com', 'Y'
);

COMMIT;
```

---

## Database Views

### RPT_ACTIVE_REPORTS
View showing only active reports with formatted information.

```sql
CREATE OR REPLACE VIEW RPT_ACTIVE_REPORTS AS
SELECT 
    RPT_ID,
    RPT_NAME,
    RPT_DESC,
    RPT_TYPE,
    CASE RPT_TYPE 
        WHEN 'CLASS' THEN 'Python Class'
        WHEN 'SQL' THEN 'SQL Query'
        WHEN 'PROCEDURE' THEN 'Database Procedure'
        ELSE RPT_TYPE
    END as RPT_TYPE_DESC,
    RPT_CATEGORY,
    TO_CHAR(CREATED_DATE, 'DD-MON-YYYY') as CREATED_DATE_FORMAT,
    CREATED_BY,
    CASE 
        WHEN DBMS_LOB.GETLENGTH(RPT_PARAMS) > 0 THEN 'Y'
        ELSE 'N'
    END as HAS_PARAMETERS
FROM RPT_REPORT_MASTER
WHERE RPT_ACTIVE_FLAG = 'Y'
ORDER BY RPT_CATEGORY, RPT_ID;

-- Grant access
GRANT SELECT ON RPT_ACTIVE_REPORTS TO PUBLIC;
```

### SYS_MENU_HIERARCHY
Hierarchical view of menu structure with full path.

```sql
CREATE OR REPLACE VIEW SYS_MENU_HIERARCHY AS
WITH menu_hierarchy AS (
    -- Root level menus
    SELECT 
        MENU_ID,
        MENU_NAME,
        PARENT_MENU_ID,
        MENU_LEVEL,
        MENU_TYPE,
        MENU_URL,
        MENU_ORDER,
        MENU_NAME as FULL_PATH,
        ACTIVE_FLAG
    FROM SYS_MENU_MASTER
    WHERE PARENT_MENU_ID IS NULL
    
    UNION ALL
    
    -- Child menus  
    SELECT 
        m.MENU_ID,
        m.MENU_NAME,
        m.PARENT_MENU_ID,
        m.MENU_LEVEL,
        m.MENU_TYPE,
        m.MENU_URL,
        m.MENU_ORDER,
        h.FULL_PATH || ' > ' || m.MENU_NAME,
        m.ACTIVE_FLAG
    FROM SYS_MENU_MASTER m
    JOIN menu_hierarchy h ON m.PARENT_MENU_ID = h.MENU_ID
)
SELECT * FROM menu_hierarchy
WHERE ACTIVE_FLAG = 'Y'
ORDER BY MENU_LEVEL, MENU_ORDER;
```

---

## Database Functions and Procedures

### Function: GET_REPORT_PARAM_COUNT
```sql
CREATE OR REPLACE FUNCTION GET_REPORT_PARAM_COUNT(p_report_id VARCHAR2)
RETURN NUMBER
IS
    v_param_count NUMBER := 0;
    v_rpt_params CLOB;
    v_json_obj JSON_OBJECT_T;
    v_params_array JSON_ARRAY_T;
BEGIN
    -- Get RPT_PARAMS
    SELECT RPT_PARAMS INTO v_rpt_params
    FROM RPT_REPORT_MASTER
    WHERE RPT_ID = p_report_id AND RPT_ACTIVE_FLAG = 'Y';
    
    -- Parse JSON and count parameters
    v_json_obj := JSON_OBJECT_T(v_rpt_params);
    v_params_array := v_json_obj.get_Array('parameters');
    v_param_count := v_params_array.get_size();
    
    RETURN v_param_count;
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0;
    WHEN OTHERS THEN
        RETURN -1;
END;
/
```

### Procedure: UPDATE_REPORT_ACCESS_LOG
```sql
CREATE OR REPLACE PROCEDURE UPDATE_REPORT_ACCESS_LOG(
    p_report_id VARCHAR2,
    p_user_id VARCHAR2,
    p_comp_code VARCHAR2,
    p_execution_time NUMBER DEFAULT NULL
)
IS
BEGIN
    INSERT INTO RPT_ACCESS_LOG (
        REPORT_ID, USER_ID, COMP_CODE, ACCESS_TIME, EXECUTION_TIME_MS
    ) VALUES (
        p_report_id, p_user_id, p_comp_code, SYSDATE, p_execution_time
    );
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/
```

---

## Performance Optimization

### Recommended Indexes
```sql
-- RPT_REPORT_MASTER performance indexes
CREATE INDEX IDX_RPT_MASTER_COMPOUND ON RPT_REPORT_MASTER(RPT_TYPE, RPT_ACTIVE_FLAG, RPT_CATEGORY);

-- Menu performance indexes  
CREATE INDEX IDX_MENU_COMPOUND ON SYS_MENU_MASTER(ACTIVE_FLAG, MENU_LEVEL, MENU_ORDER);

-- User authentication performance
CREATE INDEX IDX_USER_LOGIN ON SYS_USER_MASTER(USER_ID, COMP_CODE, ACTIVE_FLAG);
```

### Table Statistics
```sql
-- Update table statistics for better query performance
BEGIN
    DBMS_STATS.GATHER_TABLE_STATS(USER, 'RPT_REPORT_MASTER');
    DBMS_STATS.GATHER_TABLE_STATS(USER, 'SYS_MENU_MASTER');
    DBMS_STATS.GATHER_TABLE_STATS(USER, 'SYS_USER_MASTER');
    DBMS_STATS.GATHER_TABLE_STATS(USER, 'SYS_COMPANY_MASTER');
END;
/
```

---

## Backup and Recovery

### Export Essential Data
```bash
# Export report configurations
exp username/password@XE tables=RPT_REPORT_MASTER file=reports_backup.dmp

# Export menu structure
exp username/password@XE tables=SYS_MENU_MASTER file=menus_backup.dmp

# Full schema export
exp username/password@XE owner=username file=full_schema_backup.dmp
```

### Recovery Commands
```bash
# Import report configurations
imp username/password@XE tables=RPT_REPORT_MASTER file=reports_backup.dmp

# Import menu structure  
imp username/password@XE tables=SYS_MENU_MASTER file=menus_backup.dmp
```

---

## Data Validation Queries

### Check Report Configuration Integrity
```sql
-- Reports with missing or invalid RPT_PARAMS
SELECT RPT_ID, RPT_NAME, 
       CASE 
           WHEN RPT_PARAMS IS NULL THEN 'NULL'
           WHEN DBMS_LOB.GETLENGTH(RPT_PARAMS) = 0 THEN 'EMPTY'
           ELSE 'OK'
       END as PARAM_STATUS
FROM RPT_REPORT_MASTER
WHERE RPT_ACTIVE_FLAG = 'Y'
AND (RPT_PARAMS IS NULL OR DBMS_LOB.GETLENGTH(RPT_PARAMS) = 0);
```

### Check Menu Hierarchy Integrity
```sql
-- Orphaned menu items (parent doesn't exist)
SELECT m1.MENU_ID, m1.MENU_NAME, m1.PARENT_MENU_ID
FROM SYS_MENU_MASTER m1
LEFT JOIN SYS_MENU_MASTER m2 ON m1.PARENT_MENU_ID = m2.MENU_ID
WHERE m1.PARENT_MENU_ID IS NOT NULL 
AND m2.MENU_ID IS NULL
AND m1.ACTIVE_FLAG = 'Y';
```

### Check User Access Integrity
```sql
-- Users without valid company mapping
SELECT u.USER_ID, u.COMP_CODE, u.USER_NAME
FROM SYS_USER_MASTER u
LEFT JOIN SYS_COMPANY_MASTER c ON u.COMP_CODE = c.COMP_CODE
WHERE c.COMP_CODE IS NULL
AND u.ACTIVE_FLAG = 'Y';
```

This database schema documentation provides complete coverage of the Oracle 11g XE database structure supporting the ERP application, including all tables, sample data, views, functions, and maintenance procedures.