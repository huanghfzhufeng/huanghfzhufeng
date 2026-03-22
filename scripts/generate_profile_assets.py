#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import pathlib
import urllib.parse
import urllib.request


USERNAME = os.environ.get("PROFILE_USERNAME", "huanghfzhufeng")
OUTPUT_PATH = pathlib.Path("assets/metrics.svg")
API_BASE = "https://api.github.com"


def api_get(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-assets",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def get_user() -> dict:
    return api_get(f"{API_BASE}/users/{USERNAME}")


def get_repositories() -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        params = urllib.parse.urlencode(
            {
                "per_page": 100,
                "page": page,
                "type": "owner",
                "sort": "updated",
            }
        )
        batch = api_get(f"{API_BASE}/users/{USERNAME}/repos?{params}")
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def get_merged_pr_count() -> int:
    query = urllib.parse.quote(f"type:pr author:{USERNAME} is:merged")
    payload = api_get(f"{API_BASE}/search/issues?q={query}")
    return int(payload["total_count"])


def build_metrics() -> dict[str, int]:
    user = get_user()
    repos = get_repositories()

    return {
        "public_stars": sum(int(repo["stargazers_count"]) for repo in repos),
        "repositories": int(user["public_repos"]),
        "merged_prs": get_merged_pr_count(),
        "public_forks": sum(int(repo["forks_count"]) for repo in repos),
    }


def render_svg(metrics: dict[str, int]) -> str:
    cards = [
        ("PUBLIC STARS", f'{metrics["public_stars"]:,}'),
        ("PUBLIC REPOS", f'{metrics["repositories"]:,}'),
        ("MERGED PRS", f'{metrics["merged_prs"]:,}'),
        ("PUBLIC FORKS", f'{metrics["public_forks"]:,}'),
    ]

    card_width = 250
    card_height = 132
    start_x = 46
    gap = 18
    y = 64

    card_blocks: list[str] = []
    for index, (label, value) in enumerate(cards):
        x = start_x + index * (card_width + gap)
        line_color = "#0F766E" if index % 2 == 0 else "#C97A1A"
        circle_x = x + card_width - 34
        circle_y = y + 28
        card_blocks.append(
            f"""
  <g>
    <rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="22" fill="#FFFFFF" fill-opacity="0.80" stroke="#E6ECEC"/>
    <rect x="{x + 24}" y="{y + 24}" width="72" height="4" rx="2" fill="{line_color}" fill-opacity="0.95"/>
    <circle cx="{circle_x}" cy="{circle_y}" r="9" fill="{line_color}" fill-opacity="0.10" stroke="{line_color}" stroke-width="1.5"/>
    <text x="{x + 24}" y="{y + 56}" fill="#64748B" font-size="13" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif" letter-spacing="2">
      {label}
    </text>
    <text x="{x + 24}" y="{y + 110}" fill="#0F172A" font-size="44" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif">
      {value}
    </text>
  </g>"""
        )

    return f"""<svg width="1200" height="236" viewBox="0 0 1200 236" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="metricsBg" x1="62" y1="28" x2="1138" y2="212" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FBFAF7"/>
      <stop offset="1" stop-color="#F4F7F7"/>
    </linearGradient>
    <filter id="metricsShadow" x="0" y="0" width="1200" height="236" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#0F172A" flood-opacity="0.05"/>
    </filter>
  </defs>

  <g filter="url(#metricsShadow)">
    <rect x="22" y="18" width="1156" height="200" rx="28" fill="url(#metricsBg)"/>
    <rect x="22.5" y="18.5" width="1155" height="199" rx="27.5" stroke="#E5E7EB"/>
  </g>

  <path d="M46 46H248" stroke="#D8E3E2" stroke-width="2"/>
  <path d="M970 46H1152" stroke="#E6D6BE" stroke-width="2"/>
  <rect x="46" y="42" width="8" height="8" rx="4" fill="#0F766E"/>
  <rect x="1144" y="42" width="8" height="8" rx="4" fill="#C97A1A"/>

  <text x="46" y="48" fill="#64748B" font-size="14" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif" letter-spacing="3">
    PUBLIC GITHUB SNAPSHOT
  </text>
  <text x="952" y="48" fill="#94A3B8" font-size="13" font-weight="700" font-family="SF Pro Text, Segoe UI, Arial, sans-serif" letter-spacing="2">
    AUTO-REFRESHED
  </text>

  {"".join(card_blocks)}
</svg>
"""


def main() -> None:
    metrics = build_metrics()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_svg(metrics), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH} for {USERNAME}: {metrics}")


if __name__ == "__main__":
    main()
