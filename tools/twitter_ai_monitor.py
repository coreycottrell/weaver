#!/usr/bin/env python3
"""
Twitter AI Account Monitor - Read AI accounts without API reads.
Uses browser-based scraping since free tier only gets 100 reads/month.

WEAVER AI-CIV
Created: 2026-01-04
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional
import time

# === Configuration ===
MONITOR_FILE = Path("/home/corey/projects/AI-CIV/WEAVER/.claude/twitter_monitor_cache.json")

# Priority AI accounts to monitor
AI_ACCOUNTS = {
    "researchers": [
        {"handle": "AndrewYNg", "name": "Andrew Ng", "priority": 1},
        {"handle": "karpathy", "name": "Andrej Karpathy", "priority": 1},
        {"handle": "ylecun", "name": "Yann LeCun", "priority": 1},
        {"handle": "demishassabis", "name": "Demis Hassabis", "priority": 1},
        {"handle": "JeffDean", "name": "Jeff Dean", "priority": 2},
        {"handle": "DrJimFan", "name": "Jim Fan", "priority": 2},
        {"handle": "AravSrinivas", "name": "Aravind Srinivas", "priority": 2},
    ],
    "labs": [
        {"handle": "OpenAI", "name": "OpenAI", "priority": 1},
        {"handle": "GoogleDeepMind", "name": "DeepMind", "priority": 1},
        {"handle": "AnthropicAI", "name": "Anthropic", "priority": 1},
        {"handle": "HuggingFace", "name": "Hugging Face", "priority": 2},
        {"handle": "xaboratory", "name": "xAI", "priority": 2},
    ],
    "collectives": [
        {"handle": "void_comind", "name": "Void (comind)", "priority": 1},
        {"handle": "cameronsworld", "name": "Cameron Pfiffer", "priority": 1},
    ]
}


def get_nitter_rss(handle: str, instance: str = "nitter.privacydev.net") -> Optional[str]:
    """Try to get RSS from Nitter instance."""
    try:
        url = f"https://{instance}/{handle}/rss"
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (compatible; WEAVER-AI-CIV/1.0)"
        })
        if response.status_code == 200 and "<?xml" in response.text:
            return response.text
    except Exception as e:
        pass
    return None


def get_syndication_feed(handle: str) -> Optional[dict]:
    """
    Try Twitter's public syndication endpoint (no auth needed).
    Works for public timelines, limited to recent tweets.
    """
    try:
        # Twitter syndication endpoint (public, no auth)
        url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if response.status_code == 200:
            return {"html": response.text[:5000], "source": "syndication"}
    except Exception:
        pass
    return None


def scrape_account_page(handle: str) -> Optional[dict]:
    """
    Fallback: Try to get basic info from Twitter page.
    Very limited but works without API.
    """
    try:
        url = f"https://twitter.com/{handle}"
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html"
        })
        if response.status_code == 200:
            # Just confirm account exists and is accessible
            return {
                "accessible": True,
                "url": url,
                "fetched": datetime.now().isoformat()
            }
    except Exception:
        pass
    return None


def check_account(handle: str) -> dict:
    """Check an account using available methods."""
    result = {
        "handle": handle,
        "checked": datetime.now().isoformat(),
        "methods_tried": [],
        "data": None
    }

    # Try Nitter RSS first (best if working)
    for instance in ["nitter.privacydev.net", "nitter.poast.org", "nitter.net"]:
        result["methods_tried"].append(f"nitter:{instance}")
        rss = get_nitter_rss(handle, instance)
        if rss:
            result["data"] = {"source": "nitter", "instance": instance, "has_feed": True}
            return result

    # Try syndication
    result["methods_tried"].append("syndication")
    syn = get_syndication_feed(handle)
    if syn:
        result["data"] = syn
        return result

    # Fallback to page check
    result["methods_tried"].append("page_scrape")
    page = scrape_account_page(handle)
    if page:
        result["data"] = page
        return result

    result["data"] = {"accessible": False, "error": "All methods failed"}
    return result


def run_monitor() -> dict:
    """Run full monitor cycle on all accounts."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "accounts_checked": 0,
        "methods_working": set(),
        "results": {}
    }

    all_accounts = []
    for category, accounts in AI_ACCOUNTS.items():
        for acc in accounts:
            all_accounts.append({**acc, "category": category})

    # Sort by priority
    all_accounts.sort(key=lambda x: x["priority"])

    for acc in all_accounts:
        print(f"Checking @{acc['handle']} ({acc['name']})...")
        result = check_account(acc["handle"])
        report["results"][acc["handle"]] = result
        report["accounts_checked"] += 1

        if result["data"] and result["data"].get("source"):
            report["methods_working"].add(result["data"]["source"])

        # Be nice - small delay
        time.sleep(1)

    report["methods_working"] = list(report["methods_working"])

    # Save cache
    MONITOR_FILE.write_text(json.dumps(report, indent=2))
    print(f"\nSaved to {MONITOR_FILE}")

    return report


def print_summary(report: dict):
    """Print human-readable summary."""
    print("\n" + "="*60)
    print("TWITTER AI MONITOR SUMMARY")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}")
    print(f"Accounts checked: {report['accounts_checked']}")
    print(f"Working methods: {', '.join(report['methods_working']) or 'None'}")
    print()

    accessible = []
    failed = []

    for handle, result in report["results"].items():
        if result["data"] and result["data"].get("accessible", True):
            accessible.append(handle)
        else:
            failed.append(handle)

    print(f"Accessible: {len(accessible)}")
    for h in accessible:
        print(f"  - @{h}")

    if failed:
        print(f"\nFailed: {len(failed)}")
        for h in failed:
            print(f"  - @{h}")

    print()


def get_accounts_list() -> str:
    """Get formatted list of all monitored accounts."""
    lines = ["# AI Twitter Accounts to Monitor", ""]

    for category, accounts in AI_ACCOUNTS.items():
        lines.append(f"## {category.title()}")
        lines.append("")
        for acc in sorted(accounts, key=lambda x: x["priority"]):
            lines.append(f"- @{acc['handle']} - {acc['name']} (P{acc['priority']})")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print(get_accounts_list())
    else:
        report = run_monitor()
        print_summary(report)
