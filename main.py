"""Daily run: collect deals -> pick the best unposted one -> render card -> post.
Usage: python main.py [--dry-run]   (dry-run renders the card but doesn't post)"""
import json
import os
import sys

from card import render
from sources import SOURCES

CFG = json.load(open("config.json", encoding="utf-8"))
POSTED = "posted.json"


def load_posted():
    try:
        return set(json.load(open(POSTED, encoding="utf-8")))
    except FileNotFoundError:
        return set()


def main(dry_run):
    posted = load_posted()
    deals = []
    for name in CFG["sources"]:
        deals += SOURCES[name](CFG)
    good = [d for d in deals if d["id"] not in posted
            and d["discount_pct"] >= CFG["min_discount_pct"]]
    if not good:
        print("No new qualifying deals today.")
        return
    best = max(good, key=lambda d: d["discount_pct"])

    os.makedirs("out", exist_ok=True)
    fname = f"deal_{abs(hash(best['id'])) % 10**8}.png"
    render(best, os.path.join("out", fname), CFG["brand"])
    caption = (f"{best['title']}\n\n₪{best['price']:g} במקום ₪{best['old_price']:g} "
               f"(הנחה של {best['discount_pct']}%)\n\nהקישור בביו\n\n{CFG['hashtags']}")
    print("Best deal:", best["title"], f"{best['discount_pct']}%")

    if dry_run:
        print("Dry run - card saved to out/" + fname)
        return
    from publish import post_image
    post_id = post_image(f"{os.environ['IMAGE_BASE_URL']}/{fname}", caption)
    posted.add(best["id"])
    json.dump(sorted(posted), open(POSTED, "w", encoding="utf-8"), ensure_ascii=False)
    print("Posted:", post_id)


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
