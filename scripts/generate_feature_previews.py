from pathlib import Path
import shutil
import tempfile

import fitz
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "release_assets" / "test_pdfs"
OUT_DIR = ROOT / "website" / "public" / "assets"
CANVAS = (1440, 840)
BG = "#f4f7fa"
PANEL = "#ffffff"
INK = "#101c30"
MUTED = "#60728b"
LINE = "#d7e2ef"
BLUE = "#2463e8"
GREEN = "#087f70"
ORANGE = "#e86c45"


def font(size, bold=False):
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc") if bold else Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf") if bold else Path(r"C:\Windows\Fonts\simsun.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def text(draw, position, value, size, fill=INK, bold=False):
    draw.text(position, value, font=font(size, bold), fill=fill)


def rounded(draw, box, fill=PANEL, outline=LINE, radius=14, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def badge(draw, box, value, fill="#e7f0ff", color=BLUE):
    draw.rounded_rectangle(box, radius=14, fill=fill)
    bbox = draw.textbbox((0, 0), value, font=font(22, True))
    x = box[0] + (box[2] - box[0] - (bbox[2] - bbox[0])) / 2
    y = box[1] + (box[3] - box[1] - (bbox[3] - bbox[1])) / 2 - 2
    text(draw, (x, y), value, 22, color, True)


def arrow(draw, start, end, label):
    x1, y = start
    x2, _ = end
    draw.line((x1, y, x2 - 22, y), fill=GREEN, width=7)
    draw.polygon(((x2 - 22, y - 14), (x2, y), (x2 - 22, y + 14)), fill=GREEN)
    bbox = draw.textbbox((0, 0), label, font=font(20, True))
    text(draw, ((x1 + x2 - bbox[2]) / 2, y - 48), label, 20, GREEN, True)


def render_pages(pdf_name, zoom=0.7):
    document = fitz.open(str(PDF_DIR / pdf_name))
    images = []
    for page in document:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        images.append(Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples))
    document.close()
    return images


def render_file_pages(path, zoom=0.7):
    document = fitz.open(str(path))
    images = []
    for page in document:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        images.append(Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples))
    document.close()
    return images


def render_crop(path, clip, zoom=3.0):
    document = fitz.open(str(path))
    pixmap = document[0].get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    document.close()
    return image


def contain(canvas, image, box):
    x1, y1, x2, y2 = box
    ratio = min((x2 - x1) / image.width, (y2 - y1) / image.height)
    image = image.resize((int(image.width * ratio), int(image.height * ratio)), Image.Resampling.LANCZOS)
    x = x1 + (x2 - x1 - image.width) // 2
    y = y1 + (y2 - y1 - image.height) // 2
    canvas.paste(image, (x, y))


def header(draw, title, subtitle):
    text(draw, (56, 42), title, 46, INK, True)
    text(draw, (56, 104), subtitle, 23, MUTED)


def create_pdf_to_images():
    pages = render_pages("04_multipage_preview_edit.pdf", 0.8)
    canvas = Image.new("RGB", (1440, 1110), BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "PDF \u8f6c\u56fe\u7247", "\u4e00\u4e2a 3 \u9875 PDF \u6587\u4ef6\uff0c\u5bfc\u51fa\u4e3a 3 \u5f20\u53ef\u5355\u72ec\u4f7f\u7528\u7684 PNG \u56fe\u7247")

    rounded(draw, (56, 174, 1384, 448))
    text(draw, (86, 200), "\u8f93\u5165 PDF", 29, INK, True)
    badge(draw, (1192, 196, 1338, 242), "3 \u9875 PDF", "#fce9e6", ORANGE)
    text(draw, (86, 258), "04_multipage_preview_edit.pdf", 24, MUTED)
    contain(canvas, pages[0], (750, 202, 952, 422))
    contain(canvas, pages[1], (960, 202, 1162, 422))

    text(draw, (606, 471), "\u5bfc\u51fa PNG", 25, GREEN, True)
    draw.line((515, 515, 925, 515), fill=GREEN, width=7)
    draw.polygon(((925, 515), (899, 498), (899, 532)), fill=GREEN)

    rounded(draw, (56, 560, 1384, 1050))
    text(draw, (86, 590), "\u8f93\u51fa\u6587\u4ef6\u5939", 29, INK, True)
    badge(draw, (1160, 586, 1338, 632), "PNG x 3", "#def5eb", GREEN)
    text(draw, (86, 648), "04_multipage_preview_edit_\u5bfc\u51fa\u56fe\u7247\\", 22, MUTED)
    boxes = [(122, 704, 480, 984), (540, 704, 898, 984), (958, 704, 1316, 984)]
    for i, (image, box) in enumerate(zip(pages, boxes), start=1):
        rounded(draw, box, "#ffffff", LINE, 8, 1)
        contain(canvas, image, (box[0] + 12, box[1] + 10, box[2] - 12, box[3] - 54))
        text(draw, (box[0] + 88, box[3] - 42), f"\u7b2c{i:03d}\u9875.png", 23, BLUE, True)
    badge(draw, (450, 1066, 990, 1106), "\u6bcf\u4e00\u9875\u90fd\u662f\u72ec\u7acb\u56fe\u7247\u6587\u4ef6", "#def5eb", GREEN)
    canvas.save(OUT_DIR / "demo_pdf_to_images_clear.png", quality=96)


