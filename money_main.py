"""Daily run: Bank of Israel USD/ILS -> 3-slide carousel -> Instagram.
Usage: python money_main.py [--render-only]   (render-only: make the images, don't post)
Posts at most once per data date, so weekends/holidays without a new rate are skipped.
With USE_SERIES_CACHE=1 the post step reuses the data and images from the render step,
so the Bank of Israel API is only called once per workflow run."""
import json
import os
import sys
import time
from datetime import date

from money_cards import build, caption, fetch, paths_for

POSTED = "posted.json"
CACHE = "series.json"


def load_posted():
    try:
        return set(json.load(open(POSTED, encoding="utf-8")))
    except FileNotFoundError:
        return set()


def get_series():
    if os.environ.get("USE_SERIES_CACHE") == "1" and os.path.exists(CACHE):
        return [(date.fromisoformat(d), v) for d, v in json.load(open(CACHE, encoding="utf-8"))]
    series = fetch()
    json.dump([(d.isoformat(), v) for d, v in series], open(CACHE, "w", encoding="utf-8"))
    return series


def main(render_only):
    series = get_series()
    key = f"money-{series[-1][0].isoformat()}"
    if key in load_posted():
        print("Already posted for", series[-1][0], "- nothing to do.")
        return
    paths = paths_for(series)
    if render_only or not all(os.path.exists(p) for p in paths):
        paths, series = build("out", series)
        print("Rendered:", paths)
    if render_only:
        return
    from publish import post_carousel
    time.sleep(20)  # let raw.githubusercontent.com serve the freshly pushed images
    base = os.environ["IMAGE_BASE_URL"]
    post_id = post_carousel([f"{base}/{os.path.basename(p)}" for p in paths], caption(series))
    posted = load_posted()
    posted.add(key)
    json.dump(sorted(posted), open(POSTED, "w", encoding="utf-8"), ensure_ascii=False)
    print("Posted:", post_id)


if __name__ == "__main__":
    main("--render-only" in sys.argv)
