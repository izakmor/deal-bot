"""Publishes an image to Instagram via the Graph API (Business account).
Needs env: IG_USER_ID, IG_ACCESS_TOKEN. image_url must be publicly reachable."""
import os
import time
import requests

API = "https://graph.facebook.com/v21.0"


def post_image(image_url, caption):
    uid, token = os.environ["IG_USER_ID"], os.environ["IG_ACCESS_TOKEN"]
    r = requests.post(f"{API}/{uid}/media", data={
        "image_url": image_url, "caption": caption, "access_token": token}, timeout=60)
    r.raise_for_status()
    creation_id = r.json()["id"]
    for _ in range(10):  # wait until the container is ready
        s = requests.get(f"{API}/{creation_id}", params={
            "fields": "status_code", "access_token": token}, timeout=30).json()
        if s.get("status_code") == "FINISHED":
            break
        time.sleep(3)
    r = requests.post(f"{API}/{uid}/media_publish", data={
        "creation_id": creation_id, "access_token": token}, timeout=60)
    r.raise_for_status()
    return r.json()["id"]
