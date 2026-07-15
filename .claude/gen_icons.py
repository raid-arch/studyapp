from PIL import Image, ImageDraw, ImageFont
import os

BG = (16, 24, 56)      # matches --bg-ish dark navy
ACCENT = (124, 157, 255)  # matches --accent
GLYPH = "学"

def font_for(size):
    candidates = [
        r"C:\Windows\Fonts\YuGothB.ttc",
        r"C:\Windows\Fonts\meiryob.ttc",
        r"C:\Windows\Fonts\msgothic.ttc",
        r"C:\Windows\Fonts\arialbd.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def make_icon(size, maskable, out_path):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = int(size * 0.14) if maskable else 0
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=int(size * 0.22),
        fill=BG,
    )
    glyph_size = int((size - pad * 2) * 0.56)
    font = font_for(glyph_size)
    bbox = draw.textbbox((0, 0), GLYPH, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx, cy = size / 2, size / 2
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), GLYPH, font=font, fill=ACCENT)
    img.save(out_path)

out_dir = os.path.dirname(os.path.abspath(__file__)) + r"\.."
sizes = [
    (32, False, "icon-32.png"),
    (180, False, "icon-180.png"),
    (192, False, "icon-192.png"),
    (192, True, "icon-192-maskable.png"),
    (512, False, "icon-512.png"),
    (512, True, "icon-512-maskable.png"),
]
for size, maskable, name in sizes:
    make_icon(size, maskable, os.path.join(out_dir, name))

print("done")
