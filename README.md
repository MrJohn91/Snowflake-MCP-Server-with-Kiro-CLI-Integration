# Snowflake MCP Server with Kiro CLI Integration

A custom Model Context Protocol (MCP) server that enables natural language querying of Snowflake databases through Kiro CLI with integrated Flask-based data visualization. Built for the Dynamous Kiro Hackathon 2026.

## 🎯 Project Overview

This MCP server bridges the gap between business questions and Snowflake insights, making enterprise data accessible through conversational AI. Users can ask questions in natural language via Kiro CLI and receive both data results and interactive visualizations.

### Key Features

- **Natural Language Queries**: Ask business questions without SQL knowledge
- **Real-time Snowflake Integration**: Direct connection to Gold-layer data
- **Interactive Visualizations**: Flask-powered charts and graphs
- **Kiro CLI Integration**: Seamless AI-powered workflow integration
- **Secure MCP Protocol**: Enterprise-grade security and communication

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Snowflake account with Gold-layer data access
- Kiro CLI installed and configured

### Installation

1. **Clone and setup environment:**
   ```bash
   git clone <repository-url>
   cd Hackathon_snowflakemcpserverproject
   cp .env.example .env
   ```

2. **Configure Snowflake credentials in `.env`:**
   ```bash
   SNOWFLAKE_ACCOUNT=your_account_identifier
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=GOLD
   SNOWFLAKE_ROLE=your_role
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test connection:**
   ```bash
   python -m pytest tests/test_connection.py -v
   ```

5. **Start the MCP server:**
   ```bash
   python app/main.py
   ```

## 🛠 Architecture

```
Kiro CLI ↔ MCP Server (FastMCP) ↔ Snowflake Database
                ↕
        Flask Web Server (Charts/Visualization)
```

### Components

- **MCP Server**: Handles natural language queries and Snowflake connectivity
- **Flask Server**: Generates and serves interactive visualizations  
- **Query Engine**: Translates natural language to optimized SQL
- **Chart Generator**: Converts query results to visual formats

## 📋 Available Tools

### Core MCP Tools

- **`query_snowflake`**: Execute natural language queries against Gold tables
- **`describe_table`**: Get comprehensive table schema and metadata
- **`list_tables`**: Discover available tables and data sources
- **`create_chart`**: Generate interactive visualizations from query results
- **`get_chart_url`**: Retrieve URLs for generated charts

### Example Usage

```bash
# Via Kiro CLI
@prime  # Load project context
"Show me sales performance by region for Q4"
"Create a bar chart of top 10 customers by revenue"
"What are the trending product categories this month?"
```

## 🧪 Development Workflow

This project follows the Kiro CLI hackathon development pattern:

### Core Development Cycle

1. **Load Context**: `@prime` - Understand current codebase state
2. **Plan Features**: `@plan-feature` - Create comprehensive implementation plans  
3. **Execute Plans**: `@execute` - Implement features systematically
4. **Review Code**: `@code-review` - Maintain code quality and standards

### Project Structure

```
snowflake-mcp-server/
├── .kiro/                    # Kiro CLI configuration
│   ├── steering/            # Project steering documents
│   ├── prompts/             # Custom workflow prompts
│   └── documentation/       # Additional project docs
├── app/                     # Main application code
│   ├── tools/              # MCP tool implementations
│   ├── resources/          # MCP resource implementations
│   ├── flask_app/          # Flask visualization server
│   └── main.py             # MCP server entry point
├── tests/                   # Comprehensive test suite
├── .env.example            # Environment template
└── requirements.txt        # Python dependencies
```

## 🎨 Visualization Features

The integrated Flask server provides:

- **Interactive Charts**: Bar, line, pie, and scatter plots
- **Real-time Updates**: Charts update with new query results
- **Export Options**: Save charts as PNG, PDF, or interactive HTML
- **Responsive Design**: Works on desktop and mobile devices

## 🔒 Security

- Environment-based credential management
- No hardcoded secrets in source code
- MCP protocol provides secure communication
- Input validation and SQL injection prevention
- Localhost-restricted Flask server by default

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Test specific components
python -m pytest tests/test_tools.py -v
python -m pytest tests/test_integration.py -v

# Test with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

## 📚 Documentation

- [Product Overview](.kiro/steering/product.md) - Project goals and user stories
- [Technical Architecture](.kiro/steering/tech.md) - System design and tech stack
- [Project Structure](.kiro/steering/structure.md) - Code organization and conventions
- [Development Log](DEVLOG.md) - Timeline, decisions, and challenges

## 🏆 Hackathon Submission

This project is built for the **Dynamous Kiro Hackathon 2026** with focus on:

- **Effective Kiro CLI Usage** (20% of score)
- **Application Quality** (40% of score) 
- **Documentation** (20% of score)
- **Innovation** (15% of score)
- **Presentation** (5% of score)

## 🤝 Contributing

1. Follow the established Kiro CLI workflow patterns
2. Use the custom prompts in `.kiro/prompts/` for development
3. Maintain comprehensive test coverage (80%+)
4. Update documentation for any new features
5. Follow FastMCP best practices and patterns

## 📄 License

MIT License - Built for the Dynamous Kiro Hackathon 2026

---

**Ready to query your Snowflake data with natural language?** 🚀

Start with `@prime` to load the project context, then use `@plan-feature` to add new capabilities!
