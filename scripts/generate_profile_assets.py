#!/usr/bin/env python3
"""Generate Dark Pixel Craft SVG assets for huanghfzhufeng (朱锋ZF) GitHub Profile."""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "pixel"

# Dark Pixel Craft Palette
BG_DARK = "#0D1117"
PANEL_BG = "#121923"
CARD_BG = "#151E2B"
BORDER = "#2B3B52"
BORDER_HI = "#445D7E"
SHADOW = "#070A0F"
TEXT_MAIN = "#F1F5F9"
TEXT_SUB = "#94A3B8"
TEXT_DIM = "#64748B"

GREEN = "#4ADE80"
GREEN_DARK = "#14532D"
AMBER = "#F59E0B"
AMBER_DARK = "#451A03"
CYAN = "#38BDF8"
CYAN_DARK = "#0C4A6E"
VIOLET = "#A78BFA"
VIOLET_DARK = "#2E1065"

MONO_FONT = "'SF Mono', 'JetBrains Mono', 'Menlo', 'Monaco', 'Consolas', monospace"
SANS_FONT = "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, sans-serif"


def pixel_matrix(
    grid: list[str],
    x0: int,
    y0: int,
    scale: int,
    palette: dict[str, str],
) -> str:
    """Render an ASCII pixel grid as crisp SVG <rect> elements."""
    rects: list[str] = []
    for row_idx, row in enumerate(grid):
        for col_idx, ch in enumerate(row):
            color = palette.get(ch)
            if not color:
                continue
            rx = x0 + col_idx * scale
            ry = y0 + row_idx * scale
            rects.append(
                f'<rect x="{rx}" y="{ry}" width="{scale}" height="{scale}" '
                f'fill="{color}" shape-rendering="crispEdges"/>'
            )
    return "\n  ".join(rects)


def pixel_frame(
    w: int,
    h: int,
    *,
    bg: str = PANEL_BG,
    border: str = BORDER,
    highlight: str = BORDER_HI,
    accent: str | None = None,
) -> str:
    """8-bit notched pixel border with crisp edges and subtle drop shadow."""
    p = 4  # pixel unit
    parts = [
        # Outer shadow offset
        f'<rect x="{p*2}" y="{p*2}" width="{w - p*2}" height="{h - p*2}" fill="{SHADOW}" shape-rendering="crispEdges"/>',
        # Main body (notched 4 corners)
        f'<rect x="{p}" y="{0}" width="{w - p*3}" height="{h - p}" fill="{border}" shape-rendering="crispEdges"/>',
        f'<rect x="{0}" y="{p}" width="{w - p}" height="{h - p*3}" fill="{border}" shape-rendering="crispEdges"/>',
        # Inner fill
        f'<rect x="{p}" y="{p}" width="{w - p*3}" height="{h - p*3}" fill="{bg}" shape-rendering="crispEdges"/>',
        # Subtle pixel grid background
        f'<rect x="{p}" y="{p}" width="{w - p*3}" height="{h - p*3}" fill="url(#pxGrid)" opacity="0.55"/>',
        # Top inner highlight
        f'<rect x="{p*2}" y="{p}" width="{w - p*5}" height="2" fill="{highlight}" opacity="0.65" shape-rendering="crispEdges"/>',
        # 4 corner pixel rivets
        f'<rect x="{p*2}" y="{p*2}" width="3" height="3" fill="{highlight}" shape-rendering="crispEdges"/>',
        f'<rect x="{w - p*3 - 3}" y="{p*2}" width="3" height="3" fill="{highlight}" shape-rendering="crispEdges"/>',
        f'<rect x="{p*2}" y="{h - p*3 - 3}" width="3" height="3" fill="{highlight}" shape-rendering="crispEdges"/>',
        f'<rect x="{w - p*3 - 3}" y="{h - p*3 - 3}" width="3" height="3" fill="{highlight}" shape-rendering="crispEdges"/>',
    ]
    if accent:
        parts.append(
            f'<rect x="{p}" y="{p}" width="4" height="{h - p*3}" fill="{accent}" shape-rendering="crispEdges"/>'
        )
    return "\n  ".join(parts)


def svg_defs() -> str:
    return """<defs>
    <pattern id="pxGrid" width="16" height="16" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="1" height="1" fill="#334155" opacity="0.5"/>
      <line x1="0" y1="8" x2="16" y2="8" stroke="#000000" stroke-opacity="0.16" stroke-width="1"/>
    </pattern>
  </defs>"""


