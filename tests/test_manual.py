import sys
import json
import webbrowser
from src.tools.snowflake_tools import list_views, query_snowflake
from src.visualize import generate_chart_html
from src import config

# Ensure we catch the Mock Mode initialization
config.validate_config()

def print_header():
    print("\n" + "="*50)
    print(" ❄️  SNOWFLAKE MCP SERVER - TEST RUNNER ❄️")
    print("="*50)
    if config.MOCK_MODE:
        print("⚠️  RUNNING IN MOCK MODE (No Credentials Found)")
    else:
        print("✅ RUNNING IN REAL MODE")
    print("-" * 50)

def menu():
    print("\nSelect an action:")
    print("1. List Available Views (Gold Schema)")
    print("2. Query Daily Sales Summary")
    print("3. Generate & Open Demo Chart")
    print("q. Quit")
    return input("\nEnter choice [1-3, q]: ").strip()

def run_list_views():
    print("\n📡 Fetching Views...")
    result = list_views("GOLD")
    if result.get("success"):
        views = result["data"]["views"]
        print(f"\n✅ Found {len(views)} Views:")
        for v in views:
            print(f"   - {v['name']} ({v['kind']})")
    else:
        print(f"\n❌ Error: {result.get('error')}")

def run_query():
    print("\n📡 Executing Query: 'SELECT * FROM GOLD.DAILY_SALES_SUMMARY LIMIT 5'...")
    # Using a query that matches our Mock Logic heuristic just in case
    query = "SELECT PRODUCT_CATEGORY, SUM(TOTAL_REVENUE) as REVENUE FROM GOLD.DAILY_SALES_SUMMARY GROUP BY PRODUCT_CATEGORY ORDER BY REVENUE DESC LIMIT 5"
    result = query_snowflake(query)
    
    if result.get("success"):
        rows = result["data"]["rows"]
        print(f"\n✅ Query Successful. Retrieved {len(rows)} rows:")
        print(json.dumps(rows, indent=2))
    else:
        print(f"\n❌ Error: {result.get('error')}")

def run_chart():
    print("\n📊 Generating Demo Chart...")
    # Sample data mimicking the Mock Data
    data = [
        {'category': 'Electronics', 'revenue': 45320.50},
        {'category': 'Garden', 'revenue': 32100.75},
        {'category': 'Food', 'revenue': 28540.20},
        {'category': 'Home', 'revenue': 15200.10},
        {'category': 'Clothing', 'revenue': 12450.00}
    ]
    
    result = generate_chart_html(
        data=data,
        chart_type='bar',
        x_column='category',
        y_column='revenue',
        title='Demo Revenue by Category',
        open_browser=True
    )
    
    if result.get("success"):
        print(f"\n✅ Chart Generated!")
        print(f"   File: {result['file_path']}")
        print("   🚀 Browser should open automatically...")
    else:
        print(f"\n❌ Error: {result.get('error')}")

def main():
    print_header()
    while True:
        choice = menu()
        if choice == '1':
            run_list_views()
        elif choice == '2':
            run_query()
        elif choice == '3':
            run_chart()
        elif choice.lower() == 'q':
            print("\n👋 Exiting...")
            sys.exit(0)
        else:
            print("\n⚠️ Invalid choice, try again.")

if __name__ == "__main__":
    main()