def create_page_tools():
    pages = render_pages("04_multipage_preview_edit.pdf", 0.52)
    canvas = Image.new("RGB", CANVAS, BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "PDF \u5408\u5e76 / \u62c6\u5206", "\u8f93\u5165\u548c\u8f93\u51fa\u6570\u91cf\u76f4\u63a5\u5bf9\u7167\uff0c\u4e0d\u4f1a\u628a\u591a\u4e2a\u529f\u80fd\u6df7\u5728\u4e00\u5f20\u7ed3\u679c\u56fe\u91cc")
    rounded(draw, (56, 180, 694, 770))
    text(draw, (84, 206), "\u62c6\u5206 PDF", 28, INK, True)
    badge(draw, (84, 262, 246, 304), "1 \u4e2a PDF", "#edf3ff", BLUE)
    arrow(draw, (270, 284), (374, 284), "\u62c6\u5206")
    badge(draw, (400, 262, 628, 304), "3 \u4e2a\u5355\u9875 PDF", "#def5eb", GREEN)
    contain(canvas, pages[0], (102, 348, 258, 604))
    for index, page in enumerate(pages):
        x = 320 + index * 112
        contain(canvas, page, (x, 372, x + 98, 538))
        text(draw, (x, 558), f"{index + 1}.pdf", 15, BLUE, True)
    text(draw, (84, 690), "contract.pdf  \u2192  page_001.pdf, page_002.pdf, page_003.pdf", 17, MUTED)

    rounded(draw, (746, 180, 1384, 770))
    text(draw, (774, 206), "\u5408\u5e76 PDF", 28, INK, True)
    badge(draw, (774, 262, 1002, 304), "3 \u4e2a\u5355\u9875 PDF", "#edf3ff", BLUE)
    arrow(draw, (1024, 284), (1126, 284), "\u5408\u5e76")
    badge(draw, (1144, 262, 1338, 304), "1 \u4e2a PDF", "#def5eb", GREEN)
    for index, page in enumerate(pages):
        x = 792 + index * 112
        contain(canvas, page, (x, 374, x + 98, 540))
    contain(canvas, pages[0], (1170, 344, 1314, 586))
    text(draw, (1176, 608), "merged.pdf", 17, GREEN, True)
    text(draw, (774, 690), "page_001.pdf + page_002.pdf + page_003.pdf  \u2192  merged.pdf", 17, MUTED)
    canvas.save(OUT_DIR / "demo_merge_split_clear.png", quality=96)


