#!/usr/bin/env python3
"""Build the OpenWALDO Markdown book as multi-page HTML or one PDF."""

from __future__ import annotations

import argparse
import html
import math
import re
import shutil
import textwrap
from collections import OrderedDict, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
SUMMARY = SOURCE / "SUMMARY.md"
OUTPUT = ROOT / "output"
LINK = re.compile(r"\[([^]]+)\]\(([^)]+)\)")
FENCE = re.compile(r"^```([^ ]*)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.+)$")


@dataclass
class DiagramNode:
    identity: str
    label: str
    start: bool = False


@dataclass
class DiagramEdge:
    source: str
    target: str
    label: str = ""
    dotted: bool = False


def parse_mermaid(source: str) -> tuple[str, list[DiagramNode], list[DiagramEdge]]:
    """Parse the deliberately small flowchart/state subset used by this book."""
    nodes: OrderedDict[str, DiagramNode] = OrderedDict()
    edges: list[DiagramEdge] = []
    lines = [line.strip() for line in source.splitlines() if line.strip()]
    direction = "TB"
    if lines and lines[0].startswith("flowchart"):
        direction = lines.pop(0).split(maxsplit=1)[1]
    elif lines and lines[0].startswith("stateDiagram"):
        lines.pop(0)

    def remember(identity: str, label: str | None = None) -> str:
        key = "START" if identity == "[*]" else identity
        clean = (label or identity).replace(r"\n", "\n")
        if key not in nodes:
            nodes[key] = DiagramNode(key, "" if identity == "[*]" else clean, identity == "[*]")
        elif label:
            nodes[key].label = clean
        return key

    endpoint = r'(\[\*\]|[A-Za-z][A-Za-z0-9_]*)(?:\["((?:[^"\\]|\\.)*)"\])?'
    edge_pattern = re.compile(endpoint + r'\s*(-->|-\.\s*(?:"([^"]*)")?\s*\.->)\s*' + endpoint + r'(?:\s*:\s*(.+))?$')
    node_pattern = re.compile(endpoint + r"$")
    for line in lines:
        if line.startswith(("subgraph ", "classDef ", "class ")) or line == "end":
            continue
        match = edge_pattern.match(line)
        if match:
            source_id, source_label, operator, edge_label, target_id, target_label, state_label = match.groups()
            source_key = remember(source_id, source_label)
            target_key = remember(target_id, target_label)
            edges.append(DiagramEdge(source_key, target_key, edge_label or state_label or "", operator.startswith("-.")))
            continue
        match = node_pattern.match(line)
        if match:
            remember(match.group(1), match.group(2))
    return direction, list(nodes.values()), edges


def diagram_label_lines(label: str, node_width: float) -> list[str]:
    width = max(10, int(node_width / 5.2))
    lines: list[str] = []
    for explicit in label.splitlines() or [label]:
        lines.extend(textwrap.wrap(explicit, width=width, break_long_words=False) or [""])
    return lines


def diagram_layout(source: str, width: float) -> tuple[list[DiagramNode], list[DiagramEdge], dict[str, tuple[float, float]], float, float, float, str]:
    direction, nodes, edges = parse_mermaid(source)
    identities = [node.identity for node in nodes]
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree = {identity: 0 for identity in identities}
    for edge in edges:
        outgoing[edge.source].append(edge.target)
        indegree[edge.target] += 1

    layer = {identity: 0 for identity in identities}
    queue = deque(identity for identity in identities if indegree[identity] == 0)
    visited: set[str] = set()
    while queue:
        current = queue.popleft()
        visited.add(current)
        for target in outgoing[current]:
            layer[target] = max(layer[target], layer[current] + 1)
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)

    # State diagrams contain an intentional retry edge. Place the remaining
    # cycle in declaration order while preserving already resolved layers.
    for identity in identities:
        if identity not in visited:
            parents = [edge.source for edge in edges if edge.target == identity and edge.source in visited]
            layer[identity] = max((layer[parent] + 1 for parent in parents), default=max(layer.values(), default=0) + 1)
            visited.add(identity)

    groups: dict[int, list[str]] = defaultdict(list)
    for identity in identities:
        groups[layer[identity]].append(identity)
    max_layer = max(groups, default=0)
    max_group = max((len(group) for group in groups.values()), default=1)
    node_width = min(150.0, max(88.0, (width - 40.0) / max(1, max_group) - 18.0)) if direction == "TB" else min(145.0, max(72.0, (width - 40.0) / max(1, max_layer + 1) - 18.0))
    max_label_lines = max((len(diagram_label_lines(node.label, node_width)) for node in nodes if not node.start), default=1)
    node_height = max(48.0, max_label_lines * 15.0 + 16.0)
    if direction == "LR":
        height = max(120.0, max_group * 78.0 + 30.0)
        x_gap = (width - node_width - 20.0) / max(1, max_layer)
        positions = {}
        for level, group in groups.items():
            for index, identity in enumerate(group):
                y_gap = height / (len(group) + 1)
                positions[identity] = (10.0 + node_width / 2 + level * x_gap, (index + 1) * y_gap)
    else:
        height = max(160.0, (max_layer + 1) * 78.0 + 22.0)
        y_gap = (height - node_height - 20.0) / max(1, max_layer)
        positions = {}
        for level, group in groups.items():
            for index, identity in enumerate(group):
                x_gap = width / (len(group) + 1)
                positions[identity] = ((index + 1) * x_gap, 10.0 + node_height / 2 + level * y_gap)
    return nodes, edges, positions, node_width, node_height, height, direction


