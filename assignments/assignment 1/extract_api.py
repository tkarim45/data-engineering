import time
import requests
import pandas as pd

from config import HN_API_BASE, HN_SEARCH_QUERIES, HN_RESULTS_PER_QUERY


def extract_hn_stories():
    all_stories = {}

    for query in HN_SEARCH_QUERIES:
        print(f"  Searching HN for: '{query}'...")
        try:
            response = requests.get(
                f"{HN_API_BASE}/search",
                params={
                    "query": query,
                    "tags": "story",
                    "hitsPerPage": HN_RESULTS_PER_QUERY,
                },
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            for hit in data.get("hits", []):
                story_id = hit.get("objectID", "")
                if story_id not in all_stories:
                    all_stories[story_id] = {
                        "story_id": story_id,
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "author": hit.get("author", ""),
                        "created_at": hit.get("created_at", ""),
                        "points": hit.get("points", 0),
                        "num_comments": hit.get("num_comments", 0),
                        "story_text": hit.get("story_text") or "",
                    }

            print(f"    Found {len(data.get('hits', []))} results.")
            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"    Error fetching '{query}': {e}")

    if not all_stories:
        raise RuntimeError(
            "Failed to fetch any stories from HackerNews API. "
            "Check your internet connection and try again."
        )

    df = pd.DataFrame(list(all_stories.values()))
    print(f"  Extracted {len(df)} unique HackerNews stories total.")
    return df
