import argparse
import sys
from typing import Literal

from .server import start_mcp_server

def main():
    parser = argparse.ArgumentParser(description="Database MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol to use for the MCP server. stdio is best for CLI/Cursor integration, sse/streamable-http for HTTP clients.",
    )
    args = parser.parse_args()

    transport_type: Literal["stdio", "sse", "streamable-http"] = args.transport
    
    try:
        start_mcp_server(transport=transport_type)
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
