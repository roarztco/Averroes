from strands import tool
import requests
import re


@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for relevant pages about a learning topic."""

    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "SkillFoundry/0.1"
    }

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 5,
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()
    results = data["query"]["search"]

    results_text = ""

    for result in results:
        snippet = re.sub(r"<.*?>", "", result["snippet"])

        results_text += "Title: " + result["title"] + "\n"
        results_text += "Snippet: " + snippet + "\n"
        results_text += "Page ID: " + str(result["pageid"]) + "\n\n"

    return results_text


@tool
def read_wikipedia_page(title: str) -> str:
    """Read the introduction of a specific Wikipedia page."""

    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "SkillFoundry/0.1"
    }

    params = {
        "action": "query",
        "prop": "extracts|info",
        "inprop": "url",
        "titles": title,
        "explaintext": True,
        "exintro": True,
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    result = ""
    result += "Title: " + page.get("title", "") + "\n"
    result += "Source: " + page.get("fullurl", "") + "\n\n"
    result += page.get("extract", "")

    return result