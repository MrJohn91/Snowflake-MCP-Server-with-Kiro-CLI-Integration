# Project Structure

## Directory Layout
```
snowflake-mcp-server/
├── .kiro/                          # Kiro CLI configuration
│   ├── steering/                   # Project steering documents
│   ├── prompts/                    # Custom Kiro workflow prompts
│   └── settings/                   # MCP settings
├── charts/                         # Output directory for generated HTML charts
├── skills/                         # Best practice guides used by the AI Agent
│   └── mcp-builder-skill.md
├── src/                            # Main application code
│   ├── __init__.py
│   ├── config.py                   # Configuration & Mock Mode logic
│   ├── main.py                     # MCP server entry point & tool wrappers
│   ├── mock_data.py                # Simulated data for testing
│   ├── visualize.py                # Serverless Chart.js generation logic
│   └── tools/                      # Core business logic
│       ├── __init__.py
│       └── snowflake_tools.py      # Snowflake connectivity & query logic
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_cli_mock.py            # Automated end-to-end testing (Mock Mode)
│   ├── test_manual.py              # Interactive test runner
│   ├── test_tools.py               # Unit tests for tools
│   └── test_integration.py         # Integration tests
├── .env.example                    # Environment variable template
├── .env                            # Actual environment variables (gitignored)
├── .gitignore                      # Git ignore patterns
├── DEVLOG.md                       # Development timeline and decisions
├── README.md                       # Project documentation
├── VIDEO_SCRIPT.md                 # Demo video script
├── pyproject.toml                  # Python package configuration (uv)
└── uv.lock                         # Dependency lock file
```

## File Naming Conventions
- Use snake_case for Python files and directories
- Use descriptive names that indicate functionality
- Prefix test files with `test_`
- Use `.md` extension for all documentation

## Module Organization
- **src/main.py**: Entry point that registers MCP tools.
- **src/tools/**: Contains raw business logic (Snowflake/Mock).
- **src/visualize.py**: Pure function module for generating HTML.
- **src/mock_data.py**: Static data dictionaries for simulation.
- **charts/**: Transient output folder (ignored by git).

## Configuration Files
- **pyproject.toml**: Main project config & dependencies (managed by `uv`).
- **.env**: Secrets (Snowflake credentials).
- **.kiro/settings/mcp.json**: Kiro MCP configuration (portable).

## Documentation Structure
- **README.md**: User-facing "Start Here" guide.
- **DEVLOG.md**: Chronological development log.
- **VIDEO_SCRIPT.md**: Plan for the demo video.
- **.kiro/steering/**: AI context documents (Product, Tech, Structure).

## Build Artifacts
- **charts/**: Generated HTML files.
- **.venv/**: Virtual environment (created by `uv sync`).
- **__pycache__/**: Python bytecode (gitignored).
