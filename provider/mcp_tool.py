import json
from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from utils.mcp_client import McpClients


class McpToolProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        servers_config_json = credentials.get("servers_config", "")
        if not servers_config_json:
            # 允许预授权配置为空，运行时会检查
            return
        
        # 如果提供了预授权配置，则验证其有效性
        try:
            servers_config = json.loads(servers_config_json)
        except json.JSONDecodeError as e:
            raise ToolProviderCredentialValidationError(f"servers_config must be a valid JSON string: {e}")

        mcp_clients = McpClients(servers_config)
        try:
            mcp_clients.fetch_tools()
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"预授权配置无效: {str(e)}")
        finally:
            if mcp_clients:
                mcp_clients.close()
