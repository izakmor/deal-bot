"""Checks every story's visible Hebrew text for mistakes we have already made once.
Exit code 1 (with a list) if anything is found, so the workflow stops before posting."""
import html
import re
import sys

import story_cards as sc
import story_library  # noqa: F401

BANNED = ["אפילו ש", "בוא ", "התאם ", "{", "}", "None", "nan"]


def text_of(fragment):
    fragment = re.sub(r"</?(?:b|i|em|strong|span)(?: [^>]*)?>", "", fragment)  # inline tags must not add spaces
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def check():
    errors = []
    for slug, fn in sc.STORIES.items():
        slides, title, sub = fn()
        if len(slides) != 9:
            errors.append(f"{slug}: expected 9 slides, got {len(slides)}")
        for i, h in enumerate(slides, 1):
            body = re.sub(r"<svg.*?</svg>", " ", h.split("</style>")[-1], flags=re.S)
            h1s = [text_of(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S)]
            ps = [text_of(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", body, flags=re.S)]
            foots = [text_of(x) for x in re.findall(r"<div class=foot>(.*?)</div>", body, flags=re.S)]
            where = f"{slug} slide {i}"
            if "₪" in " ".join(h1s):
                errors.append(f"{where}: shekel sign in a headline (the display font has no glyph)")
            if i == 1:
                for t in h1s + ps:
                    if t.startswith("ו"):
                        errors.append(f"{where}: opening text starts with a connector: {t[:40]}")
            if ps and ps[0].startswith("ו"):
                errors.append(f"{where}: first paragraph starts with a connector: {ps[0][:40]}")
            for t in h1s + ps + foots:
                for bad in BANNED:
                    if bad in t:
                        errors.append(f"{where}: contains '{bad.strip()}': {t[:50]}")
                if re.search(r"\s[,.?!:;]", t) or "  " in t:
                    errors.append(f"{where}: spacing before punctuation: {t[:50]}")
                m = re.search(r"(?<![\w־])([א-ת]{2,}) \1(?![\w])", t)
                if m:
                    errors.append(f"{where}: repeated word '{m.group(1)}': {t[:50]}")
    return errors


if __name__ == "__main__":
    errs = check()
    for e in errs:
        print("LINT:", e)
    print(f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)
