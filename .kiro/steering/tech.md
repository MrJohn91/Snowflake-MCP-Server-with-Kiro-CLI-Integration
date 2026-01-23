# Technical Architecture

## Technology Stack
- **MCP Framework**: Official `mcp` SDK (Python)
- **Database**: Snowflake (Views Only / Gold Layer)
- **Visualization**: Static HTML + Chart.js (Serverless)
- **Client**: Kiro CLI (Model Context Protocol client)
- **Configuration**: `pyproject.toml` + `uv`
- **Testing**: `pytest`, Built-in Mock Mode

## Architecture Overview
```
Kiro CLI ↔ MCP Server (Stdio) ↔ Snowflake Database / Mock Data
                ↓
        HTML File Generation (Local Disk)
                ↓
        Browser (System Default)
```

**Components:**
- **MCP Server:** Handles tool calls (`list_views`, `query`, `create_chart`).
- **Snowflake Tools:** secure `snowflake-connector-python` logic.
- **Visualize Module:** Generates standalone `.html` files with embedded Chart.js.
- **Mock Engine:** Simulation layer that intercepts calls when credentials are missing.

## Development Environment
- Python 3.10+
- `uv` package manager
- Snowflake account (optional, for production)
- Kiro CLI

## Code Standards
- **Source Layout:** `src/` directory pattern
- **Type Hints:** Strict typing for all MCP tools
- **Error Handling:** Graceful degradation (Mock Mode fallback)
- **Portability:** Relative paths for all file operations
- **Architecture:** Separation of concerns (Tools vs. Config vs. Visualization)

## Testing Strategy
- **Automated CLI Testing:** `tests/test_cli_mock.py` runs full end-to-end scenarios.
- **Mock Mode:** Allows testing without real credentials.
- **Manual Verification:** Interactive `tests/test_manual.py` script.

## Deployment Process
1. Clone repository
2. Run `uv sync`
3. Launch with `kiro .`

## Security Considerations
- **Views-Only:** No direct table access; strictly limited to secure Views.
- **Credential Safety:** Secrets via `.env` only; auto-fallback to Mock if missing.
- **Local Execution:** Chart files generated locally, never uploaded.
- **Input Validation:** All tool inputs typed and validated by MCP SDK.
