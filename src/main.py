"""FastMCP server entry point for Snowflake integration."""

import asyncio
import logging
from typing import Any, Dict, Optional

import requests
from fastmcp import Context, FastMCP

from src.config import FLASK_HOST, FLASK_PORT
from src.tools.snowflake_tools import describe_view, list_views, query_snowflake

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("snowflake-mcp-server")


@mcp.tool(
    name="snowflake_query",
    description="Execute a SQL query against Snowflake database.",
)
def snowflake_query(query: str, limit: int = 100) -> Dict[str, Any]:
    """
    Execute a SQL query against Snowflake database.

    Args:
        query: SQL query to execute against Snowflake
        limit: Maximum number of rows to return (1-1000, default: 100)

    Returns:
        Query results with success status, data rows, columns, and metadata
    """
    logger.info(f"Executing Snowflake query with limit {limit}")
    return query_snowflake(query, limit)


@mcp.tool(
    name="snowflake_list_views",
    description="List all available views in the specified Snowflake schema.",
)
def snowflake_list_views(schema: Optional[str] = None) -> Dict[str, Any]:
    """
    List all available views in the specified Snowflake schema.

    Args:
        schema: Schema name (optional, uses configured schema if not provided)

    Returns:
        List of views with metadata including name, schema, database, row count, and size
    """
    logger.info(f"Listing views in schema: {schema or 'default'}")
    return list_views(schema)


@mcp.tool(
    name="snowflake_describe_view",
    description="Get detailed information about a specific Snowflake view.",
)
def snowflake_describe_view(
    view_name: str, schema: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific Snowflake view.

    Args:
        view_name: Name of the view to describe
        schema: Schema name (optional, uses configured schema if not provided)

    Returns:
        View description including columns, data types, and metadata
    """
    logger.info(f"Describing view: {view_name} in schema: {schema or 'default'}")
    return describe_view(view_name, schema)


@mcp.tool(
    name="create_chart",
    description="Generates a browser-based chart. USE ONLY WHEN EXPLICITLY REQUESTED BY USER. Do not call this automatically after a query.",
)
def create_chart(
    data: list,
    chart_type: str = "bar",
    x_column: str = "",
    y_column: str = "",
    title: str = "Data Visualization",
) -> Dict[str, Any]:
    """
    Create an interactive chart from query results and open it in the browser.

    Args:
        data: List of dictionaries containing the data to visualize
        chart_type: Type of chart (bar, line, pie, scatter, doughnut)
        x_column: Column name for X-axis/labels
        y_column: Column name for Y-axis/values
        title: Chart title

    Returns:
        Chart creation result with file path
    """
    try:
        logger.info(f"Creating {chart_type} chart with {len(data)} data points")

        # Validate inputs
        if not data:
            return {"success": False, "error": "No data provided for chart"}

        if not x_column or not y_column:
            return {
                "success": False,
                "error": "Both x_column and y_column are required",
            }

        # Use the visualize module to generate static HTML
        from src.visualize import generate_chart_html
        
        result = generate_chart_html(
            data=data,
            chart_type=chart_type,
            x_column=x_column,
            y_column=y_column,
            title=title,
            open_browser=True,  # Explicitly open for Agent tool calls
        )
        
        if result.get("success"):
            logger.info(f"Chart created: {result.get('file_path')}")
        else:
            logger.error(f"Chart creation failed: {result.get('error')}")
            
        return result

    except Exception as e:
        error_msg = f"Error creating chart: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


@mcp.tool(
    name="get_chart_url",
    description="Get the URL for a previously created chart (Flask mode only).",
)
def get_chart_url(chart_id: str) -> Dict[str, Any]:
    """
    Get the URL for a previously created chart.

    Args:
        chart_id: Unique identifier for the chart

    Returns:
        Chart URL and metadata
    """
    try:
        logger.info(f"Getting URL for chart: {chart_id}")

        # Check if chart exists
        flask_url = f"http://{FLASK_HOST}:{FLASK_PORT}/charts/{chart_id}/data"
        response = requests.get(flask_url, timeout=5)

        if response.status_code == 200:
            chart_data = response.json()
            chart_url = f"http://{FLASK_HOST}:{FLASK_PORT}/charts/{chart_id}"

            return {
                "success": True,
                "chart_id": chart_id,
                "url": chart_url,
                "chart": chart_data.get("chart", {}),
            }
        elif response.status_code == 404:
            return {"success": False, "error": f"Chart {chart_id} not found"}
        else:
            return {
                "success": False,
                "error": f"Error accessing chart: {response.status_code}",
            }

    except requests.exceptions.ConnectionError:
        error_msg = "Cannot connect to Flask visualization server"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Error getting chart URL: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


def main() -> None:
    """Main entry point for the MCP server."""
    logger.info("Starting Snowflake MCP Server...")

    # Validate configuration on startup
    try:
        from src.config import validate_config

        validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.warning(f"Configuration validation failed: {e}")
        logger.warning(
            "Server will start but Snowflake operations may fail without proper configuration"
        )

    # Start the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
