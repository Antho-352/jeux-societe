"""Shared page helpers for the printable-puzzle generators.

US Letter page, 18 mm margins (so the same PDF prints unscaled on A4),
title line at the top, small licence footer, pure vector output.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = letter            # 612 x 792 pt
MARGIN = 18 * 72 / 25.4            # 18 mm = 51 pt (>= 15 mm asked)
CONTENT_W = PAGE_W - 2 * MARGIN    # 510 pt
TITLE_H = 54                       # vertical room used by the title block
FOOTER_H = 22
FOOTER_TEXT = "printandplaygame.com · CC BY-NC 4.0"
INK = (0.08, 0.08, 0.10)
GREY = (0.45, 0.45, 0.48)
LIGHT = (0.86, 0.86, 0.88)
RED = (0.85, 0.12, 0.12)

ROOT = Path(__file__).resolve().parents[2]
PDF_ROOT = ROOT / "public" / "pdf" / "puzzles"
IMG_ROOT = ROOT / "public" / "img" / "puzzles"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def new_canvas(path: str | os.PathLike, title: str, subject: str = "") -> canvas.Canvas:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle(title)
    c.setAuthor("printandplaygame.com")
    if subject:
        c.setSubject(subject)
    c.setCreator("printandplaygame.com puzzle generators")
    return c


def page_header(c: canvas.Canvas, title: str, subtitle: str = "", page_no: int | None = None,
                total: int | None = None) -> float:
    """Draw the title block and footer. Returns the y of the top of the free area."""
    c.setFillColorRGB(*INK)
    size = 22 if len(title) <= 34 else 18 if len(title) <= 46 else 15
    c.setFont("Helvetica-Bold", size)
    c.drawString(MARGIN, PAGE_H - MARGIN - size + 4, title)
    y = PAGE_H - MARGIN - size - 12
    if subtitle:
        c.setFont("Helvetica", 9.5)
        c.setFillColorRGB(*GREY)
        c.drawString(MARGIN, y, subtitle)
        y -= 6
    # thin rule under the title block
    c.setStrokeColorRGB(*LIGHT)
    c.setLineWidth(0.8)
    c.line(MARGIN, y - 4, PAGE_W - MARGIN, y - 4)
    # footer
    c.setFont("Helvetica", 7.5)
    c.setFillColorRGB(*GREY)
    c.drawCentredString(PAGE_W / 2, MARGIN - 14, FOOTER_TEXT)
    if page_no is not None:
        label = f"{page_no}" if total is None else f"{page_no} / {total}"
        c.drawRightString(PAGE_W - MARGIN, MARGIN - 14, label)
    c.setFillColorRGB(*INK)
    return y - 12


def free_area(top_y: float) -> tuple[float, float, float, float]:
    """(x0, y0, width, height) of the drawable area below the header."""
    return MARGIN, MARGIN + 8, CONTENT_W, top_y - MARGIN - 8


def render_cover(pdf_path: str | os.PathLike, png_path: str | os.PathLike, size: int = 600) -> None:
    """Render page 1 with pypdfium2, crop to a square (top of the page), save a PNG."""
    import pypdfium2 as pdfium
    from PIL import Image

    pdf = pdfium.PdfDocument(str(pdf_path))
    page = pdf[0]
    scale = size / page.get_width()
    bitmap = page.render(scale=scale)
    img = bitmap.to_pil().convert("RGB")
    w, h = img.size
    side = min(w, h)
    # Keep the title and the top of the puzzle: crop from a little below the top edge.
    top = int(min(max(0, 0.02 * h), h - side))
    img = img.crop((0, top, side, top + side)).resize((size, size), Image.LANCZOS)
    Path(png_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(str(png_path), optimize=True)
    page.close()
    pdf.close()


def pdf_pages(pdf_path: str | os.PathLike) -> int:
    from pypdf import PdfReader
    return len(PdfReader(str(pdf_path)).pages)


def size_mb(path: str | os.PathLike) -> float:
    return round(os.path.getsize(path) / (1024 * 1024), 2)
