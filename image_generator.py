import io
import os
from PIL import Image, ImageDraw, ImageFont

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
    # Открываем без привязки к формату — работает и с PNG и с JPEG
    with open(TEMPLATE_PATH, "rb") as f:
        img = Image.open(f)
        img.load()
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
    img_rgb.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return buf

