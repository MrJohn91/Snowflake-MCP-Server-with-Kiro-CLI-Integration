"""Test fixtures and configuration for Snowflake MCP Server tests."""

import os
import sys
from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest
from fastmcp import Client

# Add project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import mcp


@pytest.fixture
def mock_snowflake_connection():
    """Mock Snowflake connection for testing."""
    mock_conn = Mock()
    mock_cursor = Mock()

    # Mock cursor behavior
    mock_cursor.fetchall.return_value = [
        {"name": "TEST_TABLE", "type": "TABLE", "rows": 1000},
        {"name": "SALES_DATA", "type": "TABLE", "rows": 5000},
    ]
    mock_cursor.description = [("name",), ("type",), ("rows",)]

    mock_conn.cursor.return_value = mock_cursor
    return mock_conn


@pytest.fixture
def sample_query_result():
    """Sample query result data for testing."""
    return {
        "success": True,
        "data": {
            "rows": [
                {"region": "North", "sales": 10000},
                {"region": "South", "sales": 15000},
                {"region": "East", "sales": 12000},
                {"region": "West", "sales": 8000},
            ],
            "columns": ["region", "sales"],
            "row_count": 4,
            "query": "SELECT region, sales FROM sales_data LIMIT 100",
        },
    }


@pytest.fixture
def sample_table_list():
    """Sample table list for testing."""
    return {
        "success": True,
        "data": {
            "tables": [
                {
                    "name": "CUSTOMERS",
                    "schema": "GOLD",
                    "database": "PACIFICRETAIL",
                    "kind": "TABLE",
                    "rows": 10000,
                    "bytes": 1024000,
                },
                {
                    "name": "ORDERS",
                    "schema": "GOLD",
                    "database": "PACIFICRETAIL",
                    "kind": "TABLE",
                    "rows": 50000,
                    "bytes": 5120000,
                },
            ],
            "count": 2,
            "schema": "GOLD",
        },
    }


@pytest.fixture
def mock_flask_response():
    """Mock Flask server response for chart creation."""
    return {
        "success": True,
        "chart_id": "test-chart-123",
        "url": "http://127.0.0.1:5000/charts/test-chart-123",
        "data_count": 4,
    }


@pytest.fixture
async def fastmcp_client():
    """FastMCP client for testing MCP tools."""
    async with Client(mcp) as client:
        yield client


@pytest.fixture
def mock_requests_post():
    """Mock requests.post for Flask server communication."""
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "chart_id": "test-chart-123",
            "url": "http://127.0.0.1:5000/charts/test-chart-123",
            "data_count": 4,
        }
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for Flask server communication."""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "chart": {
                "id": "test-chart-123",
                "title": "Test Chart",
                "chart_type": "bar",
                "data_count": 4,
            },
        }
        mock_get.return_value = mock_response
        yield mock_get


# Test validation function
def test_fixtures():
    """Test that fixtures are working correctly."""
    assert True  # Basic test to ensure pytest can run
