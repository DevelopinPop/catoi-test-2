#!/usr/bin/env python3
"""Builds the website into ./_site from whatever is in ./scoreboards/.

Accepted in scoreboards/:
  <id>/data.json      a contest folder made by the archiver notebook (flags/, logo.* and meta.json are
                      copied along; its index.html is rebuilt from tools/viewer.html, so every contest
                      always gets the newest scoreboard design)
  <id>/index.html     a folder that only has a finished page (no data.json): copied as it is
  <id>.json           just the data
  <id>.html           a saved scoreboard page; its embedded data is extracted and rebuilt

Run locally:  python3 tools/build_site.py   then   python3 -m http.server -d _site
In GitHub the workflow in .github/workflows/pages.yml runs this on every push.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT, TOOLS = ROOT / "scoreboards", ROOT / "_site", ROOT / "tools"
SKIP_DIRS = {"raw"}          # raw crawls can be huge and are not needed by the site


def warn(msg):
    print(f"::warning::{msg}")          # shown as a yellow note in the GitHub Actions log


def slug(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-.") or "contest"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_html_data(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^\s*const DATA = (\{.*\});\s*$", text, re.M)
    if not m:
        raise ValueError("no 'const DATA = {...};' line found in the page")
    return json.loads(m.group(1))


def check(data):
    if not isinstance(data, dict):
        raise ValueError("data is not a JSON object")
    for key in ("tasks", "users"):
        if not isinstance(data.get(key), list) or not data[key]:
            raise ValueError(f"missing or empty '{key}'")
    if "duration" not in data:
        raise ValueError("missing 'duration'")


def collect():
    items, seen = [], set()
    if not SRC.is_dir():
        return items
    for p in sorted(SRC.iterdir(), key=lambda p: p.name.lower()):
        if p.name.startswith((".", "_")):
            continue
        try:
            if p.is_dir():
                cid, folder, data, prebuilt = slug(p.name), p, None, None
                if (p / "data.json").is_file():
                    data = read_json(p / "data.json")
                elif (p / "index.html").is_file():
                    prebuilt = p / "index.html"
                else:
                    warn(f"scoreboards/{p.name}/ has neither data.json nor index.html: skipped")
                    continue
            elif p.suffix.lower() == ".json":
                cid, folder, data, prebuilt = slug(p.stem), None, read_json(p), None
            elif p.suffix.lower() in (".html", ".htm"):
                cid, folder, data, prebuilt = slug(p.stem), None, read_html_data(p), None
            else:
                continue                                  # README.md and the like
            if data is not None:
                check(data)
        except Exception as e:                            # one broken contest must not block the site
            warn(f"scoreboards/{p.name}: {e}: skipped")
            continue
        base, n = cid, 2
        while cid in seen:
            cid, n = f"{base}-{n}", n + 1
        seen.add(cid)
        items.append({"id": cid, "folder": folder, "data": data, "prebuilt": prebuilt})
    return items


def make_meta(cid, data, old):
    unoff = set(data.get("unofficial") or [])
    users = data["users"]
    return {
        "id": cid,
        "title": data.get("title") or old.get("title") or cid,
        "participants": len(users),
        "official": sum(1 for u in users if not (u.get("unofficial") or u.get("name") in unoff)),
        "tasks": [t.get("name", "") for t in data["tasks"]],
        "duration": data.get("duration"),
        "logo": data.get("logo") or old.get("logo", ""),
        "generated": old.get("generated", ""),
    }


def main():
    template = (TOOLS / "viewer.html").read_text(encoding="utf-8")
    home = (TOOLS / "home.html").read_text(encoding="utf-8")
    if "__DATA_JSON__" not in template:
        sys.exit("tools/viewer.html has no __DATA_JSON__ placeholder")

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "contests").mkdir(parents=True)
    metas = []

    for c in collect():
        dest = OUT / "contests" / c["id"]
        folder, data = c["folder"], c["data"]
        old = {}
        if folder is not None:
            if (folder / "meta.json").is_file():
                try:
                    old = read_json(folder / "meta.json")
                except ValueError:
                    pass
            skip_index = data is not None
            shutil.copytree(folder, dest, ignore=lambda d, names, f=folder, s=skip_index: [
                n for n in names if (Path(d) == f and (n in SKIP_DIRS or (s and n == "index.html")))])
        else:
            dest.mkdir(parents=True)

        if data is not None:
            payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            (dest / "data.json").write_text(payload, encoding="utf-8")
            page = template.replace("__DATA_JSON__", payload.replace("</", "<\\/"))
            (dest / "index.html").write_text(page, encoding="utf-8")
            meta = make_meta(c["id"], data, old)
        else:
            meta = {"id": c["id"], "title": old.get("title") or c["id"], "participants": old.get("participants", 0),
                    "official": old.get("official", 0), "tasks": old.get("tasks", []), "duration": old.get("duration"),
                    "logo": old.get("logo", ""), "generated": old.get("generated", "")}
        (dest / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        metas.append(meta)
        print(f"  contests/{c['id']}/  {meta['title']}  ({meta['participants']} contestants)")

    metas.sort(key=lambda m: m["id"].lower())
    metas.sort(key=lambda m: m.get("generated") or "", reverse=True)       # newest crawl first, then by id
    (OUT / "contests" / "index.json").write_text(json.dumps(metas, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "index.html").write_text(home, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(metas)} contest(s) into {OUT.name}/")


if __name__ == "__main__":
    main()
