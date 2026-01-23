"""
Mock data for the Snowflake MCP server.
This data is identical to the production GOLD schema views.
Used for judge testing when Snowflake credentials are not active.
"""

# 1. View Definitions
LIST_VIEWS_RESPONSE = {
    "success": True,
    "data": {
        "views": [
            {
                "name": "DAILY_SALES_SUMMARY",
                "schema": "GOLD",
                "database": "PACIFICRETAIL",
                "kind": "VIEW",
                "created_on": "2025-07-01 11:53:42.699000-07:00",
            },
            {
                "name": "CUSTOMER_PRODUCT_AFFINITY_MONTHLY",
                "schema": "GOLD",
                "database": "PACIFICRETAIL",
                "kind": "VIEW",
                "created_on": "2025-07-03 10:56:22.573000-07:00",
            },
        ],
        "count": 2,
        "schema": "GOLD",
    },
}

# 2. Schema Definitions
DESCRIBE_DAILY_SALES = {
    "success": True,
    "data": {
        "view": "DAILY_SALES_SUMMARY",
        "columns": [
            {"name": "TRANSACTION_DATE", "type": "DATE", "kind": "COLUMN"},
            {"name": "PRODUCT_CATEGORY", "type": "VARCHAR(255)", "kind": "COLUMN"},
            {"name": "PRODUCT_NAME", "type": "VARCHAR(255)", "kind": "COLUMN"},
            {"name": "TOTAL_REVENUE", "type": "NUMBER(38,2)", "kind": "COLUMN"},
            {"name": "TOTAL_QUANTITY_SOLD", "type": "NUMBER(38,0)", "kind": "COLUMN"},
        ],
        "column_count": 5,
    },
}

# 3. Sample Data (Sales by Category)
SAMPLE_CATEGORY_SALES = {
    "success": True,
    "data": {
        "rows": [
            {"PRODUCT_CATEGORY": "Electronics", "REVENUE": 45320.50},
            {"PRODUCT_CATEGORY": "Garden", "REVENUE": 32100.75},
            {"PRODUCT_CATEGORY": "Food", "REVENUE": 28540.20},
            {"PRODUCT_CATEGORY": "Home", "REVENUE": 15200.10},
            {"PRODUCT_CATEGORY": "Clothing", "REVENUE": 12450.00},
        ],
        "columns": ["PRODUCT_CATEGORY", "REVENUE"],
        "row_count": 5,
    },
}

# 4. Sample Data (Daily Trend)
SAMPLE_DAILY_TREND = {
    "success": True,
    "data": {
        "rows": [
            {"TRANSACTION_DATE": "2023-12-01", "REVENUE": 5200.00},
            {"TRANSACTION_DATE": "2023-12-02", "REVENUE": 4800.00},
            {"TRANSACTION_DATE": "2023-12-03", "REVENUE": 6100.00},
            {"TRANSACTION_DATE": "2023-12-04", "REVENUE": 5900.00},
            {"TRANSACTION_DATE": "2023-12-05", "REVENUE": 7200.00},
        ],
        "columns": ["TRANSACTION_DATE", "REVENUE"],
        "row_count": 5,
    },
}
