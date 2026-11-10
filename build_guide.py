from pathlib import Path
import html
import re
import sys

import markdown


SOURCE = Path("guide.md")
OUTPUT = Path("CEH_v13_Module_18_IoT_and_OT_Hacking")


def validate(source):
    lines = source.splitlines()
    errors = []
    if not source.isascii():
        errors.append("non-ASCII text present")
    if "\u2014" in source:
        errors.append("em dash present")
    if source.count("```") % 2:
        errors.append("unbalanced fences")
    for i, line in enumerate(lines, 1):
        if line.startswith("|"):
            cells = line.strip("|").split("|")
            if len(cells) > 5:
                errors.append(f"line {i}: more than five table columns")
            for cell in cells:
                if len(cell.strip()) > 60:
                    errors.append(f"line {i}: long table cell")
    in_code = False
    code_lang = ""
    for i, line in enumerate(lines, 1):
        if line.startswith("```"):
            if not in_code:
                code_lang = line[3:].strip()
                if not code_lang:
                    errors.append(f"line {i}: missing code language")
            in_code = not in_code
            continue
        if in_code and len(line) > 76:
            errors.append(f"line {i}: code line over 76 characters")
    sections = re.findall(r"^## (\d+)\.", source, re.M)
    if sections != [str(i) for i in range(1, 13)]:
        errors.append(f"required sections missing or out of order: {sections}")
    for placeholder in ("TODO", "TBD", "Lorem ipsum", "PLACEHOLDER"):
        if placeholder in source:
            errors.append(f"placeholder: {placeholder}")
    return errors


CSS = r"""
@page {
  size: A4;
  margin: 18mm;
  @bottom-left {
    content: "CEH v13 Module 18: IoT and OT Hacking";
    font-family: "DejaVu Sans";
    font-size: 8pt;
    color: #536273;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-family: "DejaVu Sans";
    font-size: 8pt;
    color: #536273;
  }
}
@page title {
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}
html { font-family: "DejaVu Sans"; font-size: 11pt; line-height: 1.5; }
body { color: #1d2733; background: white; }
h1, h2, h3 { color: #123c63; line-height: 1.25; break-after: avoid; }
h1 { font-size: 24pt; margin: 0 0 8mm; }
h2 { font-size: 17pt; border-bottom: 2px solid #2c6e9e;
  padding-bottom: 2mm; margin-top: 8mm; }
h3 { font-size: 13pt; margin-top: 6mm; }
p, ul, ol { margin: 2mm 0 3mm; orphans: 3; widows: 3; }
li { margin-bottom: 1mm; }
a { color: #185b8c; text-decoration: none; }
pre {
  font-family: "DejaVu Sans Mono";
  font-size: 8.5pt;
  line-height: 1.35;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: #f3f5f7;
  border: 0.4pt solid #b9c3cc;
  border-radius: 3px;
  padding: 3mm;
  margin: 3mm 0;
  break-inside: avoid;
}
code { font-family: "DejaVu Sans Mono"; font-size: 8.5pt;
  overflow-wrap: anywhere; background: #f3f5f7; }
pre code { background: transparent; padding: 0; }
table { width: 100%; table-layout: fixed; border-collapse: collapse;
  font-size: 9.5pt; margin: 3mm 0 4mm; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { background: #e4edf4; color: #123c63; font-weight: bold; }
th, td { border: 0.4pt solid #9eabb7; padding: 1.6mm;
  vertical-align: top; overflow-wrap: anywhere; }
blockquote { margin: 3mm 0; padding: 2.5mm 3mm; background: #eef5fa;
  border-left: 3pt solid #2878aa; break-inside: avoid; }
blockquote:has(strong) { border-left-color: #2878aa; }
blockquote p { margin: 0; }
.title-page { page: title; height: 245mm; display: flex;
  flex-direction: column; justify-content: center; text-align: center; }
.title-page .course { color: #2878aa; font-size: 15pt; font-weight: bold; }
.title-page .module { color: #123c63; font-size: 30pt; line-height: 1.2;
  font-weight: bold; margin: 8mm 0; }
.title-page .subtitle { color: #536273; font-size: 13pt; }
.title-page .meta { margin-top: 20mm; color: #536273; font-size: 10pt; }
.toc { break-after: page; }
.toc h1 { font-size: 22pt; }
.toc ul { list-style: none; padding-left: 0; }
.toc ul ul { padding-left: 5mm; }
.toc li { margin: 1mm 0; }
.toc a::after { content: leader('.') target-counter(attr(href), page);
  color: #536273; }
.content > h1 { display: none; }
.content > h2 { break-before: page; }
.content > h2:first-of-type { break-before: auto; }
"""


def build():
    source = SOURCE.read_text(encoding="utf-8")
    errors = validate(source)
    if errors:
        print("\n".join(errors))
        return 1
    md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"],
                           extension_configs={"toc": {"toc_depth": "2-3"}})
    content = md.convert(source)
    toc = md.toc
    title = """
<section class="title-page">
  <div class="course">CEH v13 AI | Exam 312-50</div>
  <div class="module">Module 18<br>IoT and OT Hacking</div>
  <div class="subtitle">Complete Exam-Focused Study Guide</div>
  <div class="meta">Based on 39 supplied note pages<br>
  Includes commands, tools, practice questions, and flashcards</div>
</section>
"""
    document = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(OUTPUT.stem)}</title>
<style>{CSS}</style></head><body>{title}
<section class="toc"><h1>Table of Contents</h1>{toc}</section>
<main class="content">{content}</main></body></html>"""
    Path("guide.html").write_text(document, encoding="utf-8")
    from weasyprint import HTML
    HTML(string=document, base_url=str(Path.cwd())).write_pdf(
        OUTPUT.with_suffix(".pdf"))
    print(f"Built {OUTPUT.with_suffix('.pdf')}")
    print(f"Markdown words: {len(re.findall(r'\S+', source))}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