def create_watermark():
    clean = render_pages("04_multipage_preview_edit.pdf", 0.6)[0]
    marked = render_pages("06_watermark_tiled_demo.pdf", 0.6)[0]
    canvas = Image.new("RGB", CANVAS, BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "\u6279\u91cf\u52a0\u6c34\u5370", "\u4fdd\u7559\u6587\u6863\u5185\u5bb9\uff0c\u5728\u9875\u9762\u80cc\u666f\u4e0a\u53e0\u52a0\u53ef\u8bc6\u522b\u7684\u6743\u5c5e\u6807\u8bb0")
    rounded(draw, (56, 176, 618, 770))
    text(draw, (84, 202), "\u539f\u6587\u4ef6", 25, INK, True)
    badge(draw, (438, 198, 576, 238), "\u65e0\u6c34\u5370", "#edf3ff", BLUE)
    contain(canvas, clean, (136, 272, 530, 682))
    arrow(draw, (650, 462), (774, 462), "\u5e73\u94fa\u6c34\u5370")
    rounded(draw, (808, 176, 1384, 770))
    text(draw, (838, 202), "\u5904\u7406\u540e PDF", 25, INK, True)
    badge(draw, (1164, 198, 1340, 238), "CONFIDENTIAL", "#def5eb", GREEN)
    contain(canvas, marked, (900, 272, 1294, 682))
    text(draw, (984, 704), "\u900f\u660e\u5ea6\u4f4e / \u6587\u5b57\u4ecd\u53ef\u9605\u8bfb", 18, GREEN, True)
    canvas.save(OUT_DIR / "demo_watermark_clear.png", quality=96)


def create_text_edit():
    source = PDF_DIR / "01_text_chinese_english.pdf"
    original_value = "\u4e0a\u6d77\u6668\u661f\u79d1\u6280\u6709\u9650\u516c\u53f8"
    updated_value = "\u676d\u5dde\u5b89\u8861\u8d38\u6613\u6709\u9650\u516c\u53f8"
    font_path = r"C:\Windows\Fonts\msyh.ttc"
    with tempfile.TemporaryDirectory() as tmp_dir:
        output = Path(tmp_dir) / "edited_result.pdf"
        document = fitz.open(str(source))
        page = document[0]
        targets = page.search_for(original_value)
        if not targets:
            raise RuntimeError("Could not find the sample text edit field.")
        target = targets[0]
        span_style = {"size": 10.0, "origin": fitz.Point(target.x0, target.y1 - 2)}
        for block in page.get_text("dict").get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if original_value in span.get("text", ""):
                        span_style = {"size": span["size"], "origin": fitz.Point(span["origin"])}
        page.add_redact_annot(target + (-1, -1, 2, 1), fill=(1, 1, 1))
        page.apply_redactions()
        page.insert_text(
            fitz.Point(target.x0, span_style["origin"].y),
            updated_value,
            fontsize=span_style["size"],
            fontname="editcn",
            fontfile=font_path if Path(font_path).exists() else None,
            color=(0, 0, 0),
        )
        document.save(str(output), garbage=4, deflate=True)
        document.close()

        clip = fitz.Rect(max(0, target.x0 - 98), target.y0 - 4, min(595, target.x1 + 206), target.y1 + 48)
        before_crop = render_crop(source, clip)
        after_crop = render_crop(output, clip)

        canvas = Image.new("RGB", (1440, 1110), BG)
        draw = ImageDraw.Draw(canvas)
        header(draw, "PDF \u6587\u5b57\u4fee\u6539", "\u540c\u4e00\u4e2a\u5b57\u6bb5\uff0c\u4fee\u6539\u524d\u540e\u4e0a\u4e0b\u5bf9\u7167\uff1a\u4e0d\u9700\u8981\u653e\u5927\u5373\u53ef\u770b\u6e05\u6587\u5b57\u53d8\u5316")

        rounded(draw, (56, 172, 1384, 524))
        text(draw, (90, 204), "\u4fee\u6539\u524d", 31, INK, True)
        badge(draw, (1174, 198, 1338, 246), "\u539f PDF", "#edf3ff", BLUE)
        rounded(draw, (90, 270, 1350, 472), "#fafcff", "#b9d4fd", 8, 2)
        contain(canvas, before_crop, (128, 292, 1312, 446))

        text(draw, (634, 548), "\u66ff\u6362\u540e\u4fdd\u5b58", 25, GREEN, True)
        draw.line((690, 586, 690, 626), fill=GREEN, width=7)
        draw.polygon(((690, 650), (673, 622), (707, 622)), fill=GREEN)

        rounded(draw, (56, 678, 1384, 1030), "#ffffff", "#9bdacb", 14, 2)
        text(draw, (90, 710), "\u4fee\u6539\u540e", 31, INK, True)
        badge(draw, (1168, 704, 1338, 752), "\u65b0 PDF", "#def5eb", GREEN)
        rounded(draw, (90, 776, 1350, 978), "#f5fdf9", "#73c9b3", 8, 2)
        contain(canvas, after_crop, (128, 798, 1312, 952))
        badge(draw, (504, 1052, 936, 1098), "\u53ea\u66ff\u6362\u9009\u4e2d\u7684\u6587\u5b57\u5185\u5bb9", "#def5eb", GREEN)
        canvas.save(OUT_DIR / "demo_text_edit_clear.png", quality=96)


