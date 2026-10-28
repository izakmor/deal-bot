"""Publishes an image to Instagram via the Graph API (Business account).
Needs env: IG_USER_ID, IG_ACCESS_TOKEN. image_url must be publicly reachable."""
import os
import time
import requests

API = "https://graph.instagram.com/v21.0"  # token comes from "API setup with Instagram login"


def _post(path, **data):
    data["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    r = requests.post(f"{API}/{path}", data=data, timeout=60)
    if not r.ok:
        raise RuntimeError(f"Instagram API {path}: {r.status_code} {r.text}")
    return r.json()["id"]


def _wait_ready(container_id):
    for _ in range(20):
        s = requests.get(f"{API}/{container_id}", params={
            "fields": "status_code", "access_token": os.environ["IG_ACCESS_TOKEN"]}, timeout=30).json()
        if s.get("status_code") == "FINISHED":
            return
        if s.get("status_code") == "ERROR":
            raise RuntimeError(f"Container {container_id} failed: {s}")
        time.sleep(3)
    raise RuntimeError(f"Container {container_id} not ready in time")


def post_image(image_url, caption):
    uid = os.environ["IG_USER_ID"]
    creation_id = _post(f"{uid}/media", image_url=image_url, caption=caption)
    _wait_ready(creation_id)
    return _post(f"{uid}/media_publish", creation_id=creation_id)


def post_carousel(image_urls, caption):
    """2-10 images as one swipeable post."""
    uid = os.environ["IG_USER_ID"]
    children = []
    for url in image_urls:
        cid = _post(f"{uid}/media", image_url=url, is_carousel_item="true")
        _wait_ready(cid)
        children.append(cid)
    parent = _post(f"{uid}/media", media_type="CAROUSEL", children=",".join(children), caption=caption)
    _wait_ready(parent)
    return _post(f"{uid}/media_publish", creation_id=parent)


def check_token(issued_file="token_issued.txt", warn_days=50, fail_days=59):
    """Stops before posting if the Instagram token is rejected or about to expire.
    token_issued.txt holds the date the token was generated (update it when you renew)."""
    from datetime import date
    r = requests.get(f"{API}/me", params={"fields": "user_id,username",
                                           "access_token": os.environ["IG_ACCESS_TOKEN"]}, timeout=30)
    if not r.ok and not ("OAuthException" in r.text or '"code":190' in r.text.replace(" ", "")):
        print(f"::warning::Token check could not be completed ({r.status_code}); continuing. {r.text[:200]}")
        return
    if not r.ok:
        raise RuntimeError("Instagram token was rejected (expired or revoked). Generate a new one in the Meta app "
                           "dashboard (Instagram API setup > Generate token) and update the IG_ACCESS_TOKEN secret. "
                           f"API said: {r.status_code} {r.text}")
    try:
        age = (date.today() - date.fromisoformat(open(issued_file).read().strip())).days
    except (OSError, ValueError):
        print("No valid token_issued.txt; skipping the age check.")
        return
    if age >= fail_days:
        raise RuntimeError(f"Instagram token is {age} days old and probably expires within days. Renew it now.")
    if age >= warn_days:
        open("token_warning", "w").write(str(age))
        print(f"::warning::Instagram token is {age} days old. Renew it soon (tokens last about 60 days).")
