# Technical Architecture

## Technology Stack
- **MCP Framework**: FastMCP (Python 3.11+)
- **Database**: Snowflake with Bronze/Silver/Gold architecture
- **Visualization**: Flask + Plotly.js for interactive charts
- **Client**: Kiro CLI (Model Context Protocol client)
- **Authentication**: Environment-based credentials
- **Testing**: FastMCP Client + pytest
- **Dependencies**: snowflake-connector-python, python-dotenv, flask

## Architecture Overview
```
Kiro CLI ↔ MCP Server (FastMCP) ↔ Snowflake Database
                ↕
        Flask Web Server (Charts/Visualization)
```

**Components:**
- MCP Server: Handles natural language queries and Snowflake connectivity
- Flask Server: Generates and serves interactive visualizations
- Snowflake Connector: Secure database communication
- Query Engine: Natural language to SQL translation
- Chart Generator: Converts query results to visual formats

## Development Environment
- Python 3.11 or higher
- FastMCP 2.13.0.1
- Snowflake account with Gold-layer data
- Kiro CLI installed and configured
- Local development server for Flask charts
- Environment variables for secure credential management

## Code Standards
- Follow FastMCP best practices and patterns
- Use type hints for all function parameters and returns
- Implement comprehensive error handling and logging
- Follow DRY principle with common.py registration pattern
- Use async/await for database operations where beneficial
- Maintain clear separation between MCP tools and Flask routes

## Testing Strategy
- Unit tests for individual MCP tools using FastMCP Client
- Integration tests for Snowflake connectivity
- End-to-end tests for complete query workflows
- Flask route testing for visualization endpoints
- Mock Snowflake responses for CI/CD pipeline
- Target 80%+ test coverage

## Deployment Process
- Local development with main_noauth.py (no authentication)
- Production deployment with main.py (full authentication)
- Environment-specific configuration via .env files
- Flask server runs as separate process or integrated service
- Kiro CLI configuration for MCP server connection

## Performance Requirements
- Query response time: < 5 seconds for standard queries
- Chart generation: < 2 seconds for typical datasets
- Memory usage: < 500MB for normal operations
- Concurrent users: Support 10+ simultaneous connections
- Database connection pooling for efficiency

## Security Considerations
- Snowflake credentials stored in environment variables only
- No hardcoded secrets in source code
- MCP protocol provides secure communication channel
- Flask server restricted to localhost by default
- Input validation for all user queries
- SQL injection prevention through parameterized queries
