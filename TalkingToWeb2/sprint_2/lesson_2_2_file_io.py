import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "essays"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def write_file(file_path: str, content: str) -> str:
    """Write content to a file inside the output/essays directory and return the saved path."""
    resolved_output_dir = OUTPUT_DIR.resolve()
    candidate_path = Path(file_path).expanduser()

    if not candidate_path.is_absolute():
        candidate_path = (PROJECT_ROOT / candidate_path).resolve()
    else:
        candidate_path = candidate_path.resolve()

    try:
        candidate_path.relative_to(resolved_output_dir)
    except ValueError as error:
        raise ValueError("Security violation: file path must stay inside the output/essays directory") from error

    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(content, encoding="utf-8")
    return str(candidate_path)


def main() -> None:
    """Demonstrate writing a small sample HTML file to the essays output folder."""
    sample_content = "<h1>Sample Page</h1><p>File I/O is working.</p>"
    saved_path = write_file(str(OUTPUT_DIR / "sample.html"), sample_content)
    print(f"Wrote file to: {saved_path}")


if __name__ == "__main__":
    main()
