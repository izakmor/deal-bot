"""Posts the next unposted evergreen carousel from content_cards.POSTS (in order).
Usage: python content_main.py [--render-only] [--slug SLUG]
State is kept in posted.json under keys like "content-habit_coffee"."""
import json
import os
import re
import sys
import time

from content_cards import META, POSTS, build_all

POSTED = "posted.json"
OUT = "out/content"


def load_posted():
    try:
        return set(json.load(open(POSTED, encoding="utf-8")))
    except FileNotFoundError:
        return set()


def caption(slug):
    m = META[slug]
    return (f"{m['title']}\n\n{m['sub']}\n\n"
            "המספרים הם דוגמה לחישוב בלבד, לא הבטחה ולא ייעוץ השקעות.\n\n"
            "#חיסכון #כסף #פיננסים #כלכלה #כספים")


def pick(slug=None):
    posted = load_posted()
    if slug:
        return slug
    for s in POSTS:
        if f"content-{s}" not in posted:
            return s
    return None


def main(render_only, slug=None):
    slug = pick(slug)
    if not slug:
        print("Queue is empty - every post has been published.")
        return
    paths = [os.path.join(OUT, f"{slug}_{i}.png") for i in (1, 2, 3)]
    if render_only or not all(os.path.exists(p) for p in paths):
        paths = build_all(OUT, only=[slug])
        print("Rendered:", paths)
    if render_only:
        return
    from publish import post_carousel
    time.sleep(20)  # let raw.githubusercontent.com serve the freshly pushed images
    base = os.environ["IMAGE_BASE_URL"]
    post_id = post_carousel([f"{base}/content/{os.path.basename(p)}" for p in paths], caption(slug))
    posted = load_posted()
    posted.add(f"content-{slug}")
    json.dump(sorted(posted), open(POSTED, "w", encoding="utf-8"), ensure_ascii=False)
    print("Posted:", slug, post_id)


if __name__ == "__main__":
    args = sys.argv[1:]
    main("--render-only" in args, args[args.index("--slug") + 1] if "--slug" in args else None)
