#!/usr/bin/env python3
"""Prepare up to three static images for the Devoxx LED raffle."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--crop", action="store_true", help="Center-crop non-square sources")
    parser.add_argument("--smooth", action="store_true", help="Use Lanczos for painted art rather than nearest-neighbor for pixel art")
    args = parser.parse_args()
    files = args.files or sorted(p for p in (ROOT / "artwork/raw").iterdir()
                                 if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp"})
    if not 1 <= len(files) <= 3:
        parser.error("Put 1–3 chosen static images in artwork/raw/, or pass 1–3 file paths.")
    if len({p.stem for p in files}) != len(files):
        parser.error("Use different filenames for each chosen image.")
    prepared = []
    for source in files:
        try:
            with Image.open(source) as opened:
                if getattr(opened, "n_frames", 1) != 1:
                    parser.error(f"{source}: animated files need a separate animation workflow.")
                original_size = list(opened.size)
                im = ImageOps.exif_transpose(opened).convert("RGBA")
                if im.width != im.height:
                    if not args.crop:
                        parser.error(f"{source}: must be square; regenerate square or explicitly use --crop.")
                    side = min(im.size)
                    x, y = (im.width - side) // 2, (im.height - side) // 2
                    im = im.crop((x, y, x + side, y + side))
                background = Image.new("RGBA", im.size, (0, 0, 0, 255))
                im = Image.alpha_composite(background, im).convert("RGB")
                method = Image.Resampling.LANCZOS if args.smooth else Image.Resampling.NEAREST
                prepared.append((source, original_size, im.resize((64, 64), method)))
        except (OSError, ValueError) as exc:
            parser.error(f"Cannot read {source}: {exc}")
    output = ROOT / "artwork/submission"
    previews = ROOT / "artwork/previews"
    output.mkdir(parents=True, exist_ok=True)
    previews.mkdir(parents=True, exist_ok=True)
    records = []
    for source, original_size, im in prepared:
        dest = output / f"{source.stem}-64.png"
        im.save(dest, optimize=True)
        with Image.open(dest) as checked:
            if checked.size != (64, 64) or dest.stat().st_size > 5_000_000:
                raise RuntimeError(f"Output failed raffle validation: {dest}")
        preview = previews / f"{source.stem}-preview.png"
        im.resize((512, 512), Image.Resampling.NEAREST).save(preview)
        records.append({"source": source.name, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                        "original_size": original_size, "output": dest.name, "size": [64, 64],
                        "bytes": dest.stat().st_size, "center_crop": args.crop,
                        "resize": "lanczos" if args.smooth else "nearest", "transparent_background": "black"})
        print(f"Upload: {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes)")
        print(f"Preview: {preview.relative_to(ROOT)}")
    (output / "manifest.json").write_text(json.dumps(records, indent=2) + "\n")
    print("Upload only the PNGs named above, not the previews or manifest. Older outputs are retained.")


if __name__ == "__main__":
    main()
