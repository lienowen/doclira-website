"""Generate fresh demo screenshots for website."""
import os, fitz
from PIL import Image, ImageDraw, ImageFont

WEBSITE_ASSETS = r"d:\develop\me\pdf_desktop\website\public\assets"
DEMO_PDF = r"d:\develop\me\pdf_desktop\recording_output\demo_pdfs_clean\Employment_Agreement_Demo.pdf"
W = 1200
H = 750
BG = (248, 250, 252)
ACCENT = (13, 148, 136)
DARK = (15, 23, 42)
WHITE = (255, 255, 255)
LIGHT = (100, 116, 139)
RED = (220, 38, 38)
try:
    FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 32)
    FONT_SM = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 20)
except:
    FONT = FONT_SM = ImageFont.load_default()

os.makedirs(WEBSITE_ASSETS, exist_ok=True)

def make_hero():
    """Hero: split before/after redaction."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Left: Before
    draw.rounded_rectangle([30, 50, 575, H-30], radius=12, fill=WHITE, outline="#e2e8f0")
    draw.text((60, 70), "BEFORE", fill=RED, font=FONT)
    draw.text((60, 115), "Contract with visible", fill=DARK, font=FONT_SM)
    draw.text((60, 145), "phone, email, SSN, salary", fill=LIGHT, font=FONT_SM)

    # Simulate redaction blocks on left
    for (x, y, w, h, c) in [
        (80, 200, 200, 16, (220,38,38,60)),
        (80, 250, 280, 16, (5,150,105,60)),
        (80, 300, 160, 16, (37,99,235,60)),
        (80, 380, 220, 16, (220,38,38,60)),
        (80, 430, 300, 16, (245,158,11,60)),
    ]:
        # Show colored highlight
        overlay = Image.new("RGBA", img.size, (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle([x, y, x+w, y+h], radius=3, fill=c)
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)

    # Right: After
    draw.rounded_rectangle([625, 50, 1170, H-30], radius=12, fill=DARK, outline="#334155")
    draw.text((655, 70), "AFTER REDACTION", fill=ACCENT, font=FONT)
    draw.text((655, 115), "Sensitive data wiped", fill="#e2e8f0", font=FONT_SM)
    draw.text((655, 145), "Safe to share", fill=LIGHT, font=FONT_SM)

    # Dark redaction bars on right
    for (x2, y2, w2, h2) in [
        (670, 200, 200, 16),
        (670, 250, 280, 16),
        (670, 300, 160, 16),
        (670, 380, 220, 16),
        (670, 430, 300, 16),
    ]:
        draw.rounded_rectangle([x2, y2, x2+w2, y2+h2], radius=2, fill=(18,18,20))

    # Arrow between
    draw.text((575, H//2 - 20), "→", fill=ACCENT, font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 48) if os.path.exists(r"C:\Windows\Fonts\arialbd.ttf") else FONT)

    # Bottom label
    draw.text((60, H-60), "Doclira PDF — Smart Redaction", fill=LIGHT, font=FONT_SM)

    path = os.path.join(WEBSITE_ASSETS, "hero_redaction_en.png")
    img.save(path, "PNG")
    print(f"✓ {path}")

def make_feature_card(filename, title, desc, color):
    """Small feature preview cards."""
    img = Image.new("RGB", (560, 340), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 560, 4], fill=color)
    draw.text((24, 24), title, fill=DARK, font=FONT)
    draw.text((24, 68), desc, fill=LIGHT, font=FONT_SM)
    path = os.path.join(WEBSITE_ASSETS, filename)
    img.save(path, "PNG")
    print(f"✓ {path}")


# Generate
make_hero()
make_feature_card("feature_redact.png", "🔒 Smart Redaction", "Auto-detect emails, phones, IDs, amounts", (220,38,38))
make_feature_card("feature_audit.png", "🔍 Security Audit", "Scan metadata, scripts, embedded files", (8,145,178))
make_feature_card("feature_ai.png", "🤖 AI Chat", "Ask, summarize, extract — files stay local", (139,92,246))

print("\nDone — refresh doclira.com")
