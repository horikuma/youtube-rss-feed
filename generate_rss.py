import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime
from pathlib import Path

CHANNEL_LIST = "channels.txt"
OUTPUT_FILE = "custom_youtube_feed.xml"
MAX_VIDEOS_PER_CHANNEL = 5

fg = FeedGenerator()
fg.title("My YouTube Feed")
fg.link(href="https://www.youtube.com", rel="alternate")
fg.description("Aggregated feed of favorite YouTube channels")
fg.language("ja")

# チャンネルID一覧を読み込む
with open(CHANNEL_LIST, "r") as f:
    channel_ids = [line.strip() for line in f if line.strip()]

entries = []

for cid in channel_ids:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
    feed = feedparser.parse(url)
    for entry in feed.entries[:MAX_VIDEOS_PER_CHANNEL]:
        entries.append(
            {
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "channel": feed.feed.title,
            }
        )

# 新しい順に並べ替え
entries.sort(key=lambda e: e["published"], reverse=True)

# RSSに追加
for e in entries:
    fe = fg.add_entry()
    fe.title(f"[{e['channel']}] {e['title']}")
    fe.link(href=e["link"])
    fe.published(e["published"])

# 書き出し
fg.rss_file(OUTPUT_FILE)
print(f"{OUTPUT_FILE} generated with {len(entries)} entries.")