def preview_page(draw, box, title, lines, watermark=None):
    rounded(draw, box, "#ffffff", LINE, 8, 1)
    x1, y1, x2, y2 = box
    text(draw, (x1 + 28, y1 + 26), title, 20, BLUE, True)
    for index, line in enumerate(lines):
        text(draw, (x1 + 28, y1 + 82 + index * 34), line, 17, INK)
    if watermark:
        for y in range(y1 + 94, y2 - 12, 76):
            text(draw, (x1 + 42, y), watermark, 24, "#c8daf4", True)


def create_text_edit_en():
    canvas = Image.new("RGB", (1440, 1110), BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "Edit Text in a PDF", "Compare the same field before and after saving a new PDF.")
    rounded(draw, (56, 172, 1384, 524))
    text(draw, (90, 204), "Before", 31, INK, True)
    badge(draw, (1160, 198, 1338, 246), "Original PDF", "#edf3ff", BLUE)
    rounded(draw, (90, 270, 1350, 472), "#fafcff", "#b9d4fd", 8, 2)
    text(draw, (230, 310), "Customer:  Northstar Technology Ltd.", 33, INK)
    text(draw, (230, 360), "Reference:  PDF-2026-0520", 30, INK)
    text(draw, (230, 408), "Contact: service@example.com", 30, INK)
    text(draw, (598, 548), "Replace and save", 25, GREEN, True)
    draw.line((690, 586, 690, 626), fill=GREEN, width=7)
    draw.polygon(((690, 650), (673, 622), (707, 622)), fill=GREEN)
    rounded(draw, (56, 678, 1384, 1030), "#ffffff", "#9bdacb", 14, 2)
    text(draw, (90, 710), "After", 31, INK, True)
    badge(draw, (1176, 704, 1338, 752), "New PDF", "#def5eb", GREEN)
    rounded(draw, (90, 776, 1350, 978), "#f5fdf9", "#73c9b3", 8, 2)
    text(draw, (230, 816), "Customer:  Brightpath Trading Ltd.", 33, INK)
    text(draw, (230, 866), "Reference:  PDF-2026-0520", 30, INK)
    text(draw, (230, 914), "Contact: service@example.com", 30, INK)
    badge(draw, (504, 1052, 936, 1098), "Only selected text is changed", "#def5eb", GREEN)
    canvas.save(OUT_DIR / "demo_text_edit_en.png", quality=96)


def create_pdf_to_images_en():
    canvas = Image.new("RGB", (1440, 1110), BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "PDF to Images", "Export a 3-page PDF as three independent PNG image files.")
    rounded(draw, (56, 174, 1384, 448))
    text(draw, (86, 200), "Input PDF", 29, INK, True)
    badge(draw, (1192, 196, 1338, 242), "3 pages", "#fce9e6", ORANGE)
    text(draw, (86, 258), "customer_report.pdf", 24, MUTED)
    preview_page(draw, (750, 202, 952, 422), "Report - Page 1", ["Summary", "Account details"])
    preview_page(draw, (960, 202, 1162, 422), "Report - Page 2", ["Schedule", "Approvals"])
    text(draw, (606, 471), "Export PNG", 25, GREEN, True)
    draw.line((515, 515, 925, 515), fill=GREEN, width=7)
    draw.polygon(((925, 515), (899, 498), (899, 532)), fill=GREEN)
    rounded(draw, (56, 560, 1384, 1050))
    text(draw, (86, 590), "Output folder", 29, INK, True)
    badge(draw, (1160, 586, 1338, 632), "PNG x 3", "#def5eb", GREEN)
    text(draw, (86, 648), "customer_report_images\\", 22, MUTED)
    boxes = [(122, 704, 480, 984), (540, 704, 898, 984), (958, 704, 1316, 984)]
    titles = ["Page 1", "Page 2", "Page 3"]
    for index, (box, title) in enumerate(zip(boxes, titles), start=1):
        preview_page(draw, box, f"Report - {title}", ["Document content", "Ready to share"])
        text(draw, (box[0] + 100, box[3] - 44), f"page_{index:03d}.png", 22, BLUE, True)
    badge(draw, (450, 1066, 990, 1106), "One independent image per page", "#def5eb", GREEN)
    canvas.save(OUT_DIR / "demo_pdf_to_images_en.png", quality=96)