def edge_points(source: tuple[float, float], target: tuple[float, float], node_width: float, node_height: float) -> tuple[float, float, float, float]:
    dx, dy = target[0] - source[0], target[1] - source[1]
    distance = math.hypot(dx, dy) or 1.0
    ux, uy = dx / distance, dy / distance
    start_offset = min(node_width / (2 * max(abs(ux), .001)), node_height / (2 * max(abs(uy), .001)))
    end_offset = start_offset
    return source[0] + ux * start_offset, source[1] + uy * start_offset, target[0] - ux * end_offset, target[1] - uy * end_offset


def mermaid_svg(source: str) -> str:
    width = 900.0
    nodes, edges, positions, node_width, node_height, height, _ = diagram_layout(source, width)
    pieces = [f'<svg class="diagram" role="img" viewBox="0 0 {width:.0f} {height:.0f}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#126e82"/></marker></defs>']
    for edge in edges:
        x1, y1, x2, y2 = edge_points(positions[edge.source], positions[edge.target], node_width, node_height)
        dash = ' stroke-dasharray="7 5"' if edge.dotted else ""
        pieces.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#126e82" stroke-width="2" marker-end="url(#arrow)"{dash}/>')
        if edge.label:
            pieces.append(f'<text x="{(x1+x2)/2:.1f}" y="{(y1+y2)/2-7:.1f}" text-anchor="middle" class="edge-label">{html.escape(edge.label)}</text>')
    for node in nodes:
        x, y = positions[node.identity]
        if node.start:
            pieces.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#126e82"/>')
            continue
        pieces.append(f'<rect x="{x-node_width/2:.1f}" y="{y-node_height/2:.1f}" width="{node_width:.1f}" height="{node_height:.1f}" rx="8" fill="#f4f7f8" stroke="#126e82" stroke-width="2"/>')
        labels = diagram_label_lines(node.label, node_width) or [node.identity]
        baseline = y - (len(labels) - 1) * 8
        for offset, label in enumerate(labels):
            pieces.append(f'<text x="{x:.1f}" y="{baseline + offset*16:.1f}" text-anchor="middle" dominant-baseline="middle">{html.escape(label)}</text>')
    pieces.append("</svg>")
    return "".join(pieces)


