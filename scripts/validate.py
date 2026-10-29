#!/usr/bin/env python3
"""Validate a Resilience Watch report before publishing.

Usage: python3 scripts/validate.py data/latest.json [data/history.json]
Exits non-zero with a list of problems if the report is malformed.
"""
import json, sys
from datetime import datetime

LEVELS = {1, 2, 3, 4, 5}
SEV = {"act", "watch", "background"}
CONF = {"high", "medium", "low"}
TIERS = {"1", "2", "3"}
TRENDS = {"rising", "steady", "falling", "new"}

def err(problems, msg):
    problems.append(msg)

def check_sources(problems, where, srcs, required=True):
    if not srcs:
        if required:
            err(problems, f"{where}: no sources")
        return
    for s in srcs:
        u = s.get("url", "")
        if not (u.startswith("https://") or u.startswith("http://")):
            err(problems, f"{where}: bad source url {u!r}")
        if not s.get("title"):
            err(problems, f"{where}: source missing title")

def check_item(problems, where, it):
    for k in ("title", "what", "mechanism"):
        if not it.get(k):
            err(problems, f"{where}: missing {k}")
    if it.get("severity") not in SEV:
        err(problems, f"{where}: severity must be one of {sorted(SEV)}")
    if str(it.get("confidence", "")).lower() not in CONF:
        err(problems, f"{where}: confidence must be high/medium/low")
    if str(it.get("tier", "")) not in TIERS:
        err(problems, f"{where}: tier must be 1/2/3")
    check_sources(problems, where, it.get("sources"))

def validate(r):
    p = []
    try:
        datetime.fromisoformat(r["generated_at"].replace("Z", "+00:00"))
    except Exception:
        err(p, "generated_at missing or not ISO 8601")
    if r.get("level") not in LEVELS:
        err(p, "level must be 1-5")
    if r.get("prev_level") not in LEVELS | {None}:
        err(p, "prev_level must be 1-5 or null")
    for k in ("headline", "bottom_line", "change_reason"):
        if not r.get(k):
            err(p, f"missing {k}")
    if len(r.get("headline", "").split()) > 14:
        err(p, "headline over 14 words")
    if not r.get("actions"):
        err(p, "actions empty")
    secs = r.get("sections") or []
    if len(secs) < 3:
        err(p, "fewer than 3 domain sections")
    for i, s in enumerate(secs):
        if not s.get("domain"):
            err(p, f"sections[{i}]: missing domain")
        for j, it in enumerate(s.get("items") or []):
            check_item(p, f"sections[{i}].items[{j}]", it)
    for j, it in enumerate(r.get("alabama") or []):
        check_item(p, f"alabama[{j}]", it)
    if not r.get("alabama"):
        err(p, "alabama layer empty (report quiet conditions as an item)")
    for j, s in enumerate(r.get("signals") or []):
        if not s.get("name") or not s.get("reading"):
            err(p, f"signals[{j}]: needs name and reading")
    for j, s in enumerate(r.get("slow_burns") or []):
        if s.get("trend") not in TRENDS:
            err(p, f"slow_burns[{j}]: trend must be one of {sorted(TRENDS)}")
        if not s.get("threat") or not s.get("horizon"):
            err(p, f"slow_burns[{j}]: needs threat and horizon")
    tw = r.get("tripwires") or {}
    if not tw.get("up") or not tw.get("down"):
        err(p, "tripwires need both up and down")
    return p

def validate_history(h):
    p = []
    if not isinstance(h, list):
        return ["history must be a list"]
    dates = [x.get("date") for x in h]
    if dates != sorted(dates):
        p.append("history not sorted by date")
    if len(dates) != len(set(dates)):
        p.append("history has duplicate dates")
    for x in h:
        if x.get("level") not in LEVELS:
            p.append(f"history {x.get('date')}: bad level")
    return p

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        rep = json.load(f)
    problems = validate(rep)
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            problems += validate_history(json.load(f))
    if problems:
        print("INVALID:\n- " + "\n- ".join(problems))
        sys.exit(1)
    print("OK")
