#!/usr/bin/env python3
"""S105 - a visible AI-generation disclosure on every page, at first exposure.

A live read at S105 found "AI-powered" only inside <head> metadata on every page, and no visible
label in any page body. ICD 203 asks a product to distinguish information from judgment; the EU
AI Act Article 50(4) asks deployers to disclose AI-generated public-interest text unless a human
reviewed it under editorial responsibility. GNI publishes with no human editorial step, so the
truthful statement is exactly that. One edit in the root layout covers every page, server-side.
Binary mode, ASCII anchors (GNI-L-015), one occurrence each, all or nothing.
usage: python tools/patch_s105_disclosure.py [--apply]     (default: dry run)"""
import subprocess, sys

F = "src/app/layout.tsx"
OLD = b'      <body className="min-h-screen bg-background antialiased"><EOL>        {children}'
NEW = (b'      <body className="min-h-screen bg-background antialiased"><EOL>'
       b'        <div className="w-full border-b border-gray-800 bg-gray-950 px-3 py-1 text-center text-[11px] text-gray-400"><EOL>'
       b'          AI-generated analysis, published automatically without human editorial review. Not financial advice.<EOL>'
       b'        </div><EOL>'
       b'        {children}')

def main():
    apply = "--apply" in sys.argv
    if subprocess.run(["git", "status", "--porcelain"], capture_output=True).stdout.strip():
        print("REFUSED: tree is not clean"); return 1
    b = open(F, "rb").read()
    eol = b"\r\n" if b"\r\n" in b else b"\n"
    o, n = OLD.replace(b"<EOL>", eol), NEW.replace(b"<EOL>", eol)
    if b.count(o) != 1:
        print("REFUSED: anchor occurs %d times in %s, expected 1" % (b.count(o), F)); return 1
    if b"without human editorial review" in b:
        print("REFUSED: disclosure already present"); return 1
    print("%-24s %s" % (F, "WRITTEN" if apply else "would change (1 edit)"))
    if apply:
        open(F, "wb").write(b.replace(o, n))
        print("APPLIED 1 edit")
    else:
        print("DRY RUN - nothing written")
    return 0

if __name__ == "__main__":
    sys.exit(main())
