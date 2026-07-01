TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for recent facts and background information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up.",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "How many results to return.",
                        "default": 3,
                    },
                },
                "required": ["query"],
            },
        },
    }
]


def main() -> None:
    """Print the tool schema so it can be inspected easily."""
    print(TOOLS)


if __name__ == "__main__":
    main()