def create_watermark_en():
    canvas = Image.new("RGB", (1440, 840), BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "Batch Watermark", "Add a visible ownership mark while keeping the page readable.")
    rounded(draw, (56, 176, 618, 770))
    text(draw, (84, 202), "Original PDF", 25, INK, True)
    badge(draw, (438, 198, 576, 238), "Clean", "#edf3ff", BLUE)
    preview_page(draw, (116, 278, 556, 680), "Internal Report", ["Project summary", "Review material", "Budget notes"])
    arrow(draw, (650, 462), (774, 462), "Add watermark")
    rounded(draw, (808, 176, 1384, 770))
    text(draw, (838, 202), "Processed PDF", 25, INK, True)
    badge(draw, (1164, 198, 1340, 238), "Tiled", "#def5eb", GREEN)
    preview_page(draw, (870, 278, 1320, 680), "Internal Report", ["Project summary", "Review material", "Budget notes"], "CONFIDENTIAL")
    text(draw, (942, 704), "Readable content + clear mark", 18, GREEN, True)
    canvas.save(OUT_DIR / "demo_watermark_en.png", quality=96)


def create_merge_split_en():
    canvas = Image.new("RGB", CANVAS, BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "Merge / Split PDFs", "Input and output quantities are visible before you process files.")
    rounded(draw, (56, 180, 694, 770))
    text(draw, (84, 206), "Split PDF", 28, INK, True)
    badge(draw, (84, 262, 246, 304), "1 PDF", "#edf3ff", BLUE)
    arrow(draw, (270, 284), (374, 284), "Split")
    badge(draw, (400, 262, 628, 304), "3 page PDFs", "#def5eb", GREEN)
    preview_page(draw, (100, 352, 260, 606), "Contract", ["Page 1"])
    for i in range(3):
        preview_page(draw, (310 + i * 112, 380, 404 + i * 112, 536), f"Page {i + 1}", [])
        text(draw, (310 + i * 112, 560), f"{i + 1}.pdf", 15, BLUE, True)
    text(draw, (84, 690), "contract.pdf  ->  page_001.pdf, page_002.pdf, page_003.pdf", 17, MUTED)
    rounded(draw, (746, 180, 1384, 770))
    text(draw, (774, 206), "Merge PDFs", 28, INK, True)
    badge(draw, (774, 262, 1002, 304), "3 page PDFs", "#edf3ff", BLUE)
    arrow(draw, (1024, 284), (1126, 284), "Merge")
    badge(draw, (1144, 262, 1338, 304), "1 PDF", "#def5eb", GREEN)
    for i in range(3):
        preview_page(draw, (792 + i * 112, 380, 886 + i * 112, 536), f"Page {i + 1}", [])
    preview_page(draw, (1170, 344, 1314, 586), "Merged", ["Pages 1-3"])
    text(draw, (1176, 608), "merged.pdf", 17, GREEN, True)
    text(draw, (774, 690), "page_001.pdf + page_002.pdf + page_003.pdf  ->  merged.pdf", 17, MUTED)
    canvas.save(OUT_DIR / "demo_merge_split_en.png", quality=96)


