"""Assemble only the reviewed Orbital website into a standalone Pages root."""
from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path

SOURCE = Path("source/demo/projects/orbital")
TARGET = Path("public")
PROJECTS_URL = "https://maharshimak.github.io/makma-ai-os/projects/"
AI_OS_URL = "https://maharshimak.github.io/makma-ai-os/"

if not (SOURCE / "index.html").is_file():
    raise SystemExit("Source Orbital page missing: pinned source commit changed.")

if TARGET.exists():
    shutil.rmtree(TARGET)
shutil.copytree(SOURCE, TARGET)
page = TARGET / "index.html"
html = page.read_text(encoding="utf-8")

# The standalone preview must link to the genuine, existing MAK'MA systems.
html = html.replace('href="../../"', f'href="{AI_OS_URL}"')
html = re.sub(
    r'href="\.\./([^"#]*)"',
    lambda match: f'href="{PROJECTS_URL}{match.group(1)}"',
    html,
)
html = html.replace(
    '<meta charset="utf-8">',
    '<meta charset="utf-8">\n  <meta name="robots" content="noindex, nofollow">',
    1,
)
for name in ("style.css", "app.js", "orbital-3d.js"):
    asset = TARGET / name
    if not asset.is_file():
        raise SystemExit(f"Missing preview asset: {name}")
    digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
    html = html.replace(f'"./{name}"', f'"./{name}?v={digest}"')

required = [TARGET / "assets" / f"{scene}.png" for scene in ("orbit", "network", "datacenter", "core")]
if any(not path.is_file() for path in required):
    raise SystemExit("Missing cinematic image asset")
if html.count(PROJECTS_URL) < 8:
    raise SystemExit("Unexpected project link count; refusing partial preview")
page.write_text(html, encoding="utf-8")
print("Prepared standalone Orbital preview with original images, 3D renderer and linked projects.")
