"""Draws the app icon (a friendly police badge) as a 1024x1024 PNG."""
from PIL import Image, ImageDraw, ImageFont

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# rounded blue background
d.rounded_rectangle((40, 40, S - 40, S - 40), radius=220, fill=(24, 78, 170, 255))

# badge shape (shield)
shield = [
    (512, 150), (760, 230), (760, 520), (700, 700), (512, 860),
    (324, 700), (264, 520), (264, 230),
]
d.polygon(shield, fill=(255, 205, 60, 255), outline=(180, 130, 20, 255), width=14)
inner = [(x + (512 - x) * 0.14, y + (505 - y) * 0.14) for x, y in shield]
d.polygon(inner, fill=(255, 230, 120, 255))

# star
import math
cx, cy, r1, r2 = 512, 480, 190, 78
pts = []
for i in range(10):
    ang = -math.pi / 2 + i * math.pi / 5
    r = r1 if i % 2 == 0 else r2
    pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
d.polygon(pts, fill=(24, 78, 170, 255))

# "100" text
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
d.text((512, 720), "100", font=font, fill=(24, 78, 170, 255), anchor="mm")

img.save("src-tauri/icons/app-icon.png")
print("icon written")
