from chimera.library.exceptions import LinearApiKeyException
from chimera.settings import LINEAR


def get_linear_mcp_config() -> dict:
    if not LINEAR["api_key"]:
        raise LinearApiKeyException

    return {
        "transport": "http",
        "url": "https://mcp.linear.app/mcp",
        "headers": {
            "Authorization": f"Bearer {LINEAR['api_key']}",
        },
    }
