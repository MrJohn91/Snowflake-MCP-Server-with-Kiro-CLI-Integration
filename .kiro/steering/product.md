# Product Overview

## Product Purpose
A custom Model Context Protocol (MCP) server that enables natural language querying of Snowflake databases through Kiro CLI. It features a "Serverless Visualization" engine that generates instant, interactive charts as standalone files, bridging the gap between business questions and visual insights without complex infrastructure.

## Target Users
- Data analysts and business intelligence professionals
- Operations teams needing quick data insights
- Sales teams requiring real-time performance metrics
- Executives seeking dashboard-free data access
- Anyone who needs to query Snowflake data without SQL knowledge

## Key Features
- **Natural Language to SQL:** Translate questions into optimized queries.
- **Views-Only Security:** Queries operate strictly on secure "Gold Layer" views, ensuring data safety.
- **Serverless Visualization:** Generates interactive Chart.js visualizations as standalone HTML files (no backend server required).
- **Mock Mode:** Built-in simulation mode for testing without credentials.
- **Kiro Integration:** Native support for Kiro's MCP client.
- **Portable:** Zero-config deployment with local execution.

## Business Objectives
- Democratize data access across the organization
- Reduce time-to-insight from hours to seconds
- Eliminate SQL knowledge barriers for business users
- Provide instant visual feedback for data queries
- Enable conversational data exploration workflows

## User Journey
1. User asks business question in natural language via Kiro CLI ("Show me sales by category")
2. MCP server translates question to SQL and queries Snowflake (or Mock Data)
3. Results are returned in plain text
4. User explicitly requests a chart ("Visualize this as a bar chart")
5. Server generates a standalone HTML file and opens it instantly in the browser
6. User interacts with the chart locally

## Success Criteria
- Query response time under 5 seconds
- Secure, read-only access via Views
- Zero infrastructure overhead (no database or web server to manage)
- Seamless "Clone & Run" experience for developers
