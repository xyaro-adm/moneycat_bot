import io
import os
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.png")
FONT_PATH = os.path.join(os.path.dirname(__file__), "Inter-SemiBold.ttf")

DESIGN_W = 1280
FONT_SIZE_DESIGN = 96
BASELINE_CORRECTION = int(FONT_SIZE_DESIGN * 0.75)

POSITIONS = {
    "rub_cny_cash": (86,  226 - BASELINE_CORRECTION),
    "rub_cny_card": (706, 226 - BASELINE_CORRECTION),
    "usdt_cny":     (86,  476 - BASELINE_CORRECTION),
    "rub_usdt":     (706, 476 - BASELINE_CORRECTION),
    "date":         (40,  839 - BASELINE_CORRECTION),
}

TEXT_COLOR = (255, 255, 255, 255)

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
    # Диагностика
    logger.info(f"TEMPLATE_PATH: {TEMPLATE_PATH}")
    logger.info(f"File exists: {os.path.exists(TEMPLATE_PATH)}")
    if os.path.exists(TEMPLATE_PATH):
        size = os.path.getsize(TEMPLATE_PATH)
        logger.info(f"File size: {size} bytes")
        # Читаем первые байты чтобы определить формат
        with open(TEMPLATE_PATH, "rb") as f:
            header = f.read(12)
        logger.info(f"File header (hex): {header.hex()}")

    img = Image.open(TEMPLATE_PATH)
    logger.info(f"Image format: {img.format}, size: {img.size}, mode: {img.mode}")
    img = img.convert("RGBA")

    actual_w, _ = img.size
    scale = actual_w / DESIGN_W
    font_size = int(FONT_SIZE_DESIGN * scale)
    font = load_font(font_size)

    draw = ImageDraw.Draw(img)

    values = {
        "rub_cny_cash": rates[0],
        "rub_cny_card": rates[1],
        "usdt_cny":     rates[2],
        "rub_usdt":     rates[3],
        "date":         date_str,
    }

    for key, (x_design, y_design) in POSITIONS.items():
        x = int(x_design * scale)
        y = int(y_design * scale)
        draw.text((x, y), values[key], font=font, fill=TEXT_COLOR)

    img_rgb = img.convert("RGB")
    buf = io.BytesIO()
    img_rgb.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf
