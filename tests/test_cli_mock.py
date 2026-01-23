#!/usr/bin/env python3
"""
MCP Server CLI Tester
=====================
This script simulates what Kiro does when calling your MCP tools.
Run this to verify all tools work correctly with Mock Data.

Usage: uv run python test_mcp_cli.py
"""

import json
import sys
import os

# FORCE Mock Mode before any imports
os.environ["FORCE_MOCK_MODE"] = "true"

# Now import our modules
from src import config
config.validate_config()  # This will now see FORCE_MOCK_MODE and enable mock

from src.tools.snowflake_tools import list_views, query_snowflake, describe_view
from src.visualize import generate_chart_html

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def test_list_views():
    """Test: snowflake_list_views tool"""
    print_header("TEST 1: List Views (snowflake_list_views)")
    
    result = list_views("GOLD")
    
    if result.get("success"):
        views = result["data"]["views"]
        print_success(f"Found {len(views)} views in GOLD schema:")
        for v in views:
            print(f"   📊 {v['name']}")
        return True
    else:
        print_error(f"Failed: {result.get('error')}")
        return False

def test_describe_view():
    """Test: snowflake_describe_view tool"""
    print_header("TEST 2: Describe View (snowflake_describe_view)")
    
    result = describe_view("DAILY_SALES_SUMMARY", "GOLD")
    
    if result.get("success"):
        columns = result["data"]["columns"]
        print_success(f"View has {len(columns)} columns:")
        for col in columns:
            print(f"   📋 {col['name']} ({col['type']})")
        return True
    else:
        print_error(f"Failed: {result.get('error')}")
        return False

def test_query():
    """Test: snowflake_query tool"""
    print_header("TEST 3: Query Data (snowflake_query)")
    
    query = "SELECT PRODUCT_CATEGORY, SUM(TOTAL_REVENUE) as REVENUE FROM GOLD.DAILY_SALES_SUMMARY GROUP BY PRODUCT_CATEGORY"
    result = query_snowflake(query)
    
    if result.get("success"):
        rows = result["data"]["rows"]
        print_success(f"Query returned {len(rows)} rows:")
        for row in rows:
            print(f"   💰 {row}")
        return True
    else:
        print_error(f"Failed: {result.get('error')}")
        return False

def test_create_chart():
    """Test: create_chart tool"""
    print_header("TEST 4: Create Chart (create_chart)")
    
    # Use the mock sales data
    data = [
        {"PRODUCT_CATEGORY": "Electronics", "REVENUE": 45320.50},
        {"PRODUCT_CATEGORY": "Garden", "REVENUE": 32100.75},
        {"PRODUCT_CATEGORY": "Food", "REVENUE": 28540.20},
        {"PRODUCT_CATEGORY": "Home", "REVENUE": 15200.10},
        {"PRODUCT_CATEGORY": "Clothing", "REVENUE": 12450.00},
    ]
    
    result = generate_chart_html(
        data=data,
        chart_type="bar",
        x_column="PRODUCT_CATEGORY",
        y_column="REVENUE",
        title="Revenue by Category (Mock Data)",
        open_browser=False  # Don't auto-open, just verify it works
    )
    
    if result.get("success"):
        print_success(f"Chart created: {result['file_path']}")
        print("   📄 Open this file in your browser to view the chart")
        return True
    else:
        print_error(f"Failed: {result.get('error')}")
        return False

def main():
    print("\n" + "🔷"*30)
    print("   SNOWFLAKE MCP SERVER - CLI TEST SUITE")
    print("🔷"*30)
    
    # Show mode
    if config.MOCK_MODE:
        print("\n⚠️  MOCK MODE ACTIVE: Using simulated production data")
    else:
        print("\n🔌 REAL MODE: Connected to Snowflake")
    
    # Run all tests
    results = []
    results.append(("List Views", test_list_views()))
    results.append(("Describe View", test_describe_view()))
    results.append(("Query Data", test_query()))
    results.append(("Create Chart", test_create_chart()))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}: {name}")
    
    print(f"\n   Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS GO! Your MCP Server is ready for Kiro!")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
