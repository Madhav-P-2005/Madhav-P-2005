#!/usr/bin/env python3
"""Generate a contribution heatmap SVG from GitHub GraphQL API data."""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# GitHub's contribution color scale (dark theme)
COLORS = {
    0: "#161b22",   # no contributions
    1: "#0e4429",   # low
    2: "#006d32",   # medium-low
    3: "#26a641",   # medium-high
    4: "#39d353",   # high
}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["", "Mon", "", "Wed", "", "Fri", ""]

BG_COLOR = "#0d1117"
BORDER_COLOR = "#30363d"
TEXT_COLOR = "#8b949e"
ACCENT_COLOR = "#a78bfa"


def color_for_count(count: int) -> str:
    """Map a contribution count to a color."""
    if count == 0:
        return COLORS[0]
    elif count <= 3:
        return COLORS[1]
    elif count <= 6:
        return COLORS[2]
    elif count <= 9:
        return COLORS[3]
    else:
        return COLORS[4]


def fetch_contributions(username: str, token: str) -> dict:
    """Fetch contribution calendar data from GitHub GraphQL API."""
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                weekday
              }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"username": username}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-heatmap-generator",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"❌ GitHub API error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)

    calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return calendar


def generate_heatmap_svg(calendar: dict) -> str:
    """Render the contribution calendar as an SVG heatmap."""
    weeks = calendar["weeks"]
    total = calendar["totalContributions"]

    cell = 13       # cell size
    gap = 3         # gap between cells
    step = cell + gap
    left_pad = 45   # space for day labels
    top_pad = 50    # space for month labels + title
    right_pad = 20
    bottom_pad = 40

    num_weeks = len(weeks)
    width = left_pad + num_weeks * step + right_pad
    height = top_pad + 7 * step + bottom_pad

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    lines.append(f'  <style>')
    lines.append(f'    @keyframes fadeIn {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}')
    lines.append(f'    .hm-fade {{ animation: fadeIn 1s ease 0.3s both; }}')
    lines.append(f'  </style>')

    # Background
    lines.append(f'  <rect width="{width}" height="{height}" rx="10" fill="{BG_COLOR}"/>')
    lines.append(f'  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="none" stroke="{BORDER_COLOR}" stroke-width="1"/>')

    # Title
    lines.append(f'  <text x="{left_pad}" y="28" fill="{ACCENT_COLOR}" font-family="Consolas, \'Courier New\', monospace" font-size="14" font-weight="600">&#9632; Contribution Activity</text>')
    lines.append(f'  <text x="{width - right_pad}" y="28" fill="{TEXT_COLOR}" font-family="Consolas, \'Courier New\', monospace" font-size="12" text-anchor="end">{total} contributions in the last year</text>')

    # Day-of-week labels
    for i, label in enumerate(DAYS):
        if label:
            y = top_pad + i * step + cell - 2
            lines.append(f'  <text x="{left_pad - 8}" y="{y}" fill="{TEXT_COLOR}" font-family="Consolas, \'Courier New\', monospace" font-size="10" text-anchor="end">{label}</text>')

    # Month labels — place at the first week of each month
    month_positions = {}
    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            d = datetime.strptime(day["date"], "%Y-%m-%d")
            if d.day <= 7 and d.month not in month_positions:
                month_positions[d.month] = wi

    for month_num, wi in month_positions.items():
        x = left_pad + wi * step
        lines.append(f'  <text x="{x}" y="{top_pad - 6}" fill="{TEXT_COLOR}" font-family="Consolas, \'Courier New\', monospace" font-size="10">{MONTHS[month_num - 1]}</text>')

    # Contribution cells
    lines.append('  <g class="hm-fade">')
    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            wd = day["weekday"]
            count = day["contributionCount"]
            x = left_pad + wi * step
            y = top_pad + wd * step
            fill = color_for_count(count)
            lines.append(f'    <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}">'
                         f'<title>{day["date"]}: {count} contributions</title></rect>')
    lines.append('  </g>')

    # Legend
    legend_x = width - right_pad - 120
    legend_y = height - 22
    lines.append(f'  <text x="{legend_x - 30}" y="{legend_y + 9}" fill="{TEXT_COLOR}" font-family="Consolas, \'Courier New\', monospace" font-size="10">Less</text>')
    for i, level in enumerate(sorted(COLORS.keys())):
        lx = legend_x + i * (cell + 3)
        lines.append(f'  <rect x="{lx}" y="{legend_y}" width="{cell}" height="{cell}" rx="2" fill="{COLORS[level]}"/>')
    lines.append(f'  <text x="{legend_x + 5 * (cell + 3) + 4}" y="{legend_y + 9}" fill="{TEXT_COLOR}" font-family="Consolas, \'Courier New\', monospace" font-size="10">More</text>')

    lines.append('</svg>')
    return "\n".join(lines)


def main():
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_USERNAME", "Madhav-P-2005")

    if not token:
        print("⚠️  GITHUB_TOKEN not set — generating placeholder heatmap.", file=sys.stderr)
        # Generate a placeholder with empty data
        from datetime import date
        today = date.today()
        weeks = []
        start = today - timedelta(days=today.weekday() + 52 * 7)
        current = start
        while current <= today:
            week_days = []
            for wd in range(7):
                d = current + timedelta(days=wd)
                if d <= today:
                    week_days.append({
                        "contributionCount": 0,
                        "date": d.strftime("%Y-%m-%d"),
                        "weekday": wd,
                    })
            if week_days:
                weeks.append({"contributionDays": week_days})
            current += timedelta(days=7)
        calendar = {"totalContributions": 0, "weeks": weeks}
    else:
        calendar = fetch_contributions(username, token)

    svg = generate_heatmap_svg(calendar)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    img_dir = os.path.join(repo_root, "images")
    os.makedirs(img_dir, exist_ok=True)
    out = os.path.join(img_dir, "contrib-heatmap.svg")

    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"✅ Contribution heatmap generated: {out}")


if __name__ == "__main__":
    main()

