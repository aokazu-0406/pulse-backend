import json
import os
from datetime import datetime, timezone

import feedparser
import anthropic

GENRES = {
    "hardware": {
        "label": "PC自作・ハードウェア",
        "feeds": [
            "https://www.itmedia.co.jp/pcuser/rss/index.rdf",
        ],
    },
    "android": {
        "label": "Android開発",
        "feeds": [
            "https://android-developers.googleblog.com/feeds/posts/default",
        ],
    },
    # 他ジャンルも同様に追加
}

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SUMMARY_PROMPT = """あなたは編集者です。以下の記事タイトルと概要から、
絵文字1つ・キーワード(16文字以内)・事実/背景/影響の3行要約をJSONで出力してください。
煽り表現、感嘆符は禁止。出力はJSONのみ。

フォーマット:
{{"emoji": "🔋", "kw": "全固体電池量産", "f1": "...", "f2": "...", "f3": "..."}}

記事タイトル: {title}
概要: {summary}
"""

def summarize(title, summary):
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": SUMMARY_PROMPT.format(title=title, summary=summary)}],
    )
    text = resp.content[0].text.strip()
    return json.loads(text)

def fetch_genre(genre_id, config):
    articles = []
    for url in config["feeds"]:
        parsed = feedparser.parse(url)
        for entry in parsed.entries[:5]:
            try:
                data = summarize(entry.get("title", ""), entry.get("summary", ""))
            except Exception:
                continue
            articles.append({
                "genre": genre_id,
                "emoji": data["emoji"],
                "kw": data["kw"],
                "f1": data["f1"],
                "f2": data["f2"],
                "f3": data["f3"],
                "source": parsed.feed.get("title", url),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
            })
    return articles

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
