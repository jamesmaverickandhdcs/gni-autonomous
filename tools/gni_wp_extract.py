#!/usr/bin/env python3
"""tools/gni_wp_extract.py - S107, DECISION S107-2. Freezes the March 2026
White Paper into the repo as verbatim text, so roadmap 3 row R3-2 can harvest
its claims with file:line.

  python tools/gni_wp_extract.py <path-to-.docx> docs/GNI_WHITE_PAPER_S107.md

SOURCE CHOICE (measured S107): the .docx is the source and the .pdf a render of
it - the pdf's mtime is 20 s later, and the two texts differ only where the pdf
fused a word across a line-break hyphen (7 fusions, 0 other differences).

ONE PARAGRAPH PER LINE, ON PURPOSE: a claim quoted from this file resolves at a
file:line only if no paragraph is wrapped across lines. A table row becomes one
line, its cells joined by ' | '. Text is never edited: no wrapping, no
re-casing, no smart-quote folding. stdlib only (item 6.9).

The output is FROZEN - written once, at S107, never regenerated. Its stamp
records the source md5 so anyone holding the .docx can reproduce it byte for
byte. EXIT: 0 written, 2 instrument error (missing input, empty extraction).
"""
import hashlib
import html
import re
import sys
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
BODY_RE = re.compile(r"<w:body>(.*)</w:body>", re.S)
BLOCK_RE = re.compile(r"<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>|<w:p/>", re.S)
ROW_RE = re.compile(r"<w:tr[ >].*?</w:tr>", re.S)
CELL_RE = re.compile(r"<w:tc>.*?</w:tc>", re.S)
PARA_RE = re.compile(r"<w:p[ >].*?</w:p>", re.S)
RUN_RE = re.compile(r"<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:(tab|br)/>")


def para_text(xml):
    out = []
    for txt, tag in RUN_RE.findall(xml):
        out.append(" " if tag else html.unescape(txt))
    return "".join(out).strip()


def extract(xml):
    m = BODY_RE.search(xml)
    if not m:
        raise SystemExit("INSTRUMENT ERROR: no <w:body> in document.xml")
    lines = []
    for block in BLOCK_RE.findall(m.group(1)):
        if block.startswith("<w:tbl>"):
            for row in ROW_RE.findall(block):
                cells = [" ".join(t for t in map(para_text, PARA_RE.findall(c)) if t)
                         for c in CELL_RE.findall(row)]
                if any(cells):
                    lines.append("| " + " | ".join(cells) + " |")
        else:
            t = para_text(block)
            if t:
                lines.append(t)
    return lines


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    src, dst = argv[1], argv[2]
    try:
        raw = open(src, "rb").read()
        xml = zipfile.ZipFile(src).read("word/document.xml").decode("utf-8")
    except (OSError, KeyError, zipfile.BadZipFile) as exc:
        print("INSTRUMENT ERROR: %s" % exc)
        return 2
    lines = extract(xml)
    if not lines:
        print("INSTRUMENT ERROR: empty extraction from " + src)
        return 2
    head = [
        "# GNI WHITE PAPER - March 2026 - FROZEN TEXT (entered at S107)",
        "",
        "FROZEN by `tools/gni_wp_extract.py`. Never hand-edited, never regenerated.",
        "SOURCE `GNI_White_Paper_Autonomous_Vision.docx` md5 `%s`, %d bytes."
        % (hashlib.md5(raw).hexdigest(), len(raw)),
        "BODY one paragraph per line, %d lines, verbatim; a table row is one line." % len(lines),
        "",
        "---",
        "",
    ]
    with open(dst, "wb") as fh:
        fh.write(("\n".join(head + lines) + "\n").encode("utf-8"))
    print("wrote %s: %d body lines from %s" % (dst, len(lines), src))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
