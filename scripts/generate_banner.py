#!/usr/bin/env python3
"""Generate a stylized, high-impact hero banner SVG for Madhav P."""

import os


def generate_banner():
    """Create a stylized name banner with prominent Linux/terminal Software Engineer role."""
    bg = "#070a12"
    card_bg = "#0c101d"
    border = "#1e293b"
    accent_violet = "#a78bfa"
    accent_purple = "#818cf8"
    accent_cyan = "#38bdf8"
    emerald = "#10b981"
    text_muted = "#64748b"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="220" viewBox="0 0 900 220">
  <defs>
    <!-- Background Radial Atmosphere -->
    <radialGradient id="meshGlow" cx="20%" cy="30%" r="80%">
      <stop offset="0%" style="stop-color:#312e81;stop-opacity:0.45"/>
      <stop offset="50%" style="stop-color:#0f172a;stop-opacity:0.6"/>
      <stop offset="100%" style="stop-color:{bg};stop-opacity:1"/>
    </radialGradient>

    <!-- Stylized Dual-Tone Gradient for Name -->
    <linearGradient id="stylizedName" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#ffffff"/>
      <stop offset="40%" style="stop-color:#e0e7ff"/>
      <stop offset="75%" style="stop-color:{accent_violet}"/>
      <stop offset="100%" style="stop-color:{accent_cyan}"/>
    </linearGradient>

    <!-- Role Badge Background Gradient -->
    <linearGradient id="badgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1e1b4b;stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:#0f172a;stop-opacity:0.4"/>
    </linearGradient>

    <!-- Luminous Drop Shadow Filter -->
    <filter id="nameGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="{accent_purple}" flood-opacity="0.35"/>
    </filter>

    <filter id="cursorGlow">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="{accent_cyan}" flood-opacity="0.8"/>
    </filter>

    <!-- Subtle Tech Grid -->
    <pattern id="dotGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.75" fill="#334155" opacity="0.4"/>
    </pattern>
  </defs>

  <style>
    @keyframes fadeIn {{ 0% {{ opacity: 0; transform: translateY(4px); }} 100% {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @keyframes beaconPulse {{ 0%, 100% {{ opacity: 0.4; r: 4; }} 50% {{ opacity: 1; r: 5.5; }} }}
    
    .f-name {{ animation: fadeIn 0.4s ease-out 0.1s both; }}
    .f-role {{ animation: fadeIn 0.5s ease-out 0.3s both; }}
    .f-bar  {{ animation: fadeIn 0.4s ease-out both; }}
    
    .cursor {{ animation: blink 1.05s step-end infinite; }}
    .beacon {{ animation: beaconPulse 2s ease-in-out infinite; }}
  </style>

  <!-- Base Canvas -->
  <rect width="900" height="220" rx="16" fill="url(#meshGlow)"/>
  <rect width="900" height="220" rx="16" fill="url(#dotGrid)"/>
  <rect x="0.5" y="0.5" width="899" height="219" rx="16" fill="none" stroke="{border}" stroke-width="1.2"/>

  <!-- Top Terminal Bar -->
  <g class="f-bar">
    <rect x="1" y="1" width="898" height="36" rx="16" fill="{card_bg}" opacity="0.85"/>
    <rect x="1" y="22" width="898" height="15" fill="{card_bg}" opacity="0.85"/>
    <line x1="0" y1="37" x2="900" y2="37" stroke="{border}" stroke-width="0.8"/>

    <!-- Mac/Linux Terminal Dots -->
    <circle cx="28" cy="19" r="4.5" fill="#f43f5e" opacity="0.85"/>
    <circle cx="44" cy="19" r="4.5" fill="#fbbf24" opacity="0.85"/>
    <circle cx="60" cy="19" r="4.5" fill="{emerald}" opacity="0.85"/>

    <!-- Terminal Breadcrumb -->
    <text x="84" y="23" fill="{text_muted}" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="500">
      terminal ~ <tspan fill="{accent_cyan}">madhav@archlinux</tspan>:<tspan fill="{accent_violet}">/workspace</tspan>
    </text>

    <!-- Top Right Status -->
    <circle cx="830" cy="19" r="4" fill="{emerald}" class="beacon"/>
    <text x="842" y="23" fill="{emerald}" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="700" letter-spacing="0.5">
      ONLINE
    </text>
  </g>

  <!-- ==================== MAIN SECTION ==================== -->

  <!-- 1. STYLIZED NAME -->
  <g class="f-name">
    <!-- Ambient Accent Line above name -->
    <line x1="50" y1="62" x2="110" y2="62" stroke="{accent_cyan}" stroke-width="2" stroke-linecap="round"/>
    
    <!-- Stylized Modern Name with Luminous Sheen -->
    <text x="50" y="112" fill="url(#stylizedName)" filter="url(#nameGlow)" font-family="system-ui, -apple-system, 'SF Pro Display', 'Inter', 'Segoe UI', sans-serif" font-size="48" font-weight="900" letter-spacing="-1.2">
      MADHAV P
    </text>
  </g>

  <!-- 2. PROMINENT LINUX / TERMINAL ROLE -->
  <g class="f-role">
    <!-- Role Container Pill / Terminal Box -->
    <rect x="50" y="132" width="480" height="42" rx="8" fill="url(#badgeGrad)" stroke="{accent_violet}" stroke-width="1.2" stroke-opacity="0.6"/>

    <!-- Terminal Prompt Symbol & Role Text -->
    <text x="68" y="159" font-family="'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace" font-size="19" font-weight="800" letter-spacing="1">
      <tspan fill="{accent_cyan}">❯ </tspan>
      <tspan fill="#ffffff">SOFTWARE ENGINEER</tspan>
    </text>

    <!-- Terminal Blinking Block Cursor -->
    <rect x="330" y="143" width="9" height="20" rx="1.5" fill="{accent_cyan}" filter="url(#cursorGlow)" class="cursor"/>

    <!-- Terminal Sub-badge / Spec Indicator -->
    <rect x="360" y="142" width="154" height="22" rx="4" fill="#0f172a" stroke="{border}" stroke-width="0.8"/>
    <text x="437" y="157" fill="{text_muted}" font-family="'JetBrains Mono', Consolas, monospace" font-size="10.5" font-weight="600" text-anchor="middle" letter-spacing="0.5">
      SYSTEMS &amp; DATA
    </text>
  </g>

  <!-- Bottom System Spec Footer (Clean & Minimal) -->
  <line x1="50" y1="194" x2="850" y2="194" stroke="{border}" stroke-width="0.6" opacity="0.6"/>
  
  <text x="50" y="209" fill="{text_muted}" font-family="'JetBrains Mono', Consolas, monospace" font-size="10.5">
    <tspan fill="{accent_cyan}">env</tspan>: production &#183; <tspan fill="{accent_violet}">arch</tspan>: distributed &#183; <tspan fill="{emerald}">status</tspan>: active
  </text>

  <text x="850" y="209" fill="{text_muted}" font-family="'JetBrains Mono', Consolas, monospace" font-size="10.5" text-anchor="end">
    [ready to ship]
  </text>
</svg>'''
    return svg


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    img_dir = os.path.join(repo_root, "images")
    os.makedirs(img_dir, exist_ok=True)
    out = os.path.join(img_dir, "hero_banner.svg")

    with open(out, "w", encoding="utf-8") as f:
        f.write(generate_banner())

    print(f"✅ Stylized Hero Banner generated: {out}")