def chapters() -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    for label, target in LINK.findall(SUMMARY.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#")):
            continue
        path = (SUMMARY.parent / target.split("#", 1)[0]).resolve()
        if path.suffix == ".md" and path != SUMMARY.resolve():
            result.append((label, path))
    return result


def rewrite_target(target: str) -> str:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return target
    base, marker, anchor = target.partition("#")
    if base.endswith(".md"):
        base = base[:-3] + ".html"
    return base + (marker + anchor if marker else "")


def inline(value: str) -> str:
    placeholders: list[str] = []

    def hold_code(match: re.Match[str]) -> str:
        placeholders.append("<code>" + html.escape(match.group(1)) + "</code>")
        return f"\x00{len(placeholders) - 1}\x00"

    value = re.sub(r"`([^`]+)`", hold_code, value)
    value = html.escape(value, quote=False)
    value = LINK.sub(
        lambda m: f'<a href="{html.escape(rewrite_target(m.group(2)), quote=True)}">{m.group(1)}</a>',
        value,
    )
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    for index, replacement in enumerate(placeholders):
        value = value.replace(f"\x00{index}\x00", replacement)
    return value


def markdown_html(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + inline(" ".join(part.strip() for part in paragraph)) + "</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    while index < len(lines):
        line = lines[index]
        fence = FENCE.match(line)
        if fence:
            flush_paragraph()
            close_list()
            language = fence.group(1)
            block: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                block.append(lines[index])
                index += 1
            content = html.escape("\n".join(block))
            if language == "mermaid":
                out.append(mermaid_svg("\n".join(block)))
            else:
                out.append(f'<pre><code class="language-{html.escape(language)}">{content}</code></pre>')
            index += 1
            continue
        heading = HEADING.match(line)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            title = heading.group(2)
            slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"`", "", title).lower()).strip("-")
            out.append(f'<h{level} id="{slug}">{inline(title)}</h{level}>')
            index += 1
            continue
        if index + 1 < len(lines) and "|" in line and re.match(r"^\s*\|?\s*:?-+", lines[index + 1]):
            flush_paragraph()
            close_list()
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows: list[list[str]] = []
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(cell)}</th>" for cell in headers) + "</tr></thead><tbody>")
            for row in rows:
                out.append("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>")
            out.append("</tbody></table>")
            continue
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        numbered = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if bullet or numbered:
            flush_paragraph()
            wanted = "ul" if bullet else "ol"
            if list_type != wanted:
                close_list()
                list_type = wanted
                out.append(f"<{wanted}>")
            out.append("<li>" + inline((bullet or numbered).group(1)) + "</li>")
            index += 1
            continue
        if line.startswith("> "):
            flush_paragraph()
            close_list()
            quote = [line[2:]]
            index += 1
            while index < len(lines) and lines[index].startswith("> "):
                quote.append(lines[index][2:])
                index += 1
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            continue
        if not line.strip():
            flush_paragraph()
            close_list()
        else:
            paragraph.append(line)
        index += 1
    flush_paragraph()
    close_list()
    return "\n".join(out)


CSS = """
:root{--ink:#18212a;--muted:#5c6975;--line:#dce3e8;--accent:#126e82;--paper:#fff;--wash:#f4f7f8}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--paper);font:16px/1.65 system-ui,-apple-system,sans-serif}
.layout{display:grid;grid-template-columns:300px minmax(0,920px);gap:48px;max-width:1320px;margin:auto;padding:0 28px}
nav{position:sticky;top:0;height:100vh;overflow:auto;padding:28px 20px 40px 0;border-right:1px solid var(--line)}
nav strong{display:block;font-size:18px;margin-bottom:18px}nav a{display:block;color:var(--muted);text-decoration:none;padding:4px 0}
nav a.active,nav a:hover{color:var(--accent)}main{min-width:0;padding:44px 0 72px}h1{font-size:2.7rem;line-height:1.1;margin:0 0 28px}
h2{font-size:1.7rem;margin-top:2.3em;border-bottom:1px solid var(--line);padding-bottom:.25em}h3{font-size:1.25rem;margin-top:1.8em}
a{color:var(--accent)}code{background:var(--wash);padding:.12em .35em;border-radius:4px}pre{overflow:auto;background:#14212a;color:#ecf4f6;padding:18px;border-radius:8px;line-height:1.45}
pre code{background:none;padding:0}.diagram{display:block;width:100%;height:auto;margin:24px 0;background:#fff}.diagram text{font:14px system-ui,-apple-system,sans-serif;fill:var(--ink)}.diagram .edge-label{font-size:12px;paint-order:stroke;stroke:#fff;stroke-width:5px;stroke-linejoin:round}table{border-collapse:collapse;width:100%;font-size:.93rem}th,td{text-align:left;vertical-align:top;border:1px solid var(--line);padding:9px 11px}th{background:var(--wash)}
blockquote{border-left:4px solid var(--accent);margin-left:0;padding-left:18px;color:var(--muted)}.pager{display:flex;justify-content:space-between;border-top:1px solid var(--line);margin-top:54px;padding-top:20px}
@media(max-width:800px){.layout{display:block;padding:0 20px}nav{position:static;height:auto;border:0;border-bottom:1px solid var(--line)}main{padding-top:28px}}
@media print{nav,.pager{display:none}.layout{display:block;max-width:none}main{padding:0}a{color:inherit}}
"""


