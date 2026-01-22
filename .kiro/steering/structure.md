# Project Structure

## Directory Layout
```
snowflake-mcp-server/
├── .kiro/                          # Kiro CLI configuration
│   ├── steering/                   # Project steering documents
│   ├── prompts/                    # Custom Kiro workflow prompts
│   └── documentation/              # Additional project docs
├── app/                            # Main application code
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── common.py                   # Shared component registration (DRY)
│   ├── main.py                     # MCP server entry point
│   ├── tools/                      # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── snowflake_tools.py      # Core Snowflake query tools
│   │   └── visualization_tools.py  # Chart generation tools
│   ├── resources/                  # MCP resource implementations
│   │   ├── __init__.py
│   │   └── data_resources.py       # Data schema and metadata resources
│   ├── prompts/                    # MCP prompt templates
│   │   ├── __init__.py
│   │   └── query_prompts.py        # Natural language query helpers
│   └── flask_app/                  # Flask visualization server
│       ├── __init__.py
│       ├── app.py                  # Flask application
│       ├── routes.py               # Chart generation endpoints
│       └── templates/              # HTML templates for charts
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                 # Test fixtures and configuration
│   ├── test_tools.py               # MCP tool tests
│   ├── test_resources.py           # Resource tests
│   └── test_integration.py         # End-to-end tests
├── .env.example                    # Environment variable template
├── .env                            # Actual environment variables (gitignored)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── DEVLOG.md                       # Development timeline and decisions
└── .gitignore                      # Git ignore patterns
```

## File Naming Conventions
- Use snake_case for Python files and directories
- Use descriptive names that indicate functionality
- Prefix test files with `test_`
- Use `.md` extension for all documentation
- Environment files use `.env` prefix

## Module Organization
- **app/tools/**: Individual MCP tools, each in separate files
- **app/resources/**: MCP resources grouped by data type
- **app/prompts/**: Reusable prompt templates for query assistance
- **app/flask_app/**: Complete Flask application for visualizations
- **tests/**: Mirror the app structure for organized testing

## Configuration Files
- **.env**: Environment variables (Snowflake credentials, Flask config)
- **.kiro/**: Kiro CLI specific configuration and prompts
- **requirements.txt**: Python package dependencies
- **.gitignore**: Exclude .env, __pycache__, and build artifacts

## Documentation Structure
- **README.md**: Project overview, setup instructions, usage examples
- **DEVLOG.md**: Development timeline, decisions, challenges, solutions
- **.kiro/steering/**: Product, technical, and structural documentation
- **.kiro/documentation/**: Additional project-specific documentation

## Asset Organization
- **app/flask_app/templates/**: HTML templates for chart rendering
- **app/flask_app/static/**: CSS, JavaScript, and static assets (if needed)
- Chart data passed dynamically, no static chart files stored

## Build Artifacts
- **__pycache__/**: Python bytecode (gitignored)
- **.pytest_cache/**: Test cache (gitignored)
- **dist/**: Distribution packages (if building for distribution)

## Environment-Specific Files
- **.env.example**: Template showing required environment variables
- **.env**: Local development environment variables
- **Production**: Environment variables managed by deployment platform
- **Testing**: Separate test environment configuration in conftest.py
