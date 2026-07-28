import feedparser
def fetch_genre(genre_id, config):
    articles = []
    for url in config["feeds"]:
        parsed = feedparser.parse(url)
        for entry in parsed.entries[:5]:
            articles.append({
                "genre": genre_id,
                "emoji": "📰",  # ジャンルごとに固定の絵文字を割り当てるだけでOK
                "kw": entry.get("title", "")[:30],
                "f1": entry.get("summary", "")[:60],
                "f2": "",
                "source": parsed.feed.get("title", url),
                "link": entry.get("link", ""),
            })
    return articles
import feedparser
import json
import os
from datetime import datetime, timezone

GENRES = {
    "hardware": {
        "feeds": ["https://www.itmedia.co.jp/pcuser/rss/index.rdf"],
    },
    "android": {
        "feeds": ["https://android-developers.googleblog.com/feeds/posts/default"],
    },
    # 他ジャンルも同様に追加していい
}

def main():
    all_articles = []
    for genre_id, config in GENRES.items():
        all_articles.extend(fetch_genre(genre_id, config))

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "articles": all_articles,
    }
    os.makedirs("data", exist_ok=True)
    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
