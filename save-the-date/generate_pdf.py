#!/usr/bin/env python3
"""Generate the Save the Date PDF for Alexa & Bruno's wedding."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageFilter
import os

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "1.jpeg")
QR = os.path.join(BASE, "QR.jpeg")
OUTPUT = os.environ.get("OUTPUT", os.path.join(BASE, "Save the date AB 2027.pdf"))
SITE = os.path.join(os.path.dirname(BASE), "index.html")


def site_values():
    """Single source of truth: read every <... data-w="key">value</...> from index.html.

    Keys used here: deposit, installments, installment, child, child_age, nights,
    agency, phone, email. Edit the website and re-run this script; never retype
    prices in two places."""
    import re, html
    src = open(SITE, encoding="utf-8").read()
    vals = {}
    for m in re.finditer(r'data-w="([a-z_]+)"[^>]*>([^<]*)<', src):
        vals[m.group(1)] = html.unescape(m.group(2)).strip()
    missing = [k for k in ("deposit", "installments", "installment", "child",
                           "child_age", "nights", "agency", "phone", "email") if k not in vals]
    if missing:
        raise SystemExit(f"index.html is missing data-w values for: {missing}")
    return vals


W_ = site_values()

# Colors
CREAM = Color(0.96, 0.93, 0.88)       # #f5ede0
GOLD = Color(0.79, 0.66, 0.43)         # #c9a96e
DARK = 0.04  # near-black value

W, H = A4  # 595.28 x 841.89 points


def draw_image_fill(c, img_path, x, y, w, h, upscale=3, blur=None):
    """Draw image filling the entire rectangle (crop to cover, no margins).
    blur: radius for GaussianBlur (None = no blur)."""
    img = Image.open(img_path)
    iw, ih = img.size
    target_ratio = w / h
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        # Image wider than target — crop sides
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        # Image taller than target — crop top/bottom
        new_h = int(iw / target_ratio)
        top = int((ih - new_h) * 0.35)
        img = img.crop((0, top, iw, top + new_h))
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    img = img.resize((int(w * upscale), int(h * upscale)), Image.LANCZOS)
    c.drawImage(ImageReader(img), x, y, w, h, preserveAspectRatio=False)


def draw_text(c, text, y, font, size, color=CREAM, center=True):
    """Draw text, centered by default."""
    c.setFont(font, size)
    c.setFillColor(color)
    if center:
        c.drawCentredString(W / 2, y, text)


def draw_rounded_rect(c, x, y, w, h, r, fill_color=None, stroke_color=None):
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
    if fill_color and stroke_color:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    elif stroke_color:
        c.drawPath(p, fill=0, stroke=1)


def gold_line(c, y, half_w=55):
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(W/2 - half_w, y, W/2 + half_w, y)


def overlay_rect(c, x, y, w, h, alpha):
    c.setFillColor(Color(DARK, DARK, DARK, alpha))
    c.rect(x, y, w, h, fill=1, stroke=0)


# ─── PAGE 1 ────────────────────────────────────────────────────────────
def page1(c):
    # Full-bleed background image (blurred for text legibility)
    draw_image_fill(c, IMG, 0, 0, W, H, blur=12)

    # ── Top band: RESERVA LA FECHA ──
    top_h = 58
    overlay_rect(c, 0, H - top_h, W, top_h, 0.72)
    draw_text(c, "RESERV\u00c1 LA FECHA", H - 38, "Helvetica", 12, GOLD)

    # ── Middle band: Quote + Names ──
    mid_top = H * 0.53
    mid_bot = H * 0.29
    overlay_rect(c, 0, mid_bot, W, mid_top - mid_bot, 0.72)

    cy = mid_top  # cursor from top of middle band

    cy -= 48
    draw_text(c, "Nuestro 25 ayer, hoy y siempre", cy, "Times-Italic", 21, CREAM)

    cy -= 14
    gold_line(c, cy, 50)

    cy -= 46
    draw_text(c, "Alexa", cy, "Times-BoldItalic", 50, white)

    cy -= 36
    draw_text(c, "&", cy, "Times-BoldItalic", 30, GOLD)

    cy -= 44
    draw_text(c, "Bruno", cy, "Times-BoldItalic", 50, white)

    # ── Bottom band: Details ──
    bot_top = mid_bot
    overlay_rect(c, 0, 0, W, bot_top, 0.78)

    dy = bot_top - 32
    draw_text(c, "VIERNES \u00b7 25 DE JUNIO \u00b7 2027", dy, "Helvetica", 12, CREAM)

    dy -= 22
    draw_text(c, "Cura\u00e7ao \u00b7 Caribe \u00b7 Todo Incluido", dy, "Helvetica", 11, CREAM)

    dy -= 16
    gold_line(c, dy, 80)

    dy -= 22
    # Website — clickable
    web_text = "boda.rivasberaud.com"
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(CREAM)
    tw = c.stringWidth(web_text, "Helvetica-Bold", 13)
    wx = W/2 - tw/2
    c.drawString(wx, dy, web_text)
    c.linkURL("https://boda.rivasberaud.com", (wx - 15, dy - 5, wx + tw + 15, dy + 18), relative=0)

    dy -= 18
    draw_text(c, "Todos los detalles en nuestra p\u00e1gina", dy, "Helvetica", 9, Color(0.96, 0.93, 0.88, 0.7))

    dy -= 24
    draw_text(c, "11 A\u00d1OS \u00b7 2 HIJOS \u00b7 1 HISTORIA", dy, "Helvetica", 9, GOLD)


# ─── PAGE 2 ────────────────────────────────────────────────────────────
def page2(c):
    # Dark background
    c.setFillColor(Color(DARK, DARK, DARK))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── SECTION 1: Top image (~62%) ──
    img_h = H * 0.62
    draw_image_fill(c, IMG, 0, H - img_h, W, img_h)

    # Subtle dark overlay on image for text contrast
    overlay_rect(c, 0, H - img_h, W, img_h, 0.35)

    # Names centered on image
    ny = H - img_h * 0.42
    c.setFont("Times-BoldItalic", 42)
    c.setFillColor(white)
    c.drawCentredString(W / 2, ny, "Alexa & Bruno")

    gold_line(c, ny - 14, 60)

    # ── SECTION 2: Detail boxes ──
    sec2_top = H - img_h - 16
    box_h = 48
    box_gap = 14
    margin_x = 24
    box_w = (W - margin_x * 2 - box_gap * 2) / 3
    sec2_bot = sec2_top - box_h

    items = [
        ("FECHA", "25 Junio 2027"),
        ("LUGAR", "Cura\u00e7ao"),
        ("FORMATO", "Todo Incluido"),
    ]
    for i, (label, value) in enumerate(items):
        bx = margin_x + i * (box_w + box_gap)
        draw_rounded_rect(c, bx, sec2_bot, box_w, box_h, 3,
                          stroke_color=Color(0.79, 0.66, 0.43, 0.5))
        # Label (top of box)
        c.setFont("Helvetica", 8)
        c.setFillColor(GOLD)
        c.drawCentredString(bx + box_w / 2, sec2_bot + box_h - 16, label)
        # Value (bottom of box)
        c.setFont("Helvetica", 10.5)
        c.setFillColor(CREAM)
        c.drawCentredString(bx + box_w / 2, sec2_bot + 8, value)

    # ── SECTION 3: Two columns (Song + Reservas) ──
    sec3_top = sec2_bot - 24
    col_margin = 20
    col_gap = 16
    col_w = (W - col_margin * 2 - col_gap) / 2
    col_h = 168
    col_bot = sec3_top - col_h

    # ── Left column: NUESTRA CANCIÓN ──
    lx = col_margin
    l_mid = lx + col_w / 2
    draw_rounded_rect(c, lx, col_bot, col_w, col_h, 5,
                       fill_color=Color(0.06, 0.06, 0.06),
                       stroke_color=Color(0.79, 0.66, 0.43, 0.25))

    # Title — 22pt from top of column
    title_y = col_bot + col_h - 22
    c.setFont("Helvetica", 9)
    c.setFillColor(GOLD)
    c.drawCentredString(l_mid, title_y, "NUESTRA CANCI\u00d3N")

    gold_line_at_title = title_y - 10
    c.setStrokeColor(Color(0.79, 0.66, 0.43, 0.3))
    c.setLineWidth(0.4)
    c.line(lx + 25, gold_line_at_title, lx + col_w - 25, gold_line_at_title)

    # Bottom label
    label_y = col_bot + 20
    c.setFont("Helvetica", 8)
    c.setFillColor(Color(0.96, 0.93, 0.88, 0.6))
    c.drawCentredString(l_mid, label_y, "Escane\u00e1 con Spotify")

    # Spotify code image — centered between title underline and bottom label
    if os.path.exists(QR):
        qr_img = Image.open(QR)
        qr_iw, qr_ih = qr_img.size
        qr_ratio = qr_iw / qr_ih  # ~4:1
        qr_w = col_w - 30
        qr_h = qr_w / qr_ratio
        qr_x = lx + (col_w - qr_w) / 2
        # Center vertically between gold line and label
        space_top = gold_line_at_title - 12
        space_bot = label_y + 12
        qr_y = space_bot + (space_top - space_bot - qr_h) / 2
        c.drawImage(ImageReader(qr_img), qr_x, qr_y, qr_w, qr_h)

    # ── Right column: RESERVAS OFICIALES ──
    rx = lx + col_w + col_gap
    r_mid = rx + col_w / 2
    draw_rounded_rect(c, rx, col_bot, col_w, col_h, 5,
                       fill_color=Color(0.06, 0.06, 0.06),
                       stroke_color=Color(0.79, 0.66, 0.43, 0.25))

    # Title — 22pt from top of column
    ry_title = col_bot + col_h - 22
    c.setFont("Helvetica", 9)
    c.setFillColor(GOLD)
    c.drawCentredString(r_mid, ry_title, "RESERVAS OFICIALES")

    gold_line_at_ry = ry_title - 10
    c.setStrokeColor(Color(0.79, 0.66, 0.43, 0.3))
    c.setLineWidth(0.4)
    c.line(rx + 25, gold_line_at_ry, rx + col_w - 25, gold_line_at_ry)

    # Contact info — centered in top half (gold line → midpoint)
    top_bound = gold_line_at_ry - 8
    mid_bound = (gold_line_at_ry + label_y) / 2
    bot_bound = mid_bound - 6

    contact_lines = [
        (W_["agency"], "Helvetica", 10, CREAM),
        (W_["phone"], "Helvetica", 9, CREAM),
        (W_["email"], "Helvetica", 7.5, CREAM),
    ]
    contact_gaps = [0, 16, 14, 12]
    contact_total = sum(contact_gaps)
    ry = top_bound - (top_bound - bot_bound - contact_total) / 2

    for idx, (txt, font, size, color) in enumerate(contact_lines):
        if idx > 0:
            ry -= contact_gaps[idx]
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawCentredString(r_mid, ry, txt)

    # Divider at midpoint
    c.setStrokeColor(Color(0.79, 0.66, 0.43, 0.3))
    c.setLineWidth(0.4)
    c.line(rx + 20, mid_bound, rx + col_w - 20, mid_bound)

    # Package info — centered in bottom half (midpoint → label)
    pkg_top = mid_bound - 10
    pkg_bot = label_y + 6
    pkg_lines = [
        (f"PAQUETE EST\u00c1NDAR: {W_['nights']} NOCHES", "Helvetica", 7.5, GOLD),
        (f"USD {W_['deposit']} + {W_['installments']} \u00d7 USD {W_['installment']}", "Helvetica-Bold", 10, GOLD),
        (f"Ni\u00f1os hasta {W_['child_age']} a\u00f1os: USD {W_['child']}", "Helvetica", 7.5, Color(0.96, 0.93, 0.88, 0.6)),
    ]
    pkg_gaps = [0, 12, 14, 12]
    pkg_total = sum(pkg_gaps)
    pr_y = pkg_top - (pkg_top - pkg_bot - pkg_total) / 2

    for idx, (txt, font, size, color) in enumerate(pkg_lines):
        if idx > 0:
            pr_y -= pkg_gaps[idx]
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawCentredString(r_mid, pr_y, txt)

    # ── SECTION 4: Footer ──
    fy1 = col_bot - 24
    c.setFont("Helvetica", 7)
    c.setFillColor(Color(0.96, 0.93, 0.88, 0.45))
    c.drawCentredString(W / 2, fy1,
                        "Descuentos por tiempo y plazas limitadas \u00b7 Se requiere dep\u00f3sito para confirmar reserva")

    fy2 = fy1 - 18
    c.setFont("Helvetica", 8)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, fy2, "25 \u00b7 VI \u00b7 MMXXVII \u00b7 CURA\u00c7AO")


def main():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("Save the Date - Alexa & Bruno - 25 de Junio 2027")
    c.setAuthor("Alexa & Bruno")
    page1(c)
    c.showPage()
    page2(c)
    c.showPage()
    c.save()
    print(f"PDF saved to: {OUTPUT}")
    print(f"File size: {os.path.getsize(OUTPUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
