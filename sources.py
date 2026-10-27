"""Deal sources. Each returns a list of deal dicts:
{id, title, price, old_price, discount_pct, url}
Add a new source by writing a function and registering it in SOURCES."""
import json
import re


def _finish(d):
    d["discount_pct"] = round((1 - d["price"] / d["old_price"]) * 100)
    return d


def from_queue(cfg):
    """Deals listed by hand/other tools in deals_queue.json."""
    try:
        with open("deals_queue.json", encoding="utf-8") as f:
            return [_finish(x) for x in json.load(f)]
    except FileNotFoundError:
        return []


def from_rss(cfg):
    """Generic RSS: reads price/old price from the entry text (e.g. 'מחיר: 99 ₪ במקום 199 ₪')."""
    import feedparser
    deals = []
    for url in cfg.get("rss_feeds", []):
        for e in feedparser.parse(url).entries:
            text = f"{e.get('title', '')} {e.get('summary', '')}"
            nums = [float(n.replace(",", "")) for n in re.findall(r"(\d[\d,]*\.?\d*)\s*(?:₪|ש\"ח|שקל)", text)]
            if len(nums) >= 2 and nums[1] > nums[0] > 0:
                deals.append(_finish({"id": e.get("id", e.link), "title": e.title.strip(),
                                      "price": nums[0], "old_price": nums[1], "url": e.link}))
    return deals


SOURCES = {"queue": from_queue, "rss": from_rss}
