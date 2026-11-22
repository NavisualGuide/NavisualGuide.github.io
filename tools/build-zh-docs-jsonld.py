"""Write the structured data (JSON-LD) in zh/docs.html from the page's own text.

    python tools/build-zh-docs-jsonld.py          # rewrite it in place
    python tools/build-zh-docs-jsonld.py --check  # exit 1 if it is out of date

Google requires an FAQPage's questions and answers to match what the page shows,
word for word. The English manual keeps the two in step by hand (a comment says
so); the Chinese one generates them instead, from the <h3>/<p> pairs of the
"quick answers" section (<section id="quick">), so a reworded answer cannot leave
a stale copy behind. Edit the section, then rerun this.
"""
import html
import io
import json
import re
import sys

PAGE = "zh/docs.html"
URL = "https://navisualguide.com/zh/docs.html"

src = io.open(PAGE, encoding="utf-8", newline="").read()


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


quick = re.search(r'<section id="quick">(.*?)</section>', src, re.S)
assert quick, "no <section id=\"quick\"> in " + PAGE
pairs = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", quick.group(1), re.S)
assert len(pairs) >= 5, "found only %d question/answer pairs" % len(pairs)

title = text(re.search(r"<title>(.*?)</title>", src, re.S).group(1))
desc = re.search(r'<meta name="description" content="([^"]*)"', src).group(1)
modified = re.search(r'<meta property="article:modified_time" content="([^"]*)"', src).group(1)

graph = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "TechArticle",
            "@id": URL + "#article",
            "headline": "Navisual 使用手册",
            "name": title,
            "description": html.unescape(desc),
            "url": URL,
            "mainEntityOfPage": URL,
            "inLanguage": "zh-CN",
            "datePublished": "2026-11-22",
            "dateModified": modified,
            "image": "https://navisualguide.com/social-preview.png",
            "author": {"@type": "Person", "name": "Jin Fu", "sameAs": ["https://x.com/stevefujin"]},
            "publisher": {"@type": "Organization", "name": "Navisual", "url": "https://navisualguide.com/"},
            "about": {
                "@type": "SoftwareApplication",
                "name": "Navisual",
                "url": "https://navisualguide.com/zh/",
                "applicationCategory": "UtilitiesApplication",
                "operatingSystem": "Windows 10, Windows 11",
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Navisual", "item": "https://navisualguide.com/zh/"},
                {"@type": "ListItem", "position": 2, "name": "使用手册", "item": URL},
            ],
        },
        {
            "@type": "FAQPage",
            "@id": URL + "#quick",
            "mainEntity": [
                {"@type": "Question", "name": text(q),
                 "acceptedAnswer": {"@type": "Answer", "text": text(a)}}
                for q, a in pairs
            ],
        },
    ],
}
block = json.dumps(graph, ensure_ascii=False, indent=2)
nl = "\r\n" if "\r\n" in src else "\n"  # the site's files are CRLF on Windows checkouts
block = block.replace("\n", nl)

script = re.compile(r'(<script type="application/ld\+json">\r?\n)(.*?)(\r?\n  </script>)', re.S)
m = script.search(src)
assert m, "no JSON-LD <script> block in " + PAGE
if m.group(2) == block:
    print("up to date (%d questions)" % len(pairs))
    sys.exit(0)
if "--check" in sys.argv:
    print("OUT OF DATE: run python tools/build-zh-docs-jsonld.py")
    sys.exit(1)
out = src[:m.start(2)] + block + src[m.end(2):]
io.open(PAGE, "w", encoding="utf-8", newline="").write(out)
print("wrote %d questions" % len(pairs))
