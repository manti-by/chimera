from chimera.settings import LINEAR_API_KEY


def get_linear_mcp_config() -> dict:
    return {
        "transport": "http",
        "url": "https://mcp.linear.app/mcp",
        "headers": {
            "Authorization": f"Bearer {LINEAR_API_KEY}",
        },
    }
