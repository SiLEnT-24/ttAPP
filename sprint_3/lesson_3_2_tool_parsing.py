import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sprint_2.lesson_2_1_web_search import search_web


def parse_tool_calls(choice_response: dict) -> list[dict]:
    """Extract tool calls from a model response and return a normalised list."""
    if not isinstance(choice_response, dict):
        raise ValueError("choice_response must be a dictionary.")

    message = choice_response.get("message", {})
    tool_calls = message.get("tool_calls", [])
    if not tool_calls:
        return []

    parsed_calls = []
    for tool_call in tool_calls:
        function = tool_call.get("function", {})
        function_name = function.get("name")
        arguments_text = function.get("arguments", "{}")

        try:
            arguments = json.loads(arguments_text) if isinstance(arguments_text, str) else arguments_text
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid tool arguments: {arguments_text}") from error

        parsed_calls.append(
            {
                "name": function_name,
                "arguments": arguments,
                "tool_call_id": tool_call.get("id"),
            }
        )

    return parsed_calls


def execute_tool_call(tool_call: dict) -> dict:
    """Execute a locally supported tool call and return the result payload."""
    if not isinstance(tool_call, dict):
        raise ValueError("tool_call must be a dictionary.")

    tool_name = tool_call.get("name")
    arguments = tool_call.get("arguments", {})

    if tool_name == "web_search":
        query = arguments.get("query", "")
        max_results = arguments.get("max_results", 3)
        results = search_web(query, max_results=max_results)
        return {"tool_name": tool_name, "results": results}

    raise ValueError(f"Unsupported tool: {tool_name}")


def main() -> None:
    """Show how a sample model response with a tool call is parsed and executed."""
    sample_response = {
        "message": {
            "tool_calls": [
                {
                    "id": "call_123",
                    "function": {
                        "name": "web_search",
                        "arguments": '{"query": "artificial intelligence", "max_results": 2}',
                    },
                }
            ]
        }
    }

    parsed_calls = parse_tool_calls(sample_response)
    print(parsed_calls)
    print(execute_tool_call(parsed_calls[0]))


if __name__ == "__main__":
    main()
