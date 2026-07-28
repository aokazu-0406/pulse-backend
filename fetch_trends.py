def fetch_genre(genre_id, config):
    articles = []
    for url in config["feeds"]:
        parsed = feedparser.parse(url)
        for entry in parsed.entries[:5]:
            articles.append({
                "genre": genre_id,
                "emoji": "📰",  # ジャンルごとに固定の絵文字を割り当てるだけでOK
                "kw": entry.get("title", "")[:16],
                "f1": entry.get("summary", "")[:60],
                "f2": "",
                "source": parsed.feed.get("title", url),
                "link": entry.get("link", ""),
            })
    return articles
