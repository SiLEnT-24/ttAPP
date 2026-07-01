import json


REQUIRED_TOP_LEVEL_KEYS = ["detected_sentiment", "theme", "layout_style"]
REQUIRED_THEME_KEYS = [
    "background_color",
    "primary_text",
    "accent_color",
    "font_family_heading",
    "font_family_body",
]


def validate_designer_json(payload: str) -> dict:
    """Parse and validate the designer JSON payload against the required schema."""
    if not isinstance(payload, str):
        raise ValueError("Payload must be a string.")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON: {error}") from error

    if not isinstance(data, dict):
        raise ValueError("Parsed JSON must be an object.")

    missing_keys = []
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data:
            missing_keys.append(key)

    if missing_keys:
        raise ValueError(f"Missing top-level keys: {', '.join(missing_keys)}")

    theme = data.get("theme")
    if not isinstance(theme, dict):
        raise ValueError("Theme must be an object.")

    missing_theme_keys = [key for key in REQUIRED_THEME_KEYS if key not in theme]
    if missing_theme_keys:
        raise ValueError(f"Missing theme keys: {', '.join(missing_theme_keys)}")

    if not isinstance(data.get("layout_style"), str):
        raise ValueError("layout_style must be a string.")

    return data


def main() -> None:
    """Demonstrate validation with one valid JSON payload and one invalid example."""
    valid_payload = json.dumps(
        {
            "detected_sentiment": "optimistic",
            "theme": {
                "background_color": "#0f172a",
                "primary_text": "#f8fafc",
                "accent_color": "#38bdf8",
                "font_family_heading": "Georgia",
                "font_family_body": "Arial",
            },
            "layout_style": "glassmorphic",
        }
    )

    invalid_payload = json.dumps(
        {
            "detected_sentiment": "calm",
            "theme": {
                "background_color": "#111827",
                "primary_text": "#f9fafb",
            },
            "layout_style": "modern",
        }
    )

    print("Valid payload:")
    print(validate_designer_json(valid_payload))

    print("\nInvalid payload:")
    try:
        validate_designer_json(invalid_payload)
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()
