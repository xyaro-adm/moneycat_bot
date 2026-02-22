import io
import os
from PIL import Image, ImageDraw, ImageFont

# Шаблон лежит рядом с этим файлом
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.png")

# Оригинальный дизайн был 1280x960, но PNG оказался 2000x1500
# Считаем масштаб автоматически
DESIGN_W = 1280
DESIGN_H = 960

# Позиции из ТЗ (в координатах дизайна 1280x960)
# Каждый курс: (x, y) — левый нижний угол числа (как в Figma/дизайне)
POSITIONS = {
    "rub_cny_cash":  (86,  226),   # RUB/CNY Нал
    "rub_cny_card":  (706, 226),   # RUB/CNY Карта
    "usdt_cny":      (86,  476),   # USDT/CNY
    "rub_usdt":      (706, 476),   # RUB/USDT
    "date":          (40,  839),   # Дата
}

FONT_SIZE_DESIGN = 96       # px в дизайне
DATE_FONT_SIZE_DESIGN = 96  # px дата

# Цвет текста — белый
TEXT_COLOR = (255, 255, 255, 255)

def load_font(size_px: int):
    """Загружает Inter Semibold или fallback на системный шрифт."""
    font_paths = [
        "/usr/share/fonts/truetype/inter/Inter-SemiBold.ttf",
        "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
        os.path.join(os.path.dirname(__file__), "fonts", "Inter-SemiBold.ttf"),
        "/System/Library/Fonts/Helvetica.ttc",  # Mac fallback
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux fallback
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size_px)
    
    # Последний fallback — дефолтный шрифт PIL (не красиво, но работает)
    return ImageFont.load_default()

def generate_image(rates: list[str], date_str: str) -> io.BytesIO:
    """
    rates: [rub_cny_cash, rub_cny_card, usdt_cny, rub_usdt]
    date_str: например "07 Фев"
    Возвращает BytesIO с PNG.
    """
    img = Image.open(TEMPLATE_PATH).convert("RGBA")
    actual_w, actual_h = img.size

    # Масштабный коэффициент
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
        text = values[key]
        draw.text((x, y), text, font=font, fill=TEXT_COLOR)

    # Конвертируем обратно в RGB для отправки в Telegram
    img_rgb = img.convert("RGB")
    buf = io.BytesIO()
    img_rgb.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf
