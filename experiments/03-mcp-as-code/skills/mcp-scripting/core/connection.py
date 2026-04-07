"""
Generic MCP connection manager.

Provides a connect() async context manager that establishes a session with any
MCP server — remote (HTTP + OAuth) or local (stdio subprocess).

Usage:
    from core.connection import connect

    async with connect("datadog") as session:
        result = await session.call_tool("search_datadog_logs", arguments={...})

The server name must match a key in servers.json (located at
.opencode/skills/mcp-scripting/servers.json). Config format follows the MCP spec:

    Remote:  {"type": "remote", "url": "https://...", "oauth": {}}
    Local:   {"type": "local", "command": ["npx", "-y", "my-mcp-server"]}

For remote servers with OAuth, tokens must already exist in
~/.local/share/opencode/mcp-auth.json (created when OpenCode first connects
to the MCP server).

Environment variable substitution:
    String values in servers.json can use ${VAR_NAME} placeholders, which are
    resolved from environment variables (with .env file support via python-dotenv).
    Example: {"env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"}}
"""

import json
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken

# Server config: lives at .opencode/skills/mcp-scripting/servers.json
SERVERS_CONFIG = Path(__file__).resolve().parent.parent / "servers.json"
# OAuth tokens: managed by OpenCode, shared with this framework
MCP_AUTH_FILE = Path.home() / ".local" / "share" / "opencode" / "mcp-auth.json"

# Load .env from the skill folder (if present) into os.environ.
# Variables already set in the shell take precedence (override=False is default).
load_dotenv(SERVERS_CONFIG.parent / ".env")


class OpenCodeTokenStorage(TokenStorage):
    """
    Reads/writes OAuth tokens from OpenCode's mcp-auth.json.
    Reuses tokens that OpenCode obtained via its OAuth flow.
    """

    def __init__(self, auth_file: Path, server_name: str):
        self.auth_file = auth_file
        self.server_name = server_name

    def _read_file(self) -> dict:
        if not self.auth_file.exists():
            return {}
        with open(self.auth_file) as f:
            return json.load(f)

    def _write_file(self, data: dict):
        with open(self.auth_file, "w") as f:
            json.dump(data, f, indent=2)

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        data = self._read_file()
        server_data = data.get(self.server_name, {})
        client_info = server_data.get("clientInfo", {})
        client_id = client_info.get("clientId")
        if not client_id:
            return None
        return OAuthClientInformationFull(
            client_id=client_id,
            redirect_uris=None,
        )

    async def get_tokens(self) -> OAuthToken | None:
        data = self._read_file()
        server_data = data.get(self.server_name, {})
        tokens = server_data.get("tokens", {})
        access_token = tokens.get("accessToken")
        if not access_token:
            return None

        expires_at = tokens.get("expiresAt", 0)
        if time.time() > expires_at:
            print(
                f"[warn] Access token expired (at {expires_at}). "
                "Refresh may be attempted automatically.",
                file=sys.stderr,
            )

        return OAuthToken(
            access_token=access_token,
            refresh_token=tokens.get("refreshToken"),
            expires_in=max(0, int(expires_at - time.time())) if expires_at else None,
            scope=tokens.get("scope"),
        )

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        data = self._read_file()
        if self.server_name not in data:
            data[self.server_name] = {}
        data[self.server_name]["clientInfo"] = {"clientId": client_info.client_id}
        self._write_file(data)

    async def set_tokens(self, tokens: OAuthToken) -> None:
        data = self._read_file()
        if self.server_name not in data:
            data[self.server_name] = {}
        data[self.server_name]["tokens"] = {
            "accessToken": tokens.access_token,
            "refreshToken": tokens.refresh_token,
            "expiresAt": time.time() + tokens.expires_in if tokens.expires_in else None,
            "scope": tokens.scope,
        }
        self._write_file(data)


# Regex for ${VAR_NAME} placeholders in config strings
_ENV_VAR_PATTERN = re.compile(r"\$\{([^}]+)}")


def _resolve_env_vars(value):
    """Recursively resolve ${VAR} placeholders in config values from os.environ.

    Walks dicts and lists. For strings, replaces every ${VAR_NAME} with the
    corresponding environment variable. Raises ValueError if any variable is
    not set.
    """
    if isinstance(value, str):
        missing = [
            m.group(1)
            for m in _ENV_VAR_PATTERN.finditer(value)
            if m.group(1) not in os.environ
        ]
        if missing:
            raise ValueError(
                f"Unresolved environment variable(s) in servers.json: "
                f"{', '.join('${' + v + '}' for v in missing)}. "
                f"Set them in the shell or in .opencode/skills/mcp-scripting/.env"
            )
        return _ENV_VAR_PATTERN.sub(lambda m: os.environ[m.group(1)], value)
    if isinstance(value, dict):
        return {k: _resolve_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env_vars(item) for item in value]
    return value


