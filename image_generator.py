import io
import os
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.png")
FONT_PATH = os.path.join(os.path.dirname(__file__), "Inter-SemiBold.ttf")

DESIGN_W = 1280
FONT_SIZE_DESIGN = 96

POSITIONS = {
    "rub_cny_cash": (86,  310),   # Y +84 вниз
    "rub_cny_card": (706, 310),
    "usdt_cny":     (86,  560),
    "rub_usdt":     (706, 560),
    "date":         (40,  839),
}

TEXT_COLOR = (255, 255, 255, 255)
DATE_COLOR = (0, 0, 0, 255)

def load_font(size_px: int):
    if os.path.exists(FONT_PATH):
        return ImageFont.truetype(FONT_PATH, size_px)
    fallbacks = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in fallbacks:
        if os.path.exists(path):
            return ImageFont.truetype(path, size_px)
    return ImageFont.load_default()

def generate_image(rates: list, date_str: str) -> io.BytesIO:
    img = Image.open(TEMPLATE_PATH).convert("RGBA")
    actual_w, _ = img.size

    scale = actual_w / DESIGN_W
    font_size = int(FONT_SIZE_DESIGN * scale)
    font = load_font(font_size)

    draw = ImageDraw.Draw(img)

    items = [
        ("rub_cny_cash", rates[0], TEXT_COLOR),
        ("rub_cny_card", rates[1], TEXT_COLOR),
        ("usdt_cny",     rates[2], TEXT_COLOR),
        ("rub_usdt",     rates[3], TEXT_COLOR),
        ("date",         date_str, DATE_COLOR),
    ]

    for key, value, color in items:
        x_design, y_design = POSITIONS[key]
        x = int(x_design * scale)
        y = int(y_design * scale)
        draw.text((x, y), value, font=font, fill=color)

    img_rgb = img.convert("RGB")
    buf = io.BytesIO()
    img_rgb.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf
