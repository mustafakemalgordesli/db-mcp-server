import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

class Settings:
    # MCP Configuration
    MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "9001"))
    MCP_SERVER_PATH: str = os.getenv("MCP_SERVER_PATH", "/mcp")
    
    @property
    def MCP_SERVER_URL(self) -> str:
        return f"http://{self.MCP_SERVER_HOST}:{self.MCP_SERVER_PORT}{self.MCP_SERVER_PATH}"

    # Database Configuration
    # Parse DATABASES env var as JSON if available, otherwise fallback to DB_PROVIDER/DB_CONNECTION_STRING
    _databases_json: str = os.getenv("DATABASES", "{}")
    
    try:
        DATABASES: dict = json.loads(_databases_json)
    except json.JSONDecodeError:
        DATABASES = {}

    if not DATABASES:
        DATABASES = {
            "default": {
                "provider": os.getenv("DB_PROVIDER", "sqlite"),
                "connection_string": os.getenv(
                    "DB_CONNECTION_STRING",
                    "sqlite:///:memory:"  # Default to in-memory sqlite if nothing provided
                )
            }
        }

settings = Settings()
