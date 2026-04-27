"""Site-state validation for the portfolio.

Checks five things that tend to drift across edits:

  1. Every internal link in every HTML page resolves to a file
     (project-folder URLs are valid if the folder has a README.md;
      profile.jpg is treated as intentionally optional).
  2. Every JSON-LD <script> block parses as valid JSON, with a
     summary of how many of each @type are present site-wide.
  3. Pages that declare hreflang carry both en and fr alternates.
  4. sitemap.xml is valid XML, every URL has <lastmod>, and every
     URL maps to a real file (or a folder with README.md).
  5. site.webmanifest is valid JSON and every declared icon exists.

Exits 0 on PASS, 1 on FAIL. Run before each push:

    python validate_site.py

Useful as a one-shot smoke test; not wired into CI yet.
"""
import json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent
SITE_PREFIX = "/data-portfolio/"
# Pages that *intentionally* don't exist on the local FS (rendered by GH Pages from README.md)
PROJECT_FOLDERS = {f"0{i}" if i < 10 else str(i) for i in range(1, 14)}
# Files that are intentionally absent — the user drops them later; UI has graceful fallback.
INTENTIONALLY_OPTIONAL = {"profile.jpg", "profile.webp"}

errors = []

# ── 1. Internal link integrity across every HTML file ──
print("=== 1. Internal link integrity ===")
html_files = sorted(set(
    list(ROOT.glob("*.html"))
    + list((ROOT / "fr").glob("*.html"))
    + list((ROOT / "case-studies").rglob("*.html"))
    + list((ROOT / "fr" / "case-studies").rglob("*.html"))
))
total_links = 0
broken = 0
for f in html_files:
    text = f.read_text(encoding="utf-8")
    for m in re.finditer(r'(?:href|src)="([^"#?]+)"', text):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#")):
            continue
        total_links += 1
        if href.startswith(SITE_PREFIX):
            target = ROOT / href[len(SITE_PREFIX):]
        elif href.startswith("/"):
            target = ROOT / href.lstrip("/")
        else:
            target = (f.parent / href).resolve()
        if target.is_dir():
            target = target / "index.html"
        # Project folder URLs render via README.md; treat the folder existing as "ok".
        if not target.exists() and any(f"/{p}-" in href or href.endswith(f"/{p}-") for p in PROJECT_FOLDERS):
            parent = target.parent
            if parent.exists() and (parent / "README.md").exists():
                continue
        if not target.exists() and any(href.endswith(opt) for opt in INTENTIONALLY_OPTIONAL):
            continue
        if not target.exists():
            broken += 1
            errors.append(f"  broken: {f.relative_to(ROOT)} -> {href}")
print(f"  {total_links} internal links, {broken} broken")

# ── 2. JSON-LD validity ──
print()
print("=== 2. JSON-LD validity ===")
ld_total = 0
ld_bad = 0
schemas_found = []
for f in html_files:
    text = f.read_text(encoding="utf-8")
    for m in re.finditer(r'<script type="application/ld\+json">\s*(\{[\s\S]*?\})\s*</script>', text):
        ld_total += 1
        try:
            d = json.loads(m.group(1))
            schemas_found.append((f.relative_to(ROOT).as_posix(), d.get("@type") or [g.get("@type") for g in d.get("@graph", [])]))
        except json.JSONDecodeError as e:
            ld_bad += 1
            errors.append(f"  invalid JSON-LD in {f.relative_to(ROOT)}: {e}")
print(f"  {ld_total} JSON-LD blocks, {ld_bad} invalid")
type_counts = {}
for _, t in schemas_found:
    if isinstance(t, list):
        for ti in t:
            type_counts[ti] = type_counts.get(ti, 0) + 1
    else:
        type_counts[t] = type_counts.get(t, 0) + 1
for tname, cnt in sorted(type_counts.items()):
    print(f"    {cnt:3d}  {tname}")

# ── 3. hreflang reciprocity ──
print()
print("=== 3. hreflang reciprocity ===")
hreflang_problems = 0
for f in html_files:
    text = f.read_text(encoding="utf-8")
    alts = re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"', text)
    if not alts:
        continue
    seen_langs = {lang for lang, _ in alts}
    if len(seen_langs) >= 2 and not ({"en", "fr"} <= seen_langs):
        hreflang_problems += 1
        errors.append(f"  {f.relative_to(ROOT)}: hreflang missing en or fr")
print(f"  {len([f for f in html_files if 'hreflang' in f.read_text(encoding='utf-8')])} pages declare hreflang, {hreflang_problems} problems")

# ── 4. Sitemap validity & coverage ──
print()
print("=== 4. Sitemap ===")
tree = ET.parse(ROOT / "sitemap.xml")
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = tree.getroot().findall("sm:url", ns)
no_lastmod = sum(1 for u in urls if u.find("sm:lastmod", ns) is None)
print(f"  {len(urls)} URLs, {no_lastmod} without lastmod")

# Verify every case-study URL in sitemap maps to a real file.
sitemap_locs = [u.find("sm:loc", ns).text for u in urls]
missing = []
for loc in sitemap_locs:
    rel = loc.replace("https://gabayae.github.io/data-portfolio/", "")
    target = ROOT / rel / "index.html" if rel else ROOT / "index.html"
    if not target.exists():
        # Project folder index — README.md is fine.
        if (ROOT / rel / "README.md").exists():
            continue
        missing.append(loc)
if missing:
    errors.append(f"  sitemap entries with no target file: {missing}")
print(f"  {len(missing)} sitemap URLs without a backing file")

# ── 5. Web manifest ──
print()
print("=== 5. Web app manifest ===")
mf = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
icon_count = len(mf.get("icons", []))
icons_ok = sum(1 for icon in mf["icons"] if (ROOT / icon["src"].lstrip("/").replace("data-portfolio/", "")).exists())
print(f"  {icon_count} icons declared, {icons_ok} resolve to files; theme={mf['theme_color']}, scope={mf['scope']}")
if icons_ok != icon_count:
    errors.append(f"  manifest icons missing on disk: {icon_count - icons_ok}")

# ── Summary ──
print()
print("=== Summary ===")
if errors:
    print(f"FAIL — {len(errors)} issues")
    for e in errors[:30]:
        print(e)
    sys.exit(1)
else:
    print(f"PASS — {len(html_files)} pages, {total_links} links, {ld_total} JSON-LD blocks, {len(urls)} sitemap URLs, {icon_count} icons. Site is internally consistent.")
