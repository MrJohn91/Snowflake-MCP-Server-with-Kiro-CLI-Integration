"""Unit tests for Snowflake MCP tools."""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.snowflake_tools import describe_table, list_tables, query_snowflake


class TestSnowflakeTools:
    """Test cases for Snowflake MCP tools."""

    @patch("app.tools.snowflake_tools.get_snowflake_connection")
    def test_query_snowflake_success(self, mock_get_conn, mock_snowflake_connection):
        """Test successful query execution."""
        # Setup mock
        mock_get_conn.return_value = mock_snowflake_connection
        mock_cursor = mock_snowflake_connection.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {"region": "North", "sales": 10000},
            {"region": "South", "sales": 15000},
        ]
        mock_cursor.description = [("region",), ("sales",)]

        # Execute
        result = query_snowflake("SELECT region, sales FROM test_table")

        # Verify
        assert result["success"] is True
        assert len(result["data"]["rows"]) == 2
        assert result["data"]["columns"] == ["region", "sales"]
        assert "LIMIT" in result["data"]["query"]

    def test_query_snowflake_empty_query(self):
        """Test query with empty string."""
        result = query_snowflake("")

        assert result["success"] is False
        assert "empty" in result["error"].lower()

    def test_query_snowflake_limit_validation(self):
        """Test query limit validation."""
        with patch(
            "app.tools.snowflake_tools.get_snowflake_connection"
        ) as mock_get_conn:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_cursor.fetchall.return_value = []
            mock_cursor.description = []
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value = mock_conn

            # Test limit too high gets capped
            result = query_snowflake("SELECT * FROM test", limit=2000)

            # Should be capped at 1000
            assert "LIMIT 1000" in result["data"]["query"]

    @patch("app.tools.snowflake_tools.get_snowflake_connection")
    def test_list_tables_success(self, mock_get_conn):
        """Test successful table listing."""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            {
                "name": "CUSTOMERS",
                "schema_name": "GOLD",
                "database_name": "PACIFICRETAIL",
                "kind": "TABLE",
                "rows": 10000,
                "bytes": 1024000,
                "created_on": "2024-01-01",
            }
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        # Execute
        result = list_tables()

        # Verify
        assert result["success"] is True
        assert len(result["data"]["tables"]) == 1
        assert result["data"]["tables"][0]["name"] == "CUSTOMERS"
        assert result["data"]["count"] == 1

    @patch("app.tools.snowflake_tools.get_snowflake_connection")
    def test_describe_table_success(self, mock_get_conn):
        """Test successful table description."""
        # Setup mock
        mock_conn = Mock()
        mock_cursor = Mock()

        # Mock DESCRIBE TABLE response
        mock_cursor.fetchall.return_value = [
            {
                "name": "ID",
                "type": "NUMBER(38,0)",
                "kind": "COLUMN",
                "null?": "N",
                "default": None,
                "primary key": "Y",
                "unique key": "N",
                "check": None,
                "expression": None,
                "comment": "Primary key",
            }
        ]

        # Mock SHOW TABLES response
        mock_cursor.fetchone.return_value = {
            "name": "CUSTOMERS",
            "schema_name": "GOLD",
            "database_name": "PACIFICRETAIL",
            "kind": "TABLE",
            "rows": 10000,
            "bytes": 1024000,
            "created_on": "2024-01-01",
            "comment": "Customer data",
        }

        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        # Execute
        result = describe_table("CUSTOMERS")

        # Verify
        assert result["success"] is True
        assert result["data"]["table"] == "CUSTOMERS"
        assert len(result["data"]["columns"]) == 1
        assert result["data"]["columns"][0]["name"] == "ID"
        assert result["data"]["columns"][0]["primary_key"] is True

    def test_describe_table_empty_name(self):
        """Test describe table with empty name."""
        result = describe_table("")

        assert result["success"] is False
        assert "empty" in result["error"].lower()

    @patch("app.tools.snowflake_tools.get_snowflake_connection")
    def test_query_snowflake_connection_error(self, mock_get_conn):
        """Test query with connection error."""
        mock_get_conn.side_effect = Exception("Connection failed")

        result = query_snowflake("SELECT * FROM test")

        assert result["success"] is False
        assert "Connection failed" in result["error"]

    @patch("app.tools.snowflake_tools.get_snowflake_connection")
    def test_list_tables_with_schema(self, mock_get_conn):
        """Test listing tables with specific schema."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = list_tables("SILVER")

        # Verify schema parameter was used
        mock_cursor.execute.assert_called_with("SHOW TABLES IN SCHEMA SILVER")
        assert result["success"] is True


class TestMCPToolsIntegration:
    """Integration tests for MCP tools using FastMCP Client."""

    @pytest.mark.asyncio
    async def test_mcp_tools_registration(self, fastmcp_client):
        """Test that all MCP tools are properly registered."""
        # Get list of available tools
        tools = await fastmcp_client.list_tools()

        tool_names = [tool.name for tool in tools.tools]

        # Verify all expected tools are registered
        expected_tools = [
            "snowflake_query",
            "snowflake_list_tables",
            "snowflake_describe_table",
            "create_chart",
            "get_chart_url",
        ]

        for tool_name in expected_tools:
            assert tool_name in tool_names, f"Tool {tool_name} not registered"

    @pytest.mark.asyncio
    @patch("app.tools.snowflake_tools.get_snowflake_connection")
    async def test_mcp_snowflake_query_tool(
        self, mock_get_conn, fastmcp_client, sample_query_result
    ):
        """Test snowflake_query tool via MCP client."""
        # Setup mock to return sample data
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = sample_query_result["data"]["rows"]
        mock_cursor.description = [("region",), ("sales",)]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        # Call tool via MCP client
        result = await fastmcp_client.call_tool(
            "snowflake_query",
            {"query": "SELECT region, sales FROM test_table", "limit": 10},
        )

        # Verify result
        assert result.content[0].text is not None
        # The result should be JSON string containing our data
        import json

        data = json.loads(result.content[0].text)
        assert data["success"] is True
        assert len(data["data"]["rows"]) == 4

    @pytest.mark.asyncio
    async def test_mcp_create_chart_tool(self, fastmcp_client, mock_requests_post):
        """Test create_chart tool via MCP client."""
        sample_data = [
            {"region": "North", "sales": 10000},
            {"region": "South", "sales": 15000},
        ]

        result = await fastmcp_client.call_tool(
            "create_chart",
            {
                "data": sample_data,
                "chart_type": "bar",
                "x_column": "region",
                "y_column": "sales",
                "title": "Sales by Region",
            },
        )

        # Verify Flask server was called
        mock_requests_post.assert_called_once()

        # Verify result format
        assert result.content[0].text is not None
        import json

        data = json.loads(result.content[0].text)
        assert data["success"] is True
        assert "chart_id" in data
