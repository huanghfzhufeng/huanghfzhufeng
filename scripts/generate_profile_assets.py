#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import os
import pathlib
import re
import urllib.parse
import urllib.request
from datetime import date, timedelta


USERNAME = os.environ.get("PROFILE_USERNAME", "huanghfzhufeng")
ASSETS_DIR = pathlib.Path("assets")
API_BASE = "https://api.github.com"
PROJECTS = [
    {
        "label": "SoftRight-AI",
        "repo": "SoftRight-AI",
        "accent": "#0F766E",
        "width": 236,
    },
    {
        "label": "GEO-Insight",
        "repo": "GEO-Insight",
        "accent": "#C97A1A",
        "width": 222,
    },
    {
        "label": "App-Mockup-Studio",
        "repo": "App-Mockup-Studio",
        "accent": "#0F766E",
        "width": 304,
    },
    {
        "label": "csccc",
        "repo": "csccc",
        "accent": "#C97A1A",
        "width": 168,
    },
]
EXTRA_LINK = {
    "label": "All repositories",
    "filename": "all-repositories.svg",
    "accent": "#0F766E",
    "width": 212,
}
CONTRIBUTION_WINDOW_DAYS = 84


def http_get(url: str) -> str:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-assets",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def api_get(url: str) -> dict:
    return json.loads(http_get(url))


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


def render_metrics_svg(metrics: dict[str, int]) -> str:
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


def contribution_date_range() -> tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=CONTRIBUTION_WINDOW_DAYS - 1)
    return start, end


def get_contribution_series() -> list[tuple[date, int]]:
    start, end = contribution_date_range()
    params = urllib.parse.urlencode(
        {
            "from": start.isoformat(),
            "to": end.isoformat(),
        }
    )
    html = http_get(f"https://github.com/users/{USERNAME}/contributions?{params}")
    pattern = re.compile(
        r'data-date="(?P<date>\d{4}-\d{2}-\d{2})"[^>]*></td>\s*<tool-tip[^>]*>(?P<tip>[^<]+)</tool-tip>',
        re.S,
    )
    counts: dict[str, int] = {}
    for match in pattern.finditer(html):
        current_date = match.group("date")
        tooltip = match.group("tip")
        contribution_match = re.search(r"(\d+) contributions?", tooltip)
        counts[current_date] = int(contribution_match.group(1)) if contribution_match else 0

    series: list[tuple[date, int]] = []
    cursor = start
    while cursor <= end:
        series.append((cursor, counts.get(cursor.isoformat(), 0)))
        cursor += timedelta(days=1)
    return series


def nice_max(value: int) -> int:
    if value <= 5:
        return 5
    magnitude = 10 ** int(math.log10(value))
    candidates = [1, 2, 5, 10]
    for step in candidates:
        ceiling = step * magnitude
        if value <= ceiling:
            return ceiling
    return 10 * magnitude


def build_line_path(points: list[tuple[float, float]]) -> str:
    commands = [f"M {points[0][0]:.2f} {points[0][1]:.2f}"]
    for x, y in points[1:]:
        commands.append(f"L {x:.2f} {y:.2f}")
    return " ".join(commands)


def build_area_path(points: list[tuple[float, float]], baseline: float) -> str:
    line = build_line_path(points)
    end_x = points[-1][0]
    start_x = points[0][0]
    return f"{line} L {end_x:.2f} {baseline:.2f} L {start_x:.2f} {baseline:.2f} Z"


