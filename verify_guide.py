from pathlib import Path
from html.parser import HTMLParser
import re

import fitz
from PIL import Image, ImageDraw


PDF = Path("CEH_v13_Module_18_IoT_and_OT_Hacking.pdf")
MD = Path("guide.md")
RENDER = Path("rendered")


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def normalized(value):
    return re.sub(r"\s+", " ", value).strip()


def main():
    doc = fitz.open(PDF)
    source = MD.read_text(encoding="utf-8")
    headings = [normalized(re.sub(r"^#+\s*", "", line))
                for line in source.splitlines() if line.startswith("#")]
    all_text = "\n".join(page.get_text() for page in doc)
    normalized_pdf = normalized(all_text)
    missing = [heading for heading in headings if heading not in normalized_pdf]

    content_start = 0
    for index, page in enumerate(doc):
        if "1. Module at a Glance" in page.get_text():
            content_start = index
    content_pages = []
    for page in list(doc)[content_start:]:
        text = page.get_text()
        text = text.replace("CEH v13 Module 18: IoT and OT Hacking", "")
        text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text)
        content_pages.append(text)
    pdf_words = [word for word in re.findall(r"\S+", "\n".join(content_pages))
                 if re.search(r"[A-Za-z0-9]", word)]

    html = Path("guide.html").read_text(encoding="utf-8")
    content_html = re.search(r'<main class="content">(.*)</main>', html, re.S).group(1)
    parser = TextParser()
    parser.feed(content_html)
    source_words = [word for word in re.findall(r"\S+", " ".join(parser.parts))
                    if re.search(r"[A-Za-z0-9]", word)]
    difference = abs(len(pdf_words) - len(source_words)) / len(source_words) * 100

    right_limit = doc[0].rect.width - 51.02
    overflow = []
    blank = []
    for index, page in enumerate(doc):
        if len(page.get_text().strip()) < 5:
            blank.append(index + 1)
        for word in page.get_text("words"):
            if word[2] > right_limit + 0.75:
                overflow.append((index + 1, word[4], round(word[2], 2)))

    toc = doc.get_toc()
    print(f"Pages: {len(doc)}")
    print(f"Headings: {len(headings)}, missing: {missing}")
    print(f"Content words HTML/PDF: {len(source_words)}/{len(pdf_words)}")
    print(f"Word-count difference: {difference:.3f}%")
    print(f"Right-margin overflow: {overflow[:20]}; total {len(overflow)}")
    print(f"Blank pages: {blank}")
    print(f"Bookmarks: {len(toc)}")
    print(f"Replacement characters: {all_text.count(chr(0xfffd))}")

    RENDER.mkdir(exist_ok=True)
    selected = {0, 1, 2, content_start, len(doc) - 1}
    diagram_terms = ("IoT path", "OT path", "Q: What are the five IoT",
                     "Question 14: Metasploit")
    table_terms = ("Tool Simple purpose", "Protocol Simple purpose",
                   "Attack How to recognize", "X vs Y",
                   "Page Source topics", "Keyword in question")
    code_terms = ("python -m fuzzowski", "gem install modbus-cli",
                  "./extract-firmware.sh", "modbus_findunitid")
    table_pages = []
    for index, page in enumerate(doc):
        text = normalized(page.get_text())
        if any(term in text for term in diagram_terms + code_terms):
            selected.add(index)
        if any(term in text for term in table_terms):
            table_pages.append(index)
            selected.add(index)
    print("Visual pages:", [p + 1 for p in sorted(selected)])
    for index in sorted(selected):
        pix = doc[index].get_pixmap(dpi=100, alpha=False)
        pix.save(RENDER / f"page-{index + 1:03d}.png")

    images = []
    for index in sorted(selected):
        image = Image.open(RENDER / f"page-{index + 1:03d}.png")
        image.thumbnail((620, 877))
        images.append((index + 1, image.copy()))
    for batch in range(0, len(images), 4):
        group = images[batch:batch + 4]
        sheet = Image.new("RGB", (1280, 1840), "#d9dee3")
        draw = ImageDraw.Draw(sheet)
        for position, (page_number, image) in enumerate(group):
            x = (position % 2) * 640 + 10
            y = (position // 2) * 920 + 30
            draw.text((x, y - 22), f"Page {page_number}", fill="black")
            sheet.paste(image, (x, y))
        sheet.save(RENDER / f"contact-{batch // 4 + 1:02d}.png")

    if missing or overflow or blank or difference > 3 or not toc:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
