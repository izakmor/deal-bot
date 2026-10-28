"""Posts the next unposted story carousel from story_cards.STORIES (in order).
Usage: python content_main.py [--render-only] [--slug SLUG]
State is kept in posted.json under keys like "story-story_compound"."""
import json
import os
import sys
import time

import story_cards as sc

POSTED = "posted.json"
OUT = "out/story"


def load_posted():
    try:
        return set(json.load(open(POSTED, encoding="utf-8")))
    except FileNotFoundError:
        return set()


def caption(m):
    return (f"{m['title']}\n\n{m['sub']}\n\n"
            "המספרים הם דוגמה לחישוב בלבד, לא הבטחה ולא ייעוץ השקעות.\n\n"
            "#חיסכון #כסף #פיננסים #כלכלה #כספים")


def pick(slug=None):
    if slug:
        return slug
    posted = load_posted()
    return next((s for s in sc.STORIES if f"story-{s}" not in posted), None)


def main(render_only, slug=None):
    slug = pick(slug)
    if not slug:
        print("Queue is empty - every story has been published.")
        return
    m = sc.meta(slug)
    paths = [os.path.join(OUT, f"{slug}_{i}.png") for i in range(1, m["count"] + 1)]
    if render_only or not all(os.path.exists(p) for p in paths):
        paths = sc.build(OUT, only=[slug])
        print("Rendered:", paths)
    if render_only:
        return
    from publish import post_carousel
    time.sleep(20)  # let raw.githubusercontent.com serve the freshly pushed images
    base = os.environ["IMAGE_BASE_URL"]
    post_id = post_carousel([f"{base}/story/{os.path.basename(p)}" for p in paths], caption(m))
    posted = load_posted()
    posted.add(f"story-{slug}")
    json.dump(sorted(posted), open(POSTED, "w", encoding="utf-8"), ensure_ascii=False)
    print("Posted:", slug, post_id)


if __name__ == "__main__":
    args = sys.argv[1:]
    main("--render-only" in args, args[args.index("--slug") + 1] if "--slug" in args else None)