def render_contribution_svg(series: list[tuple[date, int]]) -> str:
    counts = [count for _, count in series]
    total = sum(counts)
    peak = max(counts) if counts else 0
    peak_index = counts.index(peak) if counts else 0
    latest = counts[-1] if counts else 0
    latest_date = series[-1][0] if series else date.today()
    plot_left = 68
    plot_right = 1126
    plot_top = 96
    plot_bottom = 278
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    chart_max = nice_max(peak if peak > 0 else 1)

    points: list[tuple[float, float]] = []
    for index, (_, count) in enumerate(series):
        if len(series) == 1:
            x = plot_left
        else:
            x = plot_left + (plot_width * index / (len(series) - 1))
        y = plot_bottom - (count / chart_max) * plot_height
        points.append((x, y))

    area_path = build_area_path(points, plot_bottom)
    line_path = build_line_path(points)

    grid_values = [chart_max * ratio for ratio in (0.25, 0.5, 0.75)]
    grid_lines = []
    for value in grid_values:
        y = plot_bottom - (value / chart_max) * plot_height
        grid_lines.append(
            f'<path d="M {plot_left} {y:.2f} H {plot_right}" stroke="#D9E2E1" stroke-width="1" stroke-dasharray="5 8"/>'
        )

    month_labels = []
    seen_months: set[tuple[int, int]] = set()
    for index, (current_date, _) in enumerate(series):
        month_key = (current_date.year, current_date.month)
        is_first = index == 0
        month_changed = month_key not in seen_months
        if is_first or (current_date.day <= 7 and month_changed):
            x = points[index][0]
            month_labels.append(
                f'<text x="{x:.2f}" y="302" text-anchor="middle" fill="#94A3B8" font-size="13" font-weight="600" font-family="SF Pro Text, Segoe UI, Arial, sans-serif">{current_date.strftime("%b")}</text>'
            )
            seen_months.add(month_key)

    peak_x, peak_y = points[peak_index]
    latest_x, latest_y = points[-1]
    peak_date = series[peak_index][0]

    return f"""<svg width="1200" height="340" viewBox="0 0 1200 340" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="signalBg" x1="62" y1="24" x2="1138" y2="314" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FBFAF7"/>
      <stop offset="1" stop-color="#F4F7F7"/>
    </linearGradient>
    <linearGradient id="signalFill" x1="0" y1="96" x2="0" y2="278" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0F766E" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#0F766E" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="signalShadow" x="0" y="0" width="1200" height="340" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#0F172A" flood-opacity="0.05"/>
    </filter>
  </defs>

  <g filter="url(#signalShadow)">
    <rect x="22" y="18" width="1156" height="292" rx="28" fill="url(#signalBg)"/>
    <rect x="22.5" y="18.5" width="1155" height="291" rx="27.5" stroke="#E5E7EB"/>
  </g>

  <path d="M46 46H280" stroke="#D8E3E2" stroke-width="2"/>
  <path d="M942 46H1152" stroke="#E6D6BE" stroke-width="2"/>
  <rect x="46" y="42" width="8" height="8" rx="4" fill="#0F766E"/>
  <rect x="1144" y="42" width="8" height="8" rx="4" fill="#C97A1A"/>

  <text x="46" y="48" fill="#64748B" font-size="14" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif" letter-spacing="3">
    CONTRIBUTION SIGNALS
  </text>
  <text x="1032" y="48" fill="#94A3B8" font-size="13" font-weight="700" font-family="SF Pro Text, Segoe UI, Arial, sans-serif" letter-spacing="2">
    LAST {CONTRIBUTION_WINDOW_DAYS} DAYS
  </text>

  <text x="876" y="92" fill="#64748B" font-size="12" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif" letter-spacing="2">
    TOTAL
  </text>
  <text x="876" y="126" fill="#0F172A" font-size="34" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif">{total}</text>
  <text x="1010" y="92" fill="#64748B" font-size="12" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif" letter-spacing="2">
    PEAK
  </text>
  <text x="1010" y="126" fill="#0F172A" font-size="34" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif">{peak}</text>
  <text x="1090" y="126" fill="#94A3B8" font-size="13" font-weight="600" font-family="SF Pro Text, Segoe UI, Arial, sans-serif">
    {peak_date.strftime("%b %-d") if os.name != "nt" else peak_date.strftime("%b %d").replace(" 0", " ")}
  </text>

  {"".join(grid_lines)}
  <path d="{area_path}" fill="url(#signalFill)"/>
  <path d="{line_path}" stroke="#0F766E" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="{peak_x:.2f}" cy="{peak_y:.2f}" r="7.5" fill="#C97A1A"/>
  <circle cx="{peak_x:.2f}" cy="{peak_y:.2f}" r="13" stroke="#C97A1A" stroke-opacity="0.18" stroke-width="2"/>
  <circle cx="{latest_x:.2f}" cy="{latest_y:.2f}" r="6" fill="#0F766E"/>

  <text x="{latest_x:.2f}" y="78" text-anchor="middle" fill="#94A3B8" font-size="12" font-weight="700" font-family="SF Pro Text, Segoe UI, Arial, sans-serif" letter-spacing="1.4">
    TODAY {latest}
  </text>

  {"".join(month_labels)}
</svg>
"""


def render_project_pill_svg(label: str, accent: str, width: int) -> str:
    text_x = 28
    circle_x = width - 24
    line_x = text_x
    line_width = min(76, max(46, len(label) * 5))
    return f"""<svg width="{width}" height="56" viewBox="0 0 {width} 56" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="0.5" y="0.5" width="{width - 1}" height="55" rx="18" fill="#FFFFFF" fill-opacity="0.84" stroke="#E6ECEC"/>
  <rect x="{line_x}" y="16" width="{line_width}" height="3" rx="1.5" fill="{accent}"/>
  <circle cx="{circle_x}" cy="18" r="8.5" fill="{accent}" fill-opacity="0.10" stroke="{accent}" stroke-width="1.5"/>
  <text x="{text_x}" y="38" fill="#0F172A" font-size="20" font-weight="700" font-family="SF Pro Display, Segoe UI, Arial, sans-serif">{label}</text>
</svg>
"""


def write_project_assets() -> None:
    for project in PROJECTS:
        filename = project["repo"].lower().replace(".", "-") + ".svg"
        path = ASSETS_DIR / filename
        path.write_text(
            render_project_pill_svg(
                label=project["label"],
                accent=project["accent"],
                width=project["width"],
            ),
            encoding="utf-8",
        )
    (ASSETS_DIR / EXTRA_LINK["filename"]).write_text(
        render_project_pill_svg(
            label=EXTRA_LINK["label"],
            accent=EXTRA_LINK["accent"],
            width=EXTRA_LINK["width"],
        ),
        encoding="utf-8",
    )


def main() -> None:
    metrics = build_metrics()
    contribution_series = get_contribution_series()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "metrics.svg").write_text(render_metrics_svg(metrics), encoding="utf-8")
    (ASSETS_DIR / "contribution-signals.svg").write_text(
        render_contribution_svg(contribution_series),
        encoding="utf-8",
    )
    write_project_assets()
    print(
        f"Generated assets for {USERNAME}: metrics={metrics}, contribution_days={len(contribution_series)}"
    )


if __name__ == "__main__":
    main()
