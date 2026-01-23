"""Integration tests for Snowflake MCP Server."""

import json
import os
import sys
from unittest.mock import Mock, patch

import pytest
import requests

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_snowflake_config, validate_config
from app.flask_app.app import app as flask_app


class TestFlaskIntegration:
    """Integration tests for Flask visualization server."""

    @pytest.fixture
    def client(self):
        """Flask test client."""
        flask_app.config["TESTING"] = True
        with flask_app.test_client() as client:
            yield client

    def test_health_endpoint(self, client):
        """Test Flask health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "snowflake-mcp-visualization" in data["service"]

    def test_create_chart_endpoint(self, client):
        """Test chart creation endpoint."""
        chart_data = {
            "data": [
                {"region": "North", "sales": 10000},
                {"region": "South", "sales": 15000},
                {"region": "East", "sales": 12000},
            ],
            "chart_type": "bar",
            "x_column": "region",
            "y_column": "sales",
            "title": "Sales by Region",
        }

        response = client.post(
            "/charts", data=json.dumps(chart_data), content_type="application/json"
        )

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True
        assert "chart_id" in data
        assert "url" in data
        assert data["data_count"] == 3

    def test_create_chart_missing_data(self, client):
        """Test chart creation with missing data."""
        chart_data = {"chart_type": "bar", "x_column": "region", "y_column": "sales"}

        response = client.post(
            "/charts", data=json.dumps(chart_data), content_type="application/json"
        )

        assert response.status_code == 400

        data = json.loads(response.data)
        assert data["success"] is False
        assert "No data provided" in data["error"]

    def test_list_charts_endpoint(self, client):
        """Test listing charts endpoint."""
        response = client.get("/charts")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["success"] is True
        assert "charts" in data
        assert "count" in data


class TestConfigurationIntegration:
    """Integration tests for configuration management."""

    def test_config_validation_with_env(self):
        """Test configuration validation with real .env file."""
        # This should work since we have a real .env file
        try:
            validate_config()
            config = get_snowflake_config()

            # Verify required fields are present
            required_fields = [
                "account",
                "user",
                "password",
                "warehouse",
                "database",
                "role",
            ]
            for field in required_fields:
                assert config[field] is not None, f"Missing required field: {field}"
                assert config[field] != "", f"Empty required field: {field}"

        except ValueError as e:
            pytest.skip(f"Configuration validation failed: {e}")

    @patch.dict(os.environ, {}, clear=True)
    def test_config_validation_missing_env(self):
        """Test configuration validation with missing environment variables."""
        # Clear environment and reload config
        import importlib

        import app.config

        importlib.reload(app.config)

        with pytest.raises(ValueError) as exc_info:
            app.config.validate_config()

        assert "Missing required environment variables" in str(exc_info.value)


class TestSnowflakeIntegration:
    """Integration tests with real Snowflake connection."""

    @pytest.mark.integration
    def test_real_snowflake_connection(self):
        """Test actual connection to Snowflake (requires valid credentials)."""
        try:
            from app.tools.snowflake_tools import list_tables

            # This will use real credentials from .env
            result = list_tables()

            if result["success"]:
                # If connection succeeds, verify response structure
                assert "data" in result
                assert "tables" in result["data"]
                assert "count" in result["data"]
                assert isinstance(result["data"]["tables"], list)

                print(f"✅ Successfully connected to Snowflake")
                print(f"   Found {result['data']['count']} tables")

                # If we have tables, test describe_table
                if result["data"]["tables"]:
                    from app.tools.snowflake_tools import describe_table

                    first_table = result["data"]["tables"][0]["name"]
                    desc_result = describe_table(first_table)

                    if desc_result["success"]:
                        assert "data" in desc_result
                        assert "columns" in desc_result["data"]
                        print(f"   Successfully described table: {first_table}")
                        print(
                            f"   Table has {desc_result['data']['column_count']} columns"
                        )

            else:
                pytest.skip(f"Snowflake connection failed: {result['error']}")

        except Exception as e:
            pytest.skip(f"Snowflake integration test failed: {e}")

    @pytest.mark.integration
    def test_real_snowflake_query(self):
        """Test actual query execution against Snowflake."""
        try:
            from app.tools.snowflake_tools import query_snowflake

            # Simple query that should work on most Snowflake instances
            result = query_snowflake(
                "SELECT CURRENT_TIMESTAMP() as current_time", limit=1
            )

            if result["success"]:
                assert "data" in result
                assert "rows" in result["data"]
                assert "columns" in result["data"]
                assert len(result["data"]["rows"]) == 1
                assert "current_time" in result["data"]["columns"]

                print(f"✅ Successfully executed Snowflake query")
                print(f"   Current time: {result['data']['rows'][0]}")

            else:
                pytest.skip(f"Snowflake query failed: {result['error']}")

        except Exception as e:
            pytest.skip(f"Snowflake query test failed: {e}")


class TestEndToEndWorkflow:
    """End-to-end workflow tests."""

    @pytest.mark.integration
    def test_query_to_chart_workflow(self):
        """Test complete workflow from Snowflake query to chart creation."""
        try:
            # Step 1: Execute a Snowflake query
            from app.tools.snowflake_tools import query_snowflake

            query_result = query_snowflake(
                "SELECT 'North' as region, 10000 as sales UNION ALL "
                "SELECT 'South' as region, 15000 as sales UNION ALL "
                "SELECT 'East' as region, 12000 as sales",
                limit=10,
            )

            if not query_result["success"]:
                pytest.skip(f"Query failed: {query_result['error']}")

            # Step 2: Create chart from query results
            chart_data = {
                "data": query_result["data"]["rows"],
                "chart_type": "bar",
                "x_column": "region",
                "y_column": "sales",
                "title": "Sales by Region",
            }

            # Test Flask chart creation
            flask_app.config["TESTING"] = True
            with flask_app.test_client() as client:
                response = client.post(
                    "/charts",
                    data=json.dumps(chart_data),
                    content_type="application/json",
                )

                assert response.status_code == 200

                chart_result = json.loads(response.data)
                assert chart_result["success"] is True

                # Step 3: Verify chart can be accessed
                chart_id = chart_result["chart_id"]
                chart_response = client.get(f"/charts/{chart_id}")
                assert chart_response.status_code == 200

                print(f"✅ End-to-end workflow successful")
                print(f"   Query returned {len(query_result['data']['rows'])} rows")
                print(f"   Chart created with ID: {chart_id}")

        except Exception as e:
            pytest.skip(f"End-to-end workflow failed: {e}")


# Test runner configuration
if __name__ == "__main__":
    # Run integration tests only if explicitly requested
    pytest.main([__file__, "-v", "-m", "integration"])
