# db-mcp-server

A universal Model Context Protocol (MCP) server for databases. It allows LLMs (like Claude in Cursor or Claude Desktop) to connect to your databases, explore the schema, analyze column statistics, and safely run `SELECT` queries.

## Supported Databases
- SQLite
- PostgreSQL
- MySQL
- SQL Server (MSSQL)

## Installation

You can install the dependencies and run it locally using `uv`:

```bash
uv sync
uv run db-mcp-server
```

## Configuration

The server is configured entirely via environment variables. You can create a `.env` file in the directory where you run the server. See `.env.example` for all options.

### Single Database
Set `DB_PROVIDER` and `DB_CONNECTION_STRING`:

```bash
DB_PROVIDER=postgresql
DB_CONNECTION_STRING=postgresql://username:password@localhost:5432/my_database
```

### Multiple Databases
Set the `DATABASES` environment variable as a JSON string to connect to multiple databases simultaneously:

```bash
DATABASES='{"ecommerce": {"provider": "postgresql", "connection_string": "postgresql://..."}, "logs": {"provider": "sqlite", "connection_string": "sqlite:///logs.db"}}'
```

### Security / Authentication (HTTP Transports)
For `sse` or `streamable-http` transports, it is highly recommended to secure your MCP server with an API Key. 

Set the `API_KEY` environment variable:
```bash
API_KEY=your_secret_api_key_here
```

When `API_KEY` is set, all incoming HTTP requests must include either an `X-API-Key: <your_secret>` header or an `Authorization: Bearer <your_secret>` header.
> **Note:** API Key authentication only applies to HTTP transports. Standard I/O (`stdio`) connections ignore the API Key.

## Running the Server

### 1. Normal Mode (For Cursor, Claude Desktop, AI Agents)
By default, the server runs in `stdio` (Standard I/O) mode. This is the mode required by Cursor and Claude Desktop to communicate via invisible JSON-RPC messages.

```bash
uv run db-mcp-server
```
> **Note:** In `stdio` mode, the terminal will appear completely silent (frozen) without any "Server Started" messages. This is expected behavior! Any text printed to the terminal would corrupt the JSON communication with the AI.

### 2. Testing Visually (MCP Inspector)
Anthropic provides an official web-based inspector to manually test your MCP server, run queries, and see the exact JSON responses.

Run this command inside the project directory:
```bash
npx @modelcontextprotocol/inspector uv run db-mcp-server
```
It will print a local URL (e.g., `http://localhost:5173/?proxy_session_token=...`). Click that specific link to open the Inspector, and you will see buttons for `get_schema`, `get_column_stats`, and `run_sql_query`.

### 3. HTTP Server Mode
If you are building a custom client that prefers HTTP (SSE) over stdio, you can start the server in HTTP mode:

```bash
uv run db-mcp-server --transport streamable-http
```
This will print a starting message (e.g., `Starting MCP Server on http://127.0.0.1:9001/mcp`) and listen for web requests.

## Integration with Cursor

To add this to Cursor:
1. Go to Cursor Settings > Features > MCP
2. Add a new MCP server:
   - Type: `command`
   - Command: `uv run db-mcp-server` (or `uv run python -m db_mcp_server`)
   - Important: Make sure to set the execution path (CWD) to the directory where this project is located, so it can read your `.env` file and use the local `.venv`.

## Tools Provided

1. `get_schema()`: Returns the full schema (DDL) of all connected databases.
2. `get_column_stats()`: Analyzes columns and returns min/max/avg for numerics, and top 10 values for text columns.
3. `run_sql_query(query, db_name="default")`: Safely executes a `SELECT` query on the specified database.
