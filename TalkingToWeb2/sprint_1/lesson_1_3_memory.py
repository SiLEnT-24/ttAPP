import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "poolside/laguna-m.1:free"


def get_completion(messages: list[dict]) -> str:
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Add it to your .env file.")

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    request_data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(API_URL, data=request_data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"OpenRouter request failed: {error.read().decode('utf-8')}") from error

    choices = response_data.get("choices", [])
    if not choices:
        raise RuntimeError("No choices were returned by OpenRouter.")

    message = choices[0].get("message", {})
    content = message.get("content", "")
    return content


def main() -> None:
    messages = []

    print("Type your message and press Enter. Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        response_text = get_completion(messages)
        messages.append({"role": "assistant", "content": response_text})
        print(f"Assistant: {response_text}")


if __name__ == "__main__":
    main()
