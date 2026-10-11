#!/usr/bin/env python3
"""Download every Wix-hosted photo listed in images.txt into assets/photos/ so the site
no longer depends on Wix hosting.

Run this on a computer with normal internet access:

    python3 fetch_images.py && python3 build.py

Then commit the new files in assets/photos/ and push.
"""
import pathlib, urllib.request, sys
root = pathlib.Path(__file__).parent
out = root / "assets" / "photos"; out.mkdir(parents=True, exist_ok=True)
ok = bad = 0
for mid in (root / "images.txt").read_text().split():
    dest = out / mid.replace("~mv2", "")
    if dest.exists(): continue
    req = urllib.request.Request("https://static.wixstatic.com/media/" + mid, headers={"User-Agent": "Mozilla/5.0"})
    try:
        dest.write_bytes(urllib.request.urlopen(req, timeout=30).read()); ok += 1; print("saved", dest.name)
    except Exception as e:
        bad += 1; print("FAILED", mid, e, file=sys.stderr)
print(f"{ok} downloaded, {bad} failed")
