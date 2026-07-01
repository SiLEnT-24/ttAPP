import json
import os
import sys
import urllib.error
import urllib.request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sprint_2.lesson_2_1_web_search import search_web
from sprint_3.lesson_3_1_schemas import TOOLS

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "poolside/laguna-m.1:free"


def get_completion(messages: list[dict], tools: list[dict] | None = None) -> dict:
    """Send a prompt history to OpenRouter and return the raw API response object."""
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Add it to your .env file.")

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    request_data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(API_URL, data=request_data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"OpenRouter request failed: {error.read().decode('utf-8')}") from error


def extract_message_content(response_data: dict) -> str:
    """Pull plain text content from the first choice if it exists."""
    choices = response_data.get("choices", [])
    if not choices:
        return ""

    message = choices[0].get("message", {})
    return message.get("content", "") or ""


def extract_tool_calls(response_data: dict) -> list[dict]:
    """Extract tool-calling requests from the model response."""
    choices = response_data.get("choices", [])
    if not choices:
        return []

    message = choices[0].get("message", {})
    return message.get("tool_calls", []) or []


def run_single_agent(prompt: str, max_iterations: int = 5) -> str:
    """Run a simple agent loop that can request web-search tools and then answer the prompt."""
    if not API_KEY:
        search_results = search_web(prompt, max_results=3)
        return (
            "The OpenRouter API key is not configured, so this demo used a local fallback.\n"
            f"Search results for '{prompt}':\n"
            + "\n".join(
                f"- {result['title']} ({result['url']})" for result in search_results if result.get("title")
            )
        )

    messages = [{"role": "system", "content": "You are a helpful assistant that can use tools when needed."}]
    messages.append({"role": "user", "content": prompt})

    for _ in range(max_iterations):
        response_data = get_completion(messages, tools=TOOLS)
        content = extract_message_content(response_data)
        tool_calls = extract_tool_calls(response_data)

        if content and not tool_calls:
            return content

        if not tool_calls:
            return "No response was produced."

        assistant_message = response_data["choices"][0]["message"]
        messages.append(assistant_message)

        for tool_call in tool_calls:
            function_name = tool_call.get("function", {}).get("name")
            arguments = json.loads(tool_call.get("function", {}).get("arguments", "{}"))

            if function_name == "web_search":
                results = search_web(arguments.get("query", ""), max_results=arguments.get("max_results", 3))
                tool_result = {
                    "role": "tool",
                    "tool_call_id": tool_call.get("id"),
                    "content": json.dumps(results),
                }
                messages.append(tool_result)
            else:
                raise ValueError(f"Unsupported tool: {function_name}")

    return "Maximum iterations reached without a final answer."


def main() -> None:
    """Run the loop with a simple prompt that should trigger a web search tool call."""
    prompt = "Research the latest trends in artificial intelligence and summarize them."
    print(run_single_agent(prompt))


if __name__ == "__main__":
    main()
