import asyncio
from typing import Any

from chimera.library.models import WorkflowState
from chimera.services.terminal import print_message


def _sync_llm_call(state: WorkflowState, chat_model, tools_by_name: dict) -> dict[str, Any]:
    try:
        # Note: llm_call is imported here to avoid circular dependency.
        # Since it's defined in chimera/workflow.py, we might need to import it inside the function.
        from chimera.workflow import llm_call

        result = asyncio.run(llm_call(state, chat_model, tools_by_name))
        print_message(
            f"[llm_call] Completed. returning: messages={len(result.get('messages', []))}, llm_calls={result.get('llm_calls', 0)}"
        )
        return result
    except Exception as e:
        print_message(f"[llm_call] ERROR: {type(e).__name__}: {e}")
        raise


def _sync_tool_node(state: WorkflowState, tools_by_name: dict) -> dict[str, Any]:
    try:
        # Note: tool_node is imported here to avoid circular dependency.
        # Since it's defined in chimera/workflow.py, we might need to import it inside the function.
        from chimera.workflow import tool_node

        print_message(f"[tool_node] Starting. messages: {len(state.messages)}")
        result = asyncio.run(tool_node(state, tools_by_name))
        print_message(f"[tool_node] Completed. returning: messages={len(result.get('messages', []))}")
        return result
    except Exception as e:
        print_message(f"[tool_node] ERROR: {type(e).__name__}: {e}")
        raise
