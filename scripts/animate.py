#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 google-raffle contributors
"""Encode square animation frames or a regular sprite sheet as a looping LED GIF."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps, ImageSequence

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("files", nargs="+", type=Path, help="Frame images in playback order, or one GIF")
    p.add_argument("--grid", type=int, help="Split one square sheet into N×N cells, left-to-right, top-to-bottom")
    p.add_argument("--name", default="animation")
    p.add_argument("--duration", type=int, default=160, help="Milliseconds per frame, multiple of 10 (default 160)")
    p.add_argument("--smooth", action="store_true")
    p.add_argument("--black-threshold", type=int, default=12, help="Clamp pixels whose brightest channel is at most this value to true black (default 12)")
    a = p.parse_args()
    if not 0 <= a.black_threshold <= 255:
        p.error("Black threshold must be between 0 and 255.")
    if Path(a.name).name != a.name or a.name in {"", ".", ".."}:
        p.error("Name must be a filename without directory components.")
    if a.duration < 40 or a.duration > 2000 or a.duration % 10:
        p.error("Duration must be 40–2000 ms and a multiple of 10.")
    if a.grid is not None and (not 2 <= a.grid <= 8 or len(a.files) != 1):
        p.error("Grid needs exactly one sheet and a grid size from 2 to 8.")
    originals = []
    records = []
    for source in a.files:
        try:
            with Image.open(source) as image:
                records.append({"file": source.name, "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
                if a.grid:
                    if image.width != image.height or image.width % a.grid:
                        p.error("Sheet must be square and divisible by the grid size.")
                    side = image.width // a.grid
                    for y in range(a.grid):
                        for x in range(a.grid):
                            originals.append(image.crop((x * side, y * side, (x + 1) * side, (y + 1) * side)).convert("RGBA"))
                else:
                    originals.extend(ImageOps.exif_transpose(frame.copy()).convert("RGBA") for frame in ImageSequence.Iterator(image))
        except (OSError, ValueError) as exc:
            p.error(f"Cannot read {source}: {exc}")
    if not 2 <= len(originals) <= 240:
        p.error("Provide 2–240 frames. A single still image is not an animation.")
    frames = []
    method = Image.Resampling.LANCZOS if a.smooth else Image.Resampling.NEAREST
    for frame in originals:
        if frame.width != frame.height:
            p.error("All frames must be square; compose them to square before encoding.")
        base = Image.new("RGBA", frame.size, (0, 0, 0, 255))
        rgb = Image.alpha_composite(base, frame).convert("RGB").resize((64, 64), method)
        rgb.putdata([(0, 0, 0) if max(pixel) <= a.black_threshold else pixel for pixel in rgb.get_flattened_data()])
        frames.append(rgb)
    # One shared palette keeps colors stable across the animation.
    strip = Image.new("RGB", (64, 64 * len(frames)))
    for n, frame in enumerate(frames):
        strip.paste(frame, (0, n * 64))
    palette = strip.quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    # Quantization may merge black into a near-black cluster; restore LED off-state.
    pal = palette.getpalette()
    for n in range(0, len(pal), 3):
        if max(pal[n:n + 3]) <= a.black_threshold:
            pal[n:n + 3] = [0, 0, 0]
    for frame in indexed:
        frame.putpalette(pal)
    output = ROOT / "artwork/submission"
    previews = ROOT / "artwork/previews"
    output.mkdir(parents=True, exist_ok=True)
    previews.mkdir(parents=True, exist_ok=True)
    dest = output / f"{a.name}-64.gif"
    indexed[0].save(dest, save_all=True, append_images=indexed[1:], duration=a.duration,
                    loop=0, disposal=2, optimize=False)
    with Image.open(dest) as checked:
        if checked.size != (64, 64) or checked.n_frames < 2 or dest.stat().st_size > 5_000_000:
            p.error("Result must contain visible motion, be 64×64, and stay below 5 MB.")
        encoded_frames = checked.n_frames
        encoded_duration = sum(f.info.get("duration", 0) for f in ImageSequence.Iterator(checked))
    large = [frame.resize((512, 512), Image.Resampling.NEAREST) for frame in indexed]
    preview = previews / f"{a.name}-preview.gif"
    large[0].save(preview, save_all=True, append_images=large[1:], duration=a.duration,
                  loop=0, disposal=2, optimize=False)
    cols = min(8, len(indexed))
    contact = Image.new("RGB", (cols * 128, ((len(indexed) + cols - 1) // cols) * 128))
    for n, frame in enumerate(indexed):
        contact.paste(frame.resize((128, 128), Image.Resampling.NEAREST), ((n % cols) * 128, (n // cols) * 128))
    contact.save(previews / f"{a.name}-frames.png")
    manifest = {"sources": records, "grid": a.grid, "input_frames": len(frames),
                "encoded_frames": encoded_frames, "loop_ms": encoded_duration, "frame_duration_ms": a.duration,
                "output": dest.name, "bytes": dest.stat().st_size, "size": [64, 64],
                "palette_colors": 128, "resize": "lanczos" if a.smooth else "nearest", "loop": "forever"}
    black_counts = [sum(pixel == (0, 0, 0) for pixel in frame.convert("RGB").get_flattened_data()) for frame in indexed]
    manifest["black_threshold"] = a.black_threshold
    manifest["true_black_percent_mean"] = round(100 * sum(black_counts) / (4096 * len(indexed)), 2)
    (output / f"{a.name}-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Upload: {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes, {encoded_frames} frames, {encoded_duration / 1000:.2f}s loop)")
    print(f"Preview: {preview.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
