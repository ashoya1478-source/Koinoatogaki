from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import json, tempfile, shutil

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "site-bundle"
MANIFEST = json.loads((BUNDLE / "manifest.json").read_text(encoding="utf-8"))
if MANIFEST.get("format") != "split-zip-v1":
    raise SystemExit("Unsupported site bundle format")

with tempfile.TemporaryFile() as archive:
    whole = sha256()
    for part in MANIFEST["parts"]:
        path = BUNDLE / part["name"]
        data_hash = sha256()
        count = 0
        with path.open("rb") as source:
            while chunk := source.read(1024 * 1024):
                archive.write(chunk)
                whole.update(chunk)
                data_hash.update(chunk)
                count += len(chunk)
        if count != part["bytes"] or data_hash.hexdigest() != part["sha256"]:
            raise SystemExit(f"Archive part failed verification: {part['name']}")
    if whole.hexdigest() != MANIFEST["sha256"]:
        raise SystemExit("Complete archive failed SHA-256 verification")
    archive.seek(0)
    output = ROOT / "dist"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    with ZipFile(archive) as site:
        base = output.resolve()
        for info in site.infolist():
            target = (output / info.filename).resolve()
            if target != base and base not in target.parents:
                raise SystemExit(f"Unsafe path in archive: {info.filename}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with site.open(info) as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
# Optional edits can be placed here; they are copied over the verified snapshot.
OVERLAYS = ROOT / "site-overrides"
if OVERLAYS.exists():
    for source in OVERLAYS.rglob("*"):
        if source.is_file() and source.name != ".gitkeep":
            relative = source.relative_to(OVERLAYS)
            target = ROOT / "dist" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

if not (ROOT / "dist" / "index.html").is_file():
    raise SystemExit("Built site is missing dist/index.html")
print(f"Restored and verified {MANIFEST['files']} site files to dist/")
