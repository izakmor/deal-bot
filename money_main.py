"""Daily run: Bank of Israel USD/ILS -> 3-slide carousel -> Instagram.
Usage: python money_main.py [--render-only]   (render-only: make the images, don't post)
Posts at most once per data date, so weekends/holidays without a new rate are skipped."""
import json
import os
import sys

from money_cards import build, caption, fetch

POSTED = "posted.json"


def load_posted():
    try:
        return set(json.load(open(POSTED, encoding="utf-8")))
    except FileNotFoundError:
        return set()


def main(render_only):
    series = fetch()
    key = f"money-{series[-1][0].isoformat()}"
    if key in load_posted():
        print("Already posted for", series[-1][0], "- nothing to do.")
        return
    paths, series = build("out", series)
    print("Rendered:", paths)
    if render_only:
        return
    from publish import post_carousel
    import time
    time.sleep(20)  # let raw.githubusercontent.com serve the freshly pushed images
    base = os.environ["IMAGE_BASE_URL"]
    post_id = post_carousel([f"{base}/{os.path.basename(p)}" for p in paths], caption(series))
    posted = load_posted()
    posted.add(key)
    json.dump(sorted(posted), open(POSTED, "w", encoding="utf-8"), ensure_ascii=False)
    print("Posted:", post_id)


if __name__ == "__main__":
    main("--render-only" in sys.argv)
