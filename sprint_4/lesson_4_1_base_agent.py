import json
import os
import urllib.error
import urllib.request


class Agent:
    """A simple base class for LLM-powered agents that keep message history and support tool schemas."""

    def __init__(self, name: str, system_instruction: str, tools: list[dict] | None = None, model: str = "poolside/laguna-m.1:free") -> None:
        self.name = name
        self.system_instruction = system_instruction
        self.tools = tools
        self.model = model
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.messages: list[dict] = []

    def _build_payload(self, user_prompt: str) -> dict:
        """Create the request payload with the system instruction and current conversation history."""
        self.messages = [{"role": "system", "content": self.system_instruction}] + self.messages
        self.messages.append({"role": "user", "content": user_prompt})

        payload = {
            "model": self.model,
            "messages": self.messages,
        }
        if self.tools:
            payload["tools"] = self.tools
        return payload

    def _send_request(self, payload: dict) -> dict:
        """Send the prepared payload to OpenRouter and return the parsed response."""
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set. Add it to your .env file.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        request_data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(self.api_url, data=request_data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"OpenRouter request failed: {error.read().decode('utf-8')}") from error

    def execute(self, user_prompt: str) -> dict:
        """Run one turn of the agent, update conversation history, and return the raw response payload."""
        payload = self._build_payload(user_prompt)
        response = self._send_request(payload)

        choices = response.get("choices", [])
        if not choices:
            raise RuntimeError("No choices were returned by OpenRouter.")

        message = choices[0].get("message", {})
        self.messages.append(message)
        return response

    def get_last_text(self, response: dict) -> str:
        """Return the content text from the latest assistant response when present."""
        choices = response.get("choices", [])
        if not choices:
            return ""
        message = choices[0].get("message", {})
        return message.get("content", "") or ""


def main() -> None:
    """Demonstrate the base agent with a tiny sample prompt."""
    agent = Agent(name="Demo", system_instruction="You are a concise assistant.")
    try:
        response = agent.execute("Say hello in one sentence.")
        print(agent.get_last_text(response))
    except RuntimeError as error:
        print(error)


if __name__ == "__main__":
    main()
