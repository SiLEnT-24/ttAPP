import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "poolside/laguna-m.1:free"


def get_completion(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Add it to your .env file.")

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
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
    prompt = "An API call is a request made by a client application to a server's endpoint to retrieve or send data, triggering a predefined action and receiving a structured response."
    response_text = get_completion(prompt)
    print(response_text)


if __name__ == "__main__":
    main()