def _get_server_config(server_name: str) -> dict:
    """Read a server entry from servers.json and resolve ${VAR} placeholders."""
    if not SERVERS_CONFIG.exists():
        raise FileNotFoundError(
            f"Server config not found at {SERVERS_CONFIG}. "
            "Create servers.json with entries following the MCP spec, e.g.:\n"
            '  {"myserver": {"type": "remote", "url": "https://...", "oauth": {}}}'
        )
    with open(SERVERS_CONFIG) as f:
        config = json.load(f)
    server_entry = config.get(server_name)
    if not server_entry:
        raise ValueError(
            f"MCP server '{server_name}' not found in {SERVERS_CONFIG}. "
            f"Available servers: {list(config.keys())}"
        )
    return _resolve_env_vars(server_entry)  # type: ignore[return-value]


@asynccontextmanager
async def _connect_remote(server_name: str, server_config: dict):
    """Connect to a remote MCP server over HTTP with optional OAuth."""
    url = server_config.get("url")
    if not url:
        raise ValueError(f"Remote server '{server_name}' is missing 'url' in config.")

    oauth_config = server_config.get("oauth")
    headers = server_config.get("headers")

    # Build transport kwargs
    transport_kwargs = {"url": url}

    if oauth_config is not None and oauth_config is not False:
        # OAuth enabled — use OAuthClientProvider with OpenCode's stored tokens
        storage = OpenCodeTokenStorage(MCP_AUTH_FILE, server_name)

        tokens = await storage.get_tokens()
        if not tokens:
            raise RuntimeError(
                f"No OAuth tokens found for MCP server '{server_name}'. "
                "Run OpenCode first to authenticate with the MCP server."
            )

        client_info = await storage.get_client_info()
        if not client_info:
            raise RuntimeError(
                f"No client info found for MCP server '{server_name}'. "
                "Run OpenCode first to authenticate with the MCP server."
            )

        oauth_provider = OAuthClientProvider(
            server_url=url,
            client_metadata=OAuthClientMetadata(redirect_uris=None),
            storage=storage,
        )
        transport_kwargs["auth"] = oauth_provider

    if headers:
        transport_kwargs["headers"] = headers

    async with streamablehttp_client(**transport_kwargs) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session


@asynccontextmanager
async def _connect_local(server_name: str, server_config: dict):
    """Connect to a local MCP server via stdio (spawns a subprocess)."""
    command = server_config.get("command")
    if not command:
        raise ValueError(
            f"Local server '{server_name}' is missing 'command' in config."
        )

    # Support both formats:
    #   OpenCode style: {"command": ["npx", "-y", "server"]}
    #   SDK style:      {"command": "python3", "args": ["-m", "mcp_server_time"]}
    if isinstance(command, list):
        executable = command[0]
        args = command[1:]
    else:
        executable = command
        args = server_config.get("args", [])

    # Resolve relative command paths against the servers.json directory.
    # This allows configs like {"command": ".venv/bin/python3"} to work
    # regardless of the caller's working directory.
    config_dir = SERVERS_CONFIG.parent
    resolved = config_dir / executable
    if not Path(executable).is_absolute() and resolved.exists():
        executable = str(resolved)

    server_params = StdioServerParameters(
        command=executable,
        args=args,
        env=server_config.get("environment"),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session


@asynccontextmanager
async def connect(server_name: str):
    """
    Connect to an MCP server and yield a ClientSession.

    Dispatches based on the server's "type" field in servers.json:
      - "remote": HTTP transport with optional OAuth (tokens from OpenCode's mcp-auth.json)
      - "local":  stdio transport (spawns a subprocess)

    Usage:
        async with connect("datadog") as session:
            result = await session.call_tool("tool_name", arguments={...})

    Args:
        server_name: Key from servers.json (e.g., "datadog").

    Yields:
        mcp.ClientSession: An initialized MCP session ready for tool calls.
    """
    server_config = _get_server_config(server_name)
    server_type = server_config.get("type")

    # Infer type from shape if not explicitly set
    if not server_type:
        if "command" in server_config:
            server_type = "local"
        elif "url" in server_config:
            server_type = "remote"
        else:
            raise ValueError(
                f"Cannot infer server type for '{server_name}': "
                "config has neither 'type', 'command', nor 'url'."
            )

    if server_type == "remote":
        async with _connect_remote(server_name, server_config) as session:
            yield session
    elif server_type == "local":
        async with _connect_local(server_name, server_config) as session:
            yield session
    else:
        raise ValueError(
            f"Unknown server type '{server_type}' for '{server_name}'. "
            "Supported types: 'remote', 'local'."
        )
