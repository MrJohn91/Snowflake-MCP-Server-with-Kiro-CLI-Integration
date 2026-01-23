# Development Log

## Project: Snowflake MCP Server with Kiro CLI Integration

**Hackathon**: Dynamous Kiro Hackathon 2026  
**Timeline**: January 15 - 23, 2026 (9 Days)  
**Developer**: Solo  
**Goal**: Build a custom MCP server for natural language Snowflake querying via Kiro CLI with visualization

---

## Day 1 - January 15, 2026

### 💡 Inception & Research

**Hours**: 3 hours

**Activities**:
- ✅ Reviewing hackathon rules and scoring criteria.
- ✅ Brainstorming ideas for the "Innovation" category.
- ✅ Selected idea: **Natural Language Data Analyst for Snowflake**.
- ✅ Researching the **Model Context Protocol (MCP)** specification.
- ✅ Evaluating libraries: `mcp` SDK vs `fastmcp`.

**Key Decisions**:
- **Framework**: Decided to use `fastmcp` for its decorator-based syntax and ease of use, enabling faster iteration than the raw SDK.

---

## Day 2 - January 16, 2026

### 🏗️ Setup & Configuration

**Hours**: 3.5 hours

**Activities**:
- ✅ Initialized git repository from the hackathon template.
- ✅ Set up the Python environment using `uv`.
- ✅ Configured Snowflake trial account for testing.
- ✅ Created `.env` structure for secure credential management.
- ✅ Defined the project directory structure.

**Challenges**:
- ensuring `uv` works correctly with the specific Python version required by Kiro dependencies.

---

## Day 3 - January 17, 2026

### 📐 Architecture Design

**Hours**: 4 hours

**Activities**:
- ✅ Drafted Steering Documents (`product.md`, `tech.md`).
- ✅ Designed the "Security-First" architecture (restricting access to specific layers).
- ✅ Decided on the transport mechanism: `stdio` (Standard Input/Output) as it's the native way Kiro communicates with MCP servers.
- ✅ Planned the visualization strategy: evaluated Flask Server vs. Static HTML generation.

---

## Day 4 - January 18, 2026

### ⚙️ Core MCP Implementation

**Hours**: 5 hours

**Activities**:
- ✅ Implemented the base `main.py` server using FastMCP.
- ✅ Created the Snowflake connection manager with connection pooling.
- ✅ Built the first tool: `snowflake_query`.
- ✅ Tested basic connectivity with a "Hello World" query ("SELECT CURRENT_VERSION()").

**Technical Highlights**:
- Implemented robust error handling to ensure the MCP server doesn't crash on bad SQL syntax.

---

## Day 5 - January 19, 2026

### 🛠️ Tool Expansion

**Hours**: 4.5 hours

**Activities**:
- ✅ Implemented schema discovery tools:
    - `snowflake_list_tables`
    - `snowflake_describe_table`
- ✅ Refined SQL generation logic.
- ✅ Added logging throughout the application for easier debugging during Kiro sessions.

---

## Day 6 - January 20, 2026

### 🔒 Security Implementation

**Hours**: 3 hours

**Activities**:
- ✅ Implemented the **GOLD Schema Only** policy.
- ✅ Updated tool logic to enforce schema bounds.
- ✅ Tested access control: Verified that queries to "BRONZE" or "SILVER" schemas are rejected.
- ✅ Created dummy views (`DAILY_SALES_SUMMARY`, `CUSTOMER_PRODUCT_AFFINITY`) in the GOLD schema for the demo.

**Key Decisions**:
- **Why Gold Only?**: To simulate a real-world enterprise environment where AI agents are restricted to curated, high-quality data.

---

## Day 7 - January 21, 2026

### 📊 Visualization Prototyping

**Hours**: 5 hours

**Activities**:
- ✅ Prototype 1: Flask API. (Built a basic server, but realized it added complexity for the user to run two processes).
- ✅ Prototype 2: Static HTML with Chart.js.
- ✅ Decision: **Go with Static HTML**. It's cleaner, easier to share, and requires less overhead for the end user.
- ✅ Wrote `visualize.py` core logic to generate HTML files dynamically.

---

## Day 8 - January 22, 2026

### 🎨 Integration & Refinement

**Hours**: 6 hours

**Activities**:
- ✅ Created the `create_chart` MCP tool.
- ✅ Integrated `visualize.py` into the MCP workflow.
- ✅ Tested the full pipeline: User Prompt -> Kiro -> SQL -> Data -> JSON -> Chart.js HTML.
- ✅ Added support for multiple chart types (Bar, Line, Pie, Doughnut, Scatter).
- ✅ Automated the "Open in Browser" functionality.

---

## Day 9 - January 23, 2026

### 📝 Testing, Kiro integration & Documentation

**Hours**: 5 hours

**Activities**:
- ✅ Final End-to-End testing with Kiro CLI.
- ✅ Configured custom Kiro prompts (`@prime`, `@plan-feature`).
- ✅ Wrote the **Demo Video Script**.
- ✅ Cleaned up the repository (removed temporary testing files).
- ✅ Finalized **README.md** with clear instructions for judges.

---

## Time Tracking Summary

| Day | Date | Hours | Focus Area |
|-----|------|-------|------------|
| 1 | Jan 15 | 3.0h | Inception & Research |
| 2 | Jan 16 | 3.5h | Setup & Config |
| 3 | Jan 17 | 4.0h | Architecture |
| 4 | Jan 18 | 5.0h | Core MCP |
| 5 | Jan 19 | 4.5h | Tool Expansion |
| 6 | Jan 20 | 3.0h | Security |
| 7 | Jan 21 | 5.0h | Viz Prototyping |
| 8 | Jan 22 | 6.0h | Integration |
| 9 | Jan 23 | 5.0h | Final Polish |
| **Total** | | **39.0h** | |

---

## Innovation Highlights

1.  **Seamless "Prompt-to-Plot" Workflow**: Removing the friction between asking a data question and seeing a chart.
2.  **Enterprise-Grade Security Pattern**: Demonstrating how GenAI can be safely deployed using Schema restrictions (GOLD layer).
3.  **Serverless Visualization**: By generating self-contained HTML files, we eliminate the need for hosting a dashboard server, making the tool lightweight and portable.

---

*Development completed January 23, 2026*