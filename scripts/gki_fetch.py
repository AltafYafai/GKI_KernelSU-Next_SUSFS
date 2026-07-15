import os
import re
import base64
import time
import http.client
import urllib.request
import urllib.error
from datetime import datetime

BASE_URL = "https://android.googlesource.com/kernel/common/+/refs/heads"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

TARGETS = {
    ("android12", "5.10"): ("2021-08", "2025-12", "2024-08"),
}

import binascii

ERRORS = (urllib.error.HTTPError, urllib.error.URLError,
          TimeoutError, http.client.RemoteDisconnected,
          ConnectionResetError, OSError, binascii.Error)


def get_end_date(end: str | None) -> str:
    """Returns end date: if None, returns the current month"""
    if end is not None:
        return end
    return datetime.now().strftime("%Y-%m")


def make_date_range(start: str, end: str) -> list[str]:
    """Generates a YYYY-MM list from start to end"""
    sy, sm = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    dates = []
    y, m = sy, sm
    while (y, m) <= (ey, em):
        dates.append(f"{y}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return dates


def try_fetch(url: str) -> str | None:
    """Attempts to request a URL, returns None if failed"""
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return base64.b64decode(resp.read()).decode("utf-8", errors="replace")
    except ERRORS:
        return None


def fetch_makefile(android_ver: str, kernel_ver: str, date: str,
                   dep_cutoff: str) -> str | None:
    """Fetches Makefile for a dated branch. Tries expected path first, falls back on failure"""
    branch = f"{android_ver}-{kernel_ver}-{date}"
    if dep_cutoff and date <= dep_cutoff:
        paths = [f"deprecated/{branch}", branch]
    else:
        paths = [branch, f"deprecated/{branch}"]

    for p in paths:
        url = f"{BASE_URL}/{p}/Makefile?format=TEXT"
        text = try_fetch(url)
        if text is not None:
            return text
        time.sleep(0.3)
    return None


def fetch_lts(android_ver: str, kernel_ver: str) -> str | None:
    """Fetches LTS branch Makefile"""
    lts_branch = f"{android_ver}-{kernel_ver}-lts"
    url = f"{BASE_URL}/{lts_branch}/Makefile?format=TEXT"
    return try_fetch(url)


def parse_version(makefile_text: str) -> tuple[str, str, str] | None:
    """Extracts VERSION, PATCHLEVEL, SUBLEVEL from Makefile"""
    vals = {}
    for key in ("VERSION", "PATCHLEVEL", "SUBLEVEL"):
        m = re.search(rf"^{key}\s*=\s*(\d+)", makefile_text, re.MULTILINE)
        if not m:
            return None
        vals[key] = m.group(1)
    return vals["VERSION"], vals["PATCHLEVEL"], vals["SUBLEVEL"]


def json_path(android_ver: str, kernel_ver: str) -> str:
    """Returns the corresponding JSON file path"""
    return os.path.join(DATA_DIR, android_ver, f"{kernel_ver}.json")
