import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Search the web using Bing's RSS feed and return a small result list."""
    if not query.strip():
        raise ValueError("A search query is required.")

    encoded_query = urllib.parse.quote_plus(query)
    rss_url = f"https://www.bing.com/search?format=rss&q={encoded_query}"
    request = urllib.request.Request(rss_url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            xml_text = response.read().decode("utf-8", errors="ignore")
    except urllib.error.URLError as error:
        raise RuntimeError(f"Web search failed: {error}") from error

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return [{"title": "No results found", "url": "", "snippet": "The search feed could not be parsed."}]

    results = []
    for item in root.findall(".//item")[:max_results]:
        title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        snippet = (item.findtext("description") or "").strip()

        if title and url:
            results.append({"title": title, "url": url, "snippet": snippet})

    if not results:
        return [{"title": "No results found", "url": "", "snippet": "Bing did not return any visible results."}]

    return results


def main() -> None:
    """Run a simple command-line example that asks for a topic and prints the search results."""
    topic = input("Enter a topic to research: ").strip() or "artificial intelligence"
    results = search_web(topic)

    print(f"\nTop results for: {topic}\n")
    for index, result in enumerate(results, start=1):
        print(f"{index}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet']}")
        print()


if __name__ == "__main__":
    main()