def build_html() -> Path:
    destination = OUTPUT / "html"
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    pages = chapters()
    navigation = "".join(
        f'<a href="{path.relative_to(SOURCE).with_suffix(".html").as_posix()}">{html.escape(title)}</a>'
        for title, path in pages
    )
    for position, (title, path) in enumerate(pages):
        relative = path.relative_to(SOURCE).with_suffix(".html")
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        prefix = "../" * (len(relative.parts) - 1)
        local_nav = navigation.replace('href="', f'href="{prefix}')
        current_href = prefix + relative.as_posix()
        local_nav = local_nav.replace(f'href="{current_href}"', f'class="active" href="{current_href}"')
        previous = pages[position - 1] if position else None
        following = pages[position + 1] if position + 1 < len(pages) else None
        pager = '<div class="pager">'
        pager += (f'<a href="{prefix}{previous[1].relative_to(SOURCE).with_suffix(".html").as_posix()}">← {html.escape(previous[0])}</a>' if previous else "<span></span>")
        pager += (f'<a href="{prefix}{following[1].relative_to(SOURCE).with_suffix(".html").as_posix()}">{html.escape(following[0])} →</a>' if following else "<span></span>")
        pager += "</div>"
        document = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — The OpenWALDO Book</title><link rel="stylesheet" href="{prefix}assets/book.css"></head><body><div class="layout"><nav><strong>The OpenWALDO Book</strong>{local_nav}</nav><main>{markdown_html(path.read_text(encoding='utf-8'))}{pager}</main></div></body></html>"""
        output.write_text(document, encoding="utf-8")
    assets = destination / "assets"
    assets.mkdir()
    (assets / "book.css").write_text(CSS, encoding="utf-8")
    index = destination / "index.html"
    index.write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=introduction.html"><title>The OpenWALDO Book</title><a href="introduction.html">Open the book</a>', encoding="utf-8")
    return index


def pdf_markup(value: str) -> str:
    value = html.escape(value)
    value = LINK.sub(lambda m: html.escape(m.group(1)), value)
    value = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    return value


def build_pdf(
    selected_chapters: list[tuple[str, Path]] | None = None,
    destination: Path | None = None,
    book_title: str = "The OpenWALDO Book",
    subtitle: str = "Auditable training data, provenance, and model workflows",
) -> Path:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String
        from reportlab.platypus import (
            BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph,
            Spacer, Table, TableStyle, XPreformatted,
        )
        from reportlab.platypus.tableofcontents import TableOfContents
    except ImportError as error:
        raise SystemExit("PDF generation requires ReportLab. Run `make setup` first.") from error

    selected_chapters = selected_chapters or chapters()
    destination = destination or OUTPUT / "pdf" / "openwaldo-book.pdf"
    destination.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BookTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=30, leading=35, textColor=colors.HexColor("#126e82"), alignment=TA_CENTER, spaceAfter=16))
    styles.add(ParagraphStyle(name="BookSubtitle", parent=styles["Normal"], fontSize=13, leading=19, textColor=colors.HexColor("#5c6975"), alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="ContentsTitle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=colors.HexColor("#126e82"), spaceAfter=14))
    styles.add(ParagraphStyle(name="Chapter1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=colors.HexColor("#126e82"), spaceAfter=14, keepWithNext=True))
    styles.add(ParagraphStyle(name="Chapter2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#18212a"), spaceBefore=15, spaceAfter=7, keepWithNext=True))
    styles.add(ParagraphStyle(name="Chapter3", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=12, leading=15, spaceBefore=11, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle(name="BookBody", parent=styles["BodyText"], fontSize=9.5, leading=14, spaceAfter=7))
    styles.add(ParagraphStyle(name="BookBullet", parent=styles["BookBody"], leftIndent=14, firstLineIndent=-7, bulletIndent=4, spaceAfter=1))
    styles.add(ParagraphStyle(name="BookQuote", parent=styles["BookBody"], leftIndent=10, rightIndent=10, borderPadding=8, backColor=colors.HexColor("#f4f7f8"), textColor=colors.HexColor("#394854"), spaceBefore=4, spaceAfter=10))
    styles.add(ParagraphStyle(name="BookCode", parent=styles["Code"], fontName="Courier", fontSize=6.7, leading=9, leftIndent=7, rightIndent=7, borderColor=colors.HexColor("#dce3e8"), borderWidth=.5, borderPadding=6, backColor=colors.HexColor("#f4f7f8"), spaceBefore=4, spaceAfter=8))

    page_width, page_height = A4
    margin = 20 * mm

    def pdf_diagram(source: str, width: float):
        nodes, edges, positions, node_width, node_height, height, _ = diagram_layout(source, width)
        drawing = Drawing(width, height)
        accent = colors.HexColor("#126e82")
        wash = colors.HexColor("#f4f7f8")
        ink = colors.HexColor("#18212a")

        def invert(point: tuple[float, float]) -> tuple[float, float]:
            return point[0], height - point[1]

        for edge in edges:
            x1, y1, x2, y2 = edge_points(positions[edge.source], positions[edge.target], node_width, node_height)
            x1, y1 = invert((x1, y1))
            x2, y2 = invert((x2, y2))
            line = Line(x1, y1, x2, y2, strokeColor=accent, strokeWidth=1.4)
            if edge.dotted:
                line.strokeDashArray = [4, 3]
            drawing.add(line)
            angle = math.atan2(y2 - y1, x2 - x1)
            arrow_size = 5.5
            left = (x2 - arrow_size * math.cos(angle - .55), y2 - arrow_size * math.sin(angle - .55))
            right = (x2 - arrow_size * math.cos(angle + .55), y2 - arrow_size * math.sin(angle + .55))
            drawing.add(Polygon([x2, y2, left[0], left[1], right[0], right[1]], fillColor=accent, strokeColor=accent))
            if edge.label:
                drawing.add(String((x1 + x2) / 2, (y1 + y2) / 2 + 5, edge.label, textAnchor="middle", fontName="Helvetica", fontSize=6.5, fillColor=ink))

        for node in nodes:
            x, y = invert(positions[node.identity])
            if node.start:
                drawing.add(Circle(x, y, 6, fillColor=accent, strokeColor=accent))
                continue
            drawing.add(Rect(x - node_width / 2, y - node_height / 2, node_width, node_height, rx=6, ry=6, fillColor=wash, strokeColor=accent, strokeWidth=1.3))
            labels = diagram_label_lines(node.label, node_width) or [node.identity]
            baseline = y + (len(labels) - 1) * 5
            for offset, label in enumerate(labels):
                drawing.add(String(x, baseline - offset * 10, label, textAnchor="middle", fontName="Helvetica", fontSize=7.2, fillColor=ink))
        drawing.hAlign = "CENTER"
        return drawing

    def decorate(canvas, doc) -> None:
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#dce3e8"))
        canvas.line(margin, 15 * mm, page_width - margin, 15 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#5c6975"))
        canvas.drawString(margin, 10 * mm, book_title)
        canvas.drawRightString(page_width - margin, 10 * mm, str(doc.page))
        canvas.restoreState()

    class BookTemplate(BaseDocTemplate):
        def __init__(self, filename: str):
            super().__init__(filename, pagesize=A4, leftMargin=margin, rightMargin=margin, topMargin=18 * mm, bottomMargin=21 * mm, title=book_title, author="OpenWALDO Project contributors")
            frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
            self.addPageTemplates(PageTemplate(id="book", frames=frame, onPage=decorate))

        def afterFlowable(self, flowable) -> None:
            if isinstance(flowable, Paragraph) and flowable.style.name in {"Chapter1", "Chapter2"}:
                level = 0 if flowable.style.name == "Chapter1" else 1
                self.notify("TOCEntry", (level, flowable.getPlainText(), self.page))

    story = [Spacer(1, 45 * mm), Paragraph(book_title, styles["BookTitle"]), Paragraph(subtitle, styles["BookSubtitle"]), Spacer(1, 25 * mm), Paragraph("Open Weights. Open Artifacts. Open Licenses.<br/>Open Data. Open Origins.", styles["BookSubtitle"]), PageBreak(), Paragraph("Contents", styles["ContentsTitle"])]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle(name="TOC1", fontName="Helvetica-Bold", fontSize=10, leading=14, leftIndent=0, firstLineIndent=0, spaceBefore=4), ParagraphStyle(name="TOC2", fontName="Helvetica", fontSize=8.5, leading=12, leftIndent=12, firstLineIndent=0)]
    story.extend([toc, PageBreak()])

    for chapter_index, (_, path) in enumerate(selected_chapters):
        if chapter_index:
            story.append(PageBreak())
        lines = path.read_text(encoding="utf-8").splitlines()
        position = 0
        paragraph: list[str] = []

        def flush() -> None:
            if paragraph:
                story.append(Paragraph(pdf_markup(" ".join(part.strip() for part in paragraph)), styles["BookBody"]))
                paragraph.clear()

        while position < len(lines):
            line = lines[position]
            fence = FENCE.match(line)
            if fence:
                flush()
                language = fence.group(1)
                code: list[str] = []
                position += 1
                while position < len(lines) and not lines[position].startswith("```"):
                    if language == "mermaid":
                        code.append(lines[position])
                    else:
                        code.extend(textwrap.wrap(lines[position], width=100, subsequent_indent="  ") or [""])
                    position += 1
                if language == "mermaid":
                    story.extend([Spacer(1, 5), pdf_diagram("\n".join(code), page_width - 2 * margin), Spacer(1, 8)])
                else:
                    story.append(XPreformatted(html.escape("\n".join(code)), styles["BookCode"]))
                position += 1
                continue
            heading = HEADING.match(line)
            if heading:
                flush()
                level = len(heading.group(1))
                style = styles["Chapter1"] if level == 1 else styles["Chapter2"] if level == 2 else styles["Chapter3"]
                story.append(Paragraph(pdf_markup(heading.group(2)), style))
                position += 1
                continue
            if position + 1 < len(lines) and "|" in line and re.match(r"^\s*\|?\s*:?-+", lines[position + 1]):
                flush()
                headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
                data = [[Paragraph(pdf_markup(cell), styles["BookBody"]) for cell in headers]]
                position += 2
                while position < len(lines) and "|" in lines[position] and lines[position].strip():
                    cells = [cell.strip() for cell in lines[position].strip().strip("|").split("|")]
                    data.append([Paragraph(pdf_markup(cell), styles["BookBody"]) for cell in cells])
                    position += 1
                widths = [((page_width - 2 * margin) / len(headers))] * len(headers)
                table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1f3")), ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#bdcbd1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
                story.extend([table, Spacer(1, 7)])
                continue
            bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
            numbered = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
            if bullet or numbered:
                flush()
                marker = "•" if bullet else numbered.group(1) + "."
                content = bullet.group(1) if bullet else numbered.group(2)
                story.extend([
                    Paragraph(pdf_markup(content), styles["BookBullet"], bulletText=marker),
                    Spacer(1, 1),
                ])
            elif line.startswith("> "):
                flush()
                quote = [line[2:]]
                position += 1
                while position < len(lines) and lines[position].startswith("> "):
                    quote.append(lines[position][2:])
                    position += 1
                story.append(Paragraph(pdf_markup(" ".join(quote)), styles["BookQuote"]))
                continue
            elif not line.strip():
                flush()
            else:
                paragraph.append(line)
            position += 1
        flush()

    BookTemplate(str(destination)).multiBuild(story)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("format", choices=("html", "pdf", "all", "model-guide", "contributor-guide", "quickstarts"))
    args = parser.parse_args()
    if args.format in {"html", "all"}:
        print(f"wrote HTML book: {build_html()}")
    if args.format in {"pdf", "all"}:
        print(f"wrote PDF book: {build_pdf()}")
    if args.format in {"model-guide", "quickstarts"}:
        model_path = SOURCE / "quickstarts" / "models.md"
        result = build_pdf(
            [("Training Quickstart", model_path)],
            OUTPUT / "pdf" / "openwaldo-model-quickstart.pdf",
            "OpenWALDO Training Quickstart",
            "Use open weights or build a provenance-linked model from scratch",
        )
        print(f"wrote model quickstart PDF: {result}")
    if args.format in {"contributor-guide", "quickstarts"}:
        contributor_path = SOURCE / "quickstarts" / "contributing.md"
        result = build_pdf(
            [("Contribute Training Data", contributor_path)],
            OUTPUT / "pdf" / "openwaldo-contributor-quickstart.pdf",
            "OpenWALDO Contributor Quickstart",
            "Turn acquired files into a verified, reviewable index contribution",
        )
        print(f"wrote contributor quickstart PDF: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
