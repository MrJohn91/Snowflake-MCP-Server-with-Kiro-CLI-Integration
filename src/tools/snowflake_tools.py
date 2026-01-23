"""Core Snowflake MCP tools for natural language querying."""

import logging
from typing import Any, Dict, List, Optional

import snowflake.connector
from snowflake.connector import DictCursor

from src import config, mock_data
from src.config import get_snowflake_config

# Set up logging
logger = logging.getLogger(__name__)

# Initialize configuration state (detect Mock Mode)
config.validate_config()


def get_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    """Create and return a Snowflake connection."""
    try:
        config = get_snowflake_config()
        # If in Mock Mode, this returns empty dict, so we shouldn't even get here 
        # because the tools check MOCK_MODE first.
        conn = snowflake.connector.connect(**config)
        logger.info("Successfully connected to Snowflake")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {e}")
        raise


def query_snowflake(query: str, limit: int = 100) -> Dict[str, Any]:
    """
    Execute a SQL query against Snowflake and return results.

    Args:
        query: SQL query to execute
        limit: Maximum number of rows to return (default: 100)

    Returns:
        Dictionary with success status, data, and metadata
    """
    if config.MOCK_MODE:
        logger.info(f"MOCK MODE: Returning simulated data for query: {query}")
        query_upper = query.upper()
        
        # Simple heuristic to return relevant mock data
        if "GROUP BY TRANSACTION_DATE" in query_upper:
            return mock_data.SAMPLE_DAILY_TREND
        else:
            # Default to Category Sales (most common request)
            return mock_data.SAMPLE_CATEGORY_SALES

    try:
        # Input validation
        if not query or not query.strip():
            return {"success": False, "error": "Query cannot be empty"}

        # Ensure limit is reasonable
        limit = min(max(1, limit), 1000)  # Between 1 and 1000

        # Add LIMIT clause if not present
        query_upper = query.upper().strip()
        if not query_upper.endswith(";"):
            query = query.strip()
        if "LIMIT" not in query_upper:
            query = f"{query.rstrip(';')} LIMIT {limit}"

        conn = get_snowflake_connection()

        try:
            cursor = conn.cursor(DictCursor)
            cursor.execute(query)

            # Fetch results
            results = cursor.fetchall()

            # Get column information
            columns = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )

            return {
                "success": True,
                "data": {
                    "rows": results,
                    "columns": columns,
                    "row_count": len(results),
                    "query": query,
                },
            }

        finally:
            cursor.close()
            conn.close()

    except snowflake.connector.errors.ProgrammingError as e:
        logger.error(f"Snowflake query error: {e}")
        return {"success": False, "error": f"Query error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error in query_snowflake: {e}")
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


def list_views(schema: Optional[str] = None) -> Dict[str, Any]:
    """
    List all available views in the specified schema or current schema.

    Args:
        schema: Schema name (optional, defaults to configured schema)

    Returns:
        Dictionary with success status and list of views
    """
    if config.MOCK_MODE:
        logger.info("MOCK MODE: Returning simulated views list")
        return mock_data.LIST_VIEWS_RESPONSE

    try:
        conn = get_snowflake_connection()

        try:
            cursor = conn.cursor(DictCursor)

            views = []
            
            # Get views (GOLD schema uses views)
            if schema:
                query = f"SHOW VIEWS IN SCHEMA {schema}"
            else:
                query = "SHOW VIEWS"

            cursor.execute(query)
            view_results = cursor.fetchall()

            for row in view_results:
                view_info = {
                    "name": row.get("name"),
                    "schema": row.get("schema_name"),
                    "database": row.get("database_name"),
                    "kind": "VIEW",
                    "created_on": str(row.get("created_on"))
                    if row.get("created_on")
                    else None,
                }
                views.append(view_info)

            return {
                "success": True,
                "data": {
                    "views": views,
                    "count": len(views),
                    "schema": schema or "current",
                },
            }

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"Error listing views: {e}")
        return {"success": False, "error": f"Failed to list views: {str(e)}"}


def describe_view(view_name: str, schema: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed information about a specific view including columns and metadata.

    Args:
        view_name: Name of the view to describe
        schema: Schema name (optional, defaults to configured schema)

    Returns:
        Dictionary with success status and view description
    """
    if config.MOCK_MODE:
        logger.info(f"MOCK MODE: Returning simulated info for view {view_name}")
        return mock_data.DESCRIBE_DAILY_SALES

    try:
        if not view_name or not view_name.strip():
            return {"success": False, "error": "View name cannot be empty"}

        conn = get_snowflake_connection()

        try:
            cursor = conn.cursor(DictCursor)

            # Build view reference
            if schema:
                full_view_name = f"{schema}.{view_name}"
            else:
                full_view_name = view_name

            # Get column information
            cursor.execute(f"DESCRIBE VIEW {full_view_name}")
            columns_result = cursor.fetchall()

            # Get view metadata
            cursor.execute(
                f"SHOW VIEWS LIKE '{view_name}'"
                + (f" IN SCHEMA {schema}" if schema else "")
            )
            view_metadata = cursor.fetchone()

            # Process column information
            columns = []
            for col in columns_result:
                column_info = {
                    "name": col.get("name"),
                    "type": col.get("type"),
                    "kind": col.get("kind"),
                    "null": col.get("null?") == "Y",
                    "default": col.get("default"),
                    "primary_key": col.get("primary key") == "Y",
                    "unique_key": col.get("unique key") == "Y",
                    "check": col.get("check"),
                    "expression": col.get("expression"),
                    "comment": col.get("comment"),
                }
                columns.append(column_info)

            # Process view metadata
            metadata = {}
            if view_metadata:
                metadata = {
                    "name": view_metadata.get("name"),
                    "schema": view_metadata.get("schema_name"),
                    "database": view_metadata.get("database_name"),
                    "kind": "VIEW",
                    "created_on": str(view_metadata.get("created_on"))
                    if view_metadata.get("created_on")
                    else None,
                    "comment": view_metadata.get("comment"),
                }

            return {
                "success": True,
                "data": {
                    "view": full_view_name,
                    "columns": columns,
                    "metadata": metadata,
                    "column_count": len(columns),
                },
            }

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"Error describing view {view_name}: {e}")
        return {"success": False, "error": f"Failed to describe view: {str(e)}"}