def pixel_badge(x: int, y: int, text: str, fg: str, bg: str, border: str, width: int) -> str:
    return "\n  ".join(
        [
            f'<rect x="{x}" y="{y}" width="{width}" height="24" fill="{border}" shape-rendering="crispEdges"/>',
            f'<rect x="{x+2}" y="{y+2}" width="{width-4}" height="20" fill="{bg}" shape-rendering="crispEdges"/>',
            f'<rect x="{x+7}" y="{y+9}" width="5" height="5" fill="{fg}" shape-rendering="crispEdges"/>',
            f'<text x="{x+18}" y="{y+16}" fill="{fg}" font-family="{MONO_FONT}" font-size="11" font-weight="700" letter-spacing="0.8">{escape(text)}</text>',
        ]
    )


def render_hero() -> str:
    w, h = 896, 248

    # 8-bit pixel "ZF" monogram (11x7 grid)
    zf_grid = [
        "11111.22222",
        "...1..2....",
        "..1...2222.",
        ".1....2....",
        "1.....2....",
        "11111.2....",
    ]
    zf_logo = pixel_matrix(
        zf_grid,
        x0=42,
        y0=68,
        scale=6,
        palette={"1": GREEN, "2": AMBER},
    )

    # 8-bit pixel workbench illustration (CRT monitor + code + coffee + sparks)
    workstation_grid = [
        "..............y.......",
        ".............yyy......",
        "....bbbbbbbbbb.y......",
        "...bddddddddddbb......",
        "...bdggggg..ddbb......",
        "...bdg..ccc.ddbb...w..",
        "...bdg.gggg.ddbb..w...",
        "...bdg..yy..ddbb......",
        "...bdg.g....ddbb.rrrr.",
        "...bddddddddddbb.rwwrr",
        "....bbbbbbbbbb...rwwr.",
        ".......bbbb......rrrr.",
        ".....bbbbbbbb.........",
        "..ssssssssssssss......",
        ".sggggggggggggggs.....",
        "..ssssssssssssss......",
    ]
    workstation = pixel_matrix(
        workstation_grid,
        x0=676,
        y0=58,
        scale=8,
        palette={
            "b": "#334155",
            "d": "#090E14",
            "g": GREEN,
            "c": CYAN,
            "y": AMBER,
            "s": "#475569",
            "r": "#D97706",
            "w": "#CBD5E1",
        },
    )

    badges = "\n  ".join(
        [
            pixel_badge(42, 188, "AI AGENTS", GREEN, "#0E241A", "#1E4D36", 112),
            pixel_badge(166, 188, "SYSTEMS LAB", CYAN, "#0C2132", "#1B4666", 128),
            pixel_badge(306, 188, "WORKFLOWS", AMBER, "#291B07", "#5E3D0D", 116),
            pixel_badge(434, 188, "CONTENT CREATOR", VIOLET, "#1E1636", "#423175", 142),
        ]
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  {svg_defs()}
  {pixel_frame(w, h, bg=PANEL_BG)}

  <!-- Top terminal status bar -->
  <rect x="4" y="4" width="{w-12}" height="32" fill="#0C121A" shape-rendering="crispEdges"/>
  <rect x="4" y="36" width="{w-12}" height="2" fill="{BORDER}" shape-rendering="crispEdges"/>
  <rect x="20" y="16" width="8" height="8" fill="{GREEN}" shape-rendering="crispEdges"/>
  <rect x="34" y="16" width="8" height="8" fill="{AMBER}" shape-rendering="crispEdges"/>
  <rect x="48" y="16" width="8" height="8" fill="{CYAN}" shape-rendering="crispEdges"/>
  <text x="72" y="24" fill="{TEXT_SUB}" font-family="{MONO_FONT}" font-size="12" font-weight="600" letter-spacing="1.2">SYS://ZHUFENG.ZF</text>
  <rect x="698" y="17" width="7" height="7" fill="{GREEN}" shape-rendering="crispEdges"/>
  <text x="712" y="24" fill="{GREEN}" font-family="{MONO_FONT}" font-size="11" font-weight="700" letter-spacing="1">ONLINE · BUILDER MODE</text>

  <!-- Pixel ZF monogram -->
  <rect x="34" y="60" width="82" height="52" fill="#0B1017" stroke="{BORDER}" stroke-width="2" shape-rendering="crispEdges"/>
  {zf_logo}

  <!-- Main identity -->
  <text x="134" y="92" fill="{TEXT_MAIN}" font-family="{SANS_FONT}" font-size="34" font-weight="800" letter-spacing="1">朱锋ZF</text>
  <text x="136" y="114" fill="{AMBER}" font-family="{MONO_FONT}" font-size="12" font-weight="700" letter-spacing="1.8">INDEPENDENT BUILDER · AI-NATIVE &amp; AGENT SYSTEMS</text>

  <!-- Manifesto -->
  <text x="42" y="146" fill="{TEXT_MAIN}" font-family="{MONO_FONT}" font-size="14" font-weight="600">&gt; Build to understand.</text>
  <text x="42" y="170" fill="{TEXT_SUB}" font-family="{SANS_FONT}" font-size="13.5" font-weight="500">亲手构造吃透底层机制，用确定性脚本守住交付质量。</text>

  <!-- Status badges -->
  {badges}

  <!-- Right pixel workstation -->
  <rect x="654" y="50" width="212" height="176" fill="#0B1017" stroke="#223044" stroke-width="2" shape-rendering="crispEdges"/>
  {workstation}
  <text x="676" y="210" fill="{TEXT_DIM}" font-family="{MONO_FONT}" font-size="10" letter-spacing="1.2">LV.23 · CRAFTING SYSTEMS</text>
</svg>
"""


def render_section_header(title: str, subtitle: str, accent: str) -> str:
    w, h = 896, 48
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  {svg_defs()}
  {pixel_frame(w, h, bg=PANEL_BG, accent=accent)}
  <rect x="22" y="18" width="10" height="10" fill="{accent}" shape-rendering="crispEdges"/>
  <rect x="36" y="20" width="6" height="6" fill="{BORDER_HI}" shape-rendering="crispEdges"/>
  <text x="52" y="28" fill="{TEXT_MAIN}" font-family="{MONO_FONT}" font-size="14" font-weight="800" letter-spacing="1.6">{escape(title)}</text>
  <text x="242" y="28" fill="{TEXT_SUB}" font-family="{SANS_FONT}" font-size="12.5" font-weight="500">{escape(subtitle)}</text>
  <text x="794" y="28" fill="{accent}" font-family="{MONO_FONT}" font-size="11" font-weight="700" letter-spacing="1">06 / FEATURED</text>
</svg>
"""


ICONS: dict[str, list[str]] = {
    "chip": [
        "..a..a..",
        ".bbbbbb.",
        "abccccba",
        ".bcyycb.",
        ".bcyycb.",
        "abccccba",
        ".bbbbbb.",
        "..a..a..",
    ],
    "slides": [
        "bbbbbbbb",
        "bccccccb",
        "bcyaaacb",
        "bcyccccb",
        "bccccccb",
        "bbbbbbbb",
        "...bb...",
        "..b..b..",
    ],
    "radar": [
        "..bbbb..",
        ".bccccb.",
        "bc..y.cb",
        "bc.y..cb",
        "bc..y.cb",
        "bc....cb",
        ".bccccb.",
        "..bbbb..",
    ],
    "doc": [
        ".bbbbbb.",
        ".bccccb.",
        ".bcyycb.",
        ".bccccb.",
        ".bcyyyb.",
        ".bccccb.",
        ".bcyycb.",
        ".bbbbbb.",
    ],
    "phone": [
        "..bbbb..",
        ".bccccb.",
        ".bcyycb.",
        ".bccccb.",
        ".bccccb.",
        ".bccccb.",
        ".bc..cb.",
        "..bbbb..",
    ],
    "gear": [
        "...bb...",
        ".b.bb.b.",
        "..bbbb..",
        "bbbyybbb",
        "bbbyybbb",
        "..bbbb..",
        ".b.bb.b.",
        "...bb...",
    ],
}


def render_project_card(
    *,
    name: str,
    line1: str,
    line2: str,
    tag: str,
    accent: str,
    accent_bg: str,
    icon_key: str,
) -> str:
    w, h = 440, 146
    icon = pixel_matrix(
        ICONS[icon_key],
        x0=24,
        y0=24,
        scale=4,
        palette={
            "a": BORDER_HI,
            "b": "#64748B",
            "c": "#0F172A",
            "y": accent,
        },
    )
    tag_w = max(92, len(tag) * 8 + 24)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  {svg_defs()}
  {pixel_frame(w, h, bg=CARD_BG, accent=accent)}

  <!-- Icon frame -->
  <rect x="18" y="18" width="44" height="44" fill="#0B1017" stroke="{BORDER}" stroke-width="2" shape-rendering="crispEdges"/>
  {icon}

  <!-- Title -->
  <text x="76" y="38" fill="{TEXT_MAIN}" font-family="{MONO_FONT}" font-size="16" font-weight="800">{escape(name)}</text>
  <rect x="76" y="46" width="48" height="3" fill="{accent}" shape-rendering="crispEdges"/>

  <!-- Description (2 crisp lines, generous spacing) -->
  <text x="22" y="84" fill="{TEXT_SUB}" font-family="{SANS_FONT}" font-size="12.5" font-weight="500">{escape(line1)}</text>
  <text x="22" y="103" fill="{TEXT_SUB}" font-family="{SANS_FONT}" font-size="12.5" font-weight="500">{escape(line2)}</text>

  <!-- Footer tag & pixel arrow -->
  <rect x="22" y="114" width="{tag_w}" height="18" fill="{accent_bg}" stroke="{accent}" stroke-width="1" shape-rendering="crispEdges"/>
  <text x="32" y="127" fill="{accent}" font-family="{MONO_FONT}" font-size="10.5" font-weight="700" letter-spacing="0.8">{escape(tag)}</text>
  <text x="382" y="127" fill="{accent}" font-family="{MONO_FONT}" font-size="12" font-weight="700">OPEN &gt;</text>
</svg>
"""


def render_protocol() -> str:
    w, h = 896, 224
    pillars = [
        ("01", "BUILD TO UNDERSTAND", GREEN, "不停在收藏与调 API", "在低复杂度里亲手重建机制才算真懂"),
        ("02", "DETERMINISTIC GATES", AMBER, "原则归原则，机械归脚本", "能用自动化脚本验收的绝不靠感觉"),
        ("03", "END-TO-END SHIPPING", CYAN, "事实、原型、验证闭环", "坚持单主线推进，把想法真正交付上线"),
    ]
    cols: list[str] = []
    col_w = 268
    for idx, (num, title, color, l1, l2) in enumerate(pillars):
        cx = 24 + idx * (col_w + 18)
        cy = 50
        cols.append(
            f"""
  <rect x="{cx}" y="{cy}" width="{col_w}" height="106" fill="#0B1017" stroke="{BORDER}" stroke-width="2" shape-rendering="crispEdges"/>
  <rect x="{cx}" y="{cy}" width="{col_w}" height="4" fill="{color}" shape-rendering="crispEdges"/>
  <text x="{cx+14}" y="{cy+28}" fill="{color}" font-family="{MONO_FONT}" font-size="12" font-weight="800" letter-spacing="1">{num} // {escape(title)}</text>
  <text x="{cx+14}" y="{cy+58}" fill="{TEXT_MAIN}" font-family="{SANS_FONT}" font-size="12.5" font-weight="600">{escape(l1)}</text>
  <text x="{cx+14}" y="{cy+80}" fill="{TEXT_SUB}" font-family="{SANS_FONT}" font-size="12" font-weight="500">{escape(l2)}</text>"""
        )

    stack = [
        ("PYTHON", GREEN),
        ("TYPESCRIPT", CYAN),
        ("REACT", CYAN),
        ("LANGGRAPH", AMBER),
        ("AGENT HARNESS", GREEN),
        ("SQLITE", VIOLET),
        ("FFMPEG", AMBER),
    ]
    pills: list[str] = []
    px = 114
    for label, color in stack:
        pw = len(label) * 8 + 20
        pills.append(
            f'<rect x="{px}" y="174" width="{pw}" height="24" fill="#0B1017" stroke="{BORDER_HI}" stroke-width="1.5" shape-rendering="crispEdges"/>'
            f'<rect x="{px+6}" y="183" width="5" height="5" fill="{color}" shape-rendering="crispEdges"/>'
            f'<text x="{px+16}" y="190" fill="{TEXT_MAIN}" font-family="{MONO_FONT}" font-size="11" font-weight="700">{label}</text>'
        )
        px += pw + 10

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  {svg_defs()}
  {pixel_frame(w, h, bg=PANEL_BG)}

  <rect x="24" y="20" width="8" height="8" fill="{AMBER}" shape-rendering="crispEdges"/>
  <text x="40" y="29" fill="{TEXT_MAIN}" font-family="{MONO_FONT}" font-size="13" font-weight="800" letter-spacing="1.4">BUILDER PROTOCOL &amp; LOADOUT</text>
  <text x="708" y="29" fill="{TEXT_DIM}" font-family="{MONO_FONT}" font-size="11" letter-spacing="1">VERIFIED BY SCRIPTS</text>

  {"".join(cols)}

  <text x="24" y="190" fill="{TEXT_SUB}" font-family="{MONO_FONT}" font-size="11.5" font-weight="700" letter-spacing="1">LOADOUT:</text>
  {"".join(pills)}
</svg>
"""


def render_all_repos_button() -> str:
    w, h = 448, 52
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
  {svg_defs()}
  {pixel_frame(w, h, bg="#13221A", border="#22543D", highlight=GREEN)}
  <rect x="28" y="19" width="8" height="10" fill="{GREEN}" shape-rendering="crispEdges"/>
  <text x="48" y="29" fill="{TEXT_MAIN}" font-family="{MONO_FONT}" font-size="13" font-weight="800" letter-spacing="1">EXPLORE ALL REPOSITORIES · 查看全部项目</text>
</svg>
"""


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    # Remove obsolete zero-stat assets
    for old in ("header.svg", "metrics.svg", "contribution-signals.svg", "csccc.svg"):
        old_path = ASSETS / old
        if old_path.exists():
            old_path.unlink()

    (ASSETS / "hero.svg").write_text(render_hero(), encoding="utf-8")
    (ASSETS / "section-work.svg").write_text(
        render_section_header("SELECTED WORK", "精选公开作品 · 点击卡片直达仓库", GREEN),
        encoding="utf-8",
    )
    (ASSETS / "protocol.svg").write_text(render_protocol(), encoding="utf-8")
    (ASSETS / "all-repositories.svg").write_text(render_all_repos_button(), encoding="utf-8")

    projects = [
        (
            "build-to-understand.svg",
            "build-to-understand",
            "通过从零构造最小可运行系统吃透底层机制",
            "涵盖 mini-agent、mini-object-store 等系统实验",
            "PYTHON · SYSTEMS",
            CYAN,
            CYAN_DARK,
            "chip",
        ),
        (
            "organicslides.svg",
            "OrganicSlides",
            "基于 LangGraph 多智能体的 AI 演示文稿引擎",
            "自动完成研究、策划、撰写、设计与 PPT 渲染",
            "PYTHON · LANGGRAPH",
            AMBER,
            AMBER_DARK,
            "slides",
        ),
        (
            "geo-insight.svg",
            "GEO-Insight",
            "国产大模型品牌可见性与推荐排名监测工具",
            "覆盖 DeepSeek、Kimi、豆包、通义千问等主流模型",
            "JS · GEO RADAR",
            GREEN,
            GREEN_DARK,
            "radar",
        ),
        (
            "aigc-deslop.svg",
            "aigc-deslop",
            "中文论文 AIGC 降重方法论 + Word 保格式工具",
            "真实论文实测检测率由 55% 降至 11%",
            "PYTHON · NLP",
            VIOLET,
            VIOLET_DARK,
            "doc",
        ),
        (
            "app-mockup-studio.svg",
            "App-Mockup-Studio",
            "SnapShell 在线截图带壳展示图生成工具",
            "上传截图一键生成应用商店、官网与社媒配图",
            "JS · WEB TOOL",
            CYAN,
            CYAN_DARK,
            "phone",
        ),
        (
            "softright-ai.svg",
            "SoftRight-AI",
            "面向开发者与企业的软著申请智能体系统",
            "自动化完成软件著作权文档撰写与源码整理",
            "TS · AI AGENT",
            AMBER,
            AMBER_DARK,
            "gear",
        ),
    ]
    for filename, name, l1, l2, tag, accent, accent_bg, icon_key in projects:
        (ASSETS / filename).write_text(
            render_project_card(
                name=name,
                line1=l1,
                line2=l2,
                tag=tag,
                accent=accent,
                accent_bg=accent_bg,
                icon_key=icon_key,
            ),
            encoding="utf-8",
        )
    print(f"Generated {len(list(ASSETS.glob('*.svg')))} dark pixel SVG assets in {ASSETS}")


if __name__ == "__main__":
    main()
