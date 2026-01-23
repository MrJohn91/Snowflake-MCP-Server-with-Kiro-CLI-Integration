# Architecture Diagram

## System Architecture

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│                 │    │                      │    │                 │
│   Kiro CLI      │◄──►│   MCP Server         │◄──►│   Snowflake     │
│   (Client)      │    │   (FastMCP)          │    │   Database      │
│                 │    │                      │    │                 │
└─────────────────┘    └──────────────────────┘    └─────────────────┘
                                │
                                │
                                ▼
                       ┌──────────────────────┐
                       │                      │
                       │   Flask Web Server   │
                       │   (Visualization)    │
                       │                      │
                       └──────────────────────┘
```

## Component Details

### 1. **Kiro CLI (Client)**
- **Role**: AI-powered command line interface
- **Function**: Sends natural language queries via MCP protocol
- **Communication**: Bidirectional MCP protocol over STDIO/HTTP

### 2. **MCP Server (FastMCP)**
- **Role**: Core application server
- **Components**:
  - Natural language to SQL translator
  - Snowflake query executor
  - Chart generation coordinator
  - Error handling and logging
- **Tools**:
  - `query_snowflake` - Execute queries
  - `create_chart` - Generate visualizations
  - `list_tables` - Discover schema
  - `describe_table` - Get metadata

### 3. **Snowflake Database**
- **Role**: Data warehouse
- **Focus**: Gold-layer tables (business-ready data)
- **Connection**: Secure snowflake-connector-python

### 4. **Flask Web Server**
- **Role**: Visualization engine
- **Function**: Generates interactive charts from query results
- **Technology**: Flask + Plotly.js
- **Output**: Web-accessible chart URLs

## Data Flow

```
1. User Query (Natural Language)
   │
   ▼
2. Kiro CLI → MCP Server
   │
   ▼
3. NL to SQL Translation
   │
   ▼
4. SQL Query → Snowflake
   │
   ▼
5. Query Results ← Snowflake
   │
   ▼
6. Chart Generation → Flask Server
   │
   ▼
7. Chart URL ← Flask Server
   │
   ▼
8. Response (Data + Chart URL) → Kiro CLI
   │
   ▼
9. Display Results + Open Chart
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                    │
├─────────────────────────────────────────────────────────┤
│  Kiro CLI  │  FastMCP Server  │  Flask Web Server      │
├─────────────────────────────────────────────────────────┤
│                   Framework Layer                       │
├─────────────────────────────────────────────────────────┤
│  Python 3.11+  │  FastMCP  │  Flask  │  Plotly.js     │
├─────────────────────────────────────────────────────────┤
│                   Protocol Layer                        │
├─────────────────────────────────────────────────────────┤
│  MCP Protocol  │  HTTP/HTTPS  │  Snowflake Protocol    │
├─────────────────────────────────────────────────────────┤
│                     Data Layer                          │
├─────────────────────────────────────────────────────────┤
│              Snowflake Gold Tables                      │
└─────────────────────────────────────────────────────────┘
```

## Security Architecture & Data Governance

### Security-First Design Philosophy

The MCP server implements a **security-first approach** by connecting exclusively to Snowflake's Gold layer, demonstrating enterprise data governance best practices:

**GOLD Schema Only Access** - The MCP server is intentionally restricted to only the GOLD schema:

- **No Raw Data Exposure**: BRONZE and SILVER schemas are completely inaccessible to the MCP server
- **Curated Views Only**: Only 2 pre-approved views are exposed:
  - `DAILY_SALES_SUMMARY` - Daily revenue and sales metrics
  - `CUSTOMER_PRODUCT_AFFINITY_MONTHLY` - Customer behavior analytics
- **Data Governance**: Raw transactional data remains protected in lower layers
- **Controlled Analytics**: Business users get insights without accessing sensitive raw data

### Data Layer Security Model

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│   Kiro CLI      │◄──►│   MCP Server         │◄──►│   GOLD Views    │
│   (Client)      │    │   (Secure Access)    │    │   (Curated)     │
└─────────────────┘    └──────────────────────┘    └─────────────────┘
                                                            │
                                                    ┌─────────────────┐
                                                    │ BRONZE/SILVER   │
                                                    │ (Protected)     │
                                                    └─────────────────┘
```

This design ensures that AI-powered natural language queries can access business insights while maintaining strict data security and governance controls.

### Application Security

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│   Kiro CLI      │    │   MCP Server         │    │   Snowflake     │
│                 │    │                      │    │                 │
│ • Local client  │◄──►│ • Env variables      │◄──►│ • Secure conn   │
│ • No auth needed│    │ • Input validation   │    │ • Role-based    │
│                 │    │ • SQL injection      │    │ • GOLD only     │
│                 │    │   prevention         │    │                 │
└─────────────────┘    └──────────────────────┘    └─────────────────┘
                                │
                                │ Localhost only
                                ▼
                       ┌──────────────────────┐
                       │   Flask Server       │
                       │                      │
                       │ • Local binding      │
                       │ • No external access │
                       └──────────────────────┘
```

## Deployment Architecture

### Development Mode
```
┌─────────────────────────────────────────────────────────┐
│                Local Development                        │
│                                                         │
│  Kiro CLI ◄─► MCP Server ◄─► Snowflake (Cloud)        │
│                    │                                    │
│                    ▼                                    │
│              Flask Server                               │
│            (localhost:5000)                             │
└─────────────────────────────────────────────────────────┘
```

### Production Mode
```
┌─────────────────────────────────────────────────────────┐
│                Production Environment                   │
│                                                         │
│  Kiro CLI ◄─► MCP Server ◄─► Snowflake (Cloud)        │
│   (Remote)      (Server)                               │
│                    │                                    │
│                    ▼                                    │
│              Flask Server                               │
│            (Internal Network)                           │
└─────────────────────────────────────────────────────────┘
```
