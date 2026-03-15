import json
import os
import re
from copy import deepcopy


_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")
_SENSITIVE_KEY_PATTERN = re.compile(
    r"(authorization|token|secret|password|api[_-]?key|private[_-]?key)",
    re.IGNORECASE,
)


def _resolve_env_placeholders(obj):
    if isinstance(obj, dict):
        return {k: _resolve_env_placeholders(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve_env_placeholders(item) for item in obj]
    if isinstance(obj, str):
        def _replace(match):
            var_name = match.group(1)
            env_value = os.getenv(var_name)
            if env_value is None:
                raise EnvironmentError(
                    f"Environment variable '{var_name}' is not set"
                )
            return env_value

        return _ENV_VAR_PATTERN.sub(_replace, obj)
    return obj


def _mask_secret(value, show_start=4, show_end=4):
    if value is None:
        return None
    value = str(value)
    if len(value) <= show_start + show_end:
        return "*" * len(value)
    return f"{value[:show_start]}...{value[-show_end:]}"


def _redact_value_by_key(key, value):
    if not isinstance(value, str):
        return value

    key_str = str(key)
    if not _SENSITIVE_KEY_PATTERN.search(key_str):
        return value

    if key_str.lower() == "authorization" and value.lower().startswith("bearer "):
        token = value[7:].strip()
        return f"Bearer {_mask_secret(token)}"

    return _mask_secret(value)


def _redact_nested(obj, parent_key=None):
    if isinstance(obj, dict):
        return {k: _redact_nested(v, parent_key=k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_redact_nested(item, parent_key=parent_key) for item in obj]
    if parent_key is None:
        return obj
    return _redact_value_by_key(parent_key, obj)


def redact_mcp_servers(servers):
    return _redact_nested(deepcopy(servers))


def load_mcp_servers(config_path):
    """
    Load MCP server definitions from a JSON config file.
    Expects a top-level 'mcpServers' dict in the config.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        config = json.load(f)
    servers = _resolve_env_placeholders(config.get("mcpServers", {}))

    # Set default transport from server shape.
    for _, server in servers.items():
        if "command" in server and "transport" not in server:
            server["transport"] = "stdio"
        if "url" in server and "transport" not in server:
            server["transport"] = "streamable_http"

    return servers


def get_tool_names(tools, sort_names=True):
    names = [getattr(tool, "name", "<unknown>") for tool in tools]
    return sorted(names) if sort_names else names


def print_tool_names_grid(tools, cols=3, col_width=30, sort_names=True):
    tool_names = get_tool_names(tools, sort_names=sort_names)
    print(f"Total MCP tools: {len(tool_names)}")
    print("=" * (col_width * cols))

    for i in range(0, len(tool_names), cols):
        row = tool_names[i:i + cols]
        print("".join(f"{name:<{col_width}}" for name in row))