def create_pdf_to_word_en():
    canvas = Image.new("RGB", CANVAS, BG)
    draw = ImageDraw.Draw(canvas)
    header(draw, "PDF to Word", "Turn text-based PDF content into an editable DOCX document.")
    rounded(draw, (56, 176, 608, 770))
    text(draw, (84, 202), "Input PDF", 25, INK, True)
    preview_page(draw, (144, 284, 516, 656), "Quarterly Notes", ["Review summary", "Items for approval", "Next steps"])
    arrow(draw, (648, 462), (786, 462), "Convert")
    rounded(draw, (826, 176, 1384, 770))
    text(draw, (854, 202), "Output Word", 25, INK, True)
    rounded(draw, (902, 270, 1308, 678), "#ffffff", "#b9d4fd", 8, 2)
    draw.rectangle((902, 270, 1308, 332), fill=BLUE)
    text(draw, (1034, 286), "Word document", 25, "#ffffff", True)
    text(draw, (934, 374), "Quarterly Notes", 28, INK, True)
    text(draw, (934, 432), "Review summary", 21, MUTED)
    text(draw, (934, 472), "Items for approval", 21, MUTED)
    text(draw, (934, 512), "Next steps", 21, MUTED)
    badge(draw, (964, 610, 1248, 654), "Editable DOCX output", "#def5eb", GREEN)
    canvas.save(OUT_DIR / "demo_pdf_to_word_en.png", quality=96)


def create_gumroad_assets():
    canvas = Image.new("RGB", (1280, 720), "#f4f7fa")
    draw = ImageDraw.Draw(canvas)
    badge(draw, (58, 46, 202, 88), "WINDOWS", "#def5eb", GREEN)
    text(draw, (58, 118), "Doclira PDF", 62, INK, True)
    text(draw, (58, 197), "Practical PDF tools for everyday work", 28, MUTED)
    text(draw, (58, 260), "Edit short text  |  Watermark  |  Convert  |  Organize", 21, GREEN, True)
    rounded(draw, (58, 338, 1222, 484), "#ffffff", "#b9d4fd", 10, 2)
    badge(draw, (84, 367, 194, 407), "Before", "#edf3ff", BLUE)
    text(draw, (230, 365), "Customer:  Northstar Technology Ltd.", 29, INK)
    rounded(draw, (58, 514, 1222, 660), "#ffffff", "#73c9b3", 10, 2)
    badge(draw, (84, 543, 194, 583), "After", "#def5eb", GREEN)
    text(draw, (230, 541), "Customer:  Brightpath Trading Ltd.", 29, INK)
    text(draw, (916, 276), "PDF -> DOCX / PNG", 21, BLUE, True)
    canvas.save(OUT_DIR / "gumroad_cover_en_1280x720.png", quality=96)

    thumb = Image.new("RGB", (600, 600), "#f4f7fa")
    thumb_draw = ImageDraw.Draw(thumb)
    thumb_draw.rounded_rectangle((48, 46, 122, 120), radius=14, fill=GREEN)
    text(thumb_draw, (71, 57), "D", 40, "#ffffff", True)
    text(thumb_draw, (48, 166), "Doclira", 64, INK, True)
    text(thumb_draw, (48, 236), "PDF", 64, INK, True)
    text(thumb_draw, (48, 326), "Windows PDF Toolkit", 25, MUTED)
    badge(thumb_draw, (48, 394, 264, 446), "PDF to Word", "#edf3ff", BLUE)
    badge(thumb_draw, (284, 394, 542, 446), "Watermark", "#def5eb", GREEN)
    badge(thumb_draw, (48, 468, 264, 520), "Edit Text", "#def5eb", GREEN)
    badge(thumb_draw, (284, 468, 542, 520), "Merge / Split", "#edf3ff", BLUE)
    thumb.save(OUT_DIR / "gumroad_thumbnail_en_600x600.png", quality=96)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    create_text_edit()
    create_pdf_to_images()
    create_page_tools()
    create_watermark()
    shutil.copyfile(OUT_DIR / "demo_text_edit_clear.png", OUT_DIR / "demo_text_edit_zh.png")
    shutil.copyfile(OUT_DIR / "demo_pdf_to_images_clear.png", OUT_DIR / "demo_pdf_to_images_zh.png")
    shutil.copyfile(OUT_DIR / "demo_merge_split_clear.png", OUT_DIR / "demo_merge_split_zh.png")
    shutil.copyfile(OUT_DIR / "demo_watermark_clear.png", OUT_DIR / "demo_watermark_zh.png")
    shutil.copyfile(OUT_DIR / "effect_pdf_to_word.png", OUT_DIR / "demo_pdf_to_word_zh.png")
    create_text_edit_en()
    create_pdf_to_images_en()
    create_watermark_en()
    create_merge_split_en()
    create_pdf_to_word_en()
    create_gumroad_assets()
    print("Generated feature previews:", OUT_DIR)


if __name__ == "__main__":
    main()
