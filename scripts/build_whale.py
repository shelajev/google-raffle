#!/usr/bin/env python3
"""Animate the Nano Banana Pro keyframe using deterministic native-grid layers."""
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artwork/raw/whale-pro-keyframe.png"


def connected_parts(im):
    pixels = im.load()
    remaining = {(x, y) for y in range(im.height) for x in range(im.width)
                 if max(pixels[x, y]) > 40}
    parts = []
    while remaining:
        seed = remaining.pop()
        stack = [seed]
        component = [seed]
        while stack:
            x, y = stack.pop()
            for pos in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if pos in remaining:
                    remaining.remove(pos)
                    stack.append(pos)
                    component.append(pos)
        if len(component) >= 250:
            parts.append(component)
    return parts


def main():
    original = Image.open(SOURCE).convert("RGB")
    if original.size != (1024, 1024):
        raise ValueError("This extraction is calibrated for the recorded 1024×1024 Pro keyframe.")
    hero = Image.new("RGBA", original.size)
    moon = Image.new("RGBA", original.size)
    cargo = Image.new("RGBA", original.size)
    for part in connected_parts(original):
        xs, ys = zip(*part)
        box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
        if box[0] > 690 and box[3] < 300:
            target = moon
        elif box[1] >= 820:
            continue
        elif box[0] >= 320 and box[2] <= 480 and 280 <= box[1] <= 320 and box[3] < 390:
            target = cargo
        elif box[3] < 820 and len(part) > 1500:
            target = hero
        else:
            continue
        for x, y in part:
            target.putpixel((x, y), (*original.getpixel((x, y)), 255))
    if not cargo.getbbox() or not hero.getbbox() or not moon.getbbox():
        raise ValueError("Required source layers were not identified.")
    bounds = hero.getbbox()
    scale = 43 / (bounds[2] - bounds[0])
    size = (43, round((bounds[3] - bounds[1]) * scale))
    sprite = hero.crop(bounds).resize(size, Image.Resampling.NEAREST)
    cargo_bounds = cargo.getbbox()
    box_sprite = cargo.crop(cargo_bounds).resize((max(1, round((cargo_bounds[2] - cargo_bounds[0]) * scale)),
                                                 max(1, round((cargo_bounds[3] - cargo_bounds[1]) * scale))), Image.Resampling.NEAREST)
    cargo_offset = (round((cargo_bounds[0] - bounds[0]) * scale), round((cargo_bounds[1] - bounds[1]) * scale))
    moon_sprite = moon.crop(moon.getbbox()).resize((8, 8), Image.Resampling.NEAREST)
    assets = ROOT / "artwork/layers"
    assets.mkdir(parents=True, exist_ok=True)
    sprite.save(assets / "whale-pro.png")
    box_sprite.save(assets / "launch-container.png")
    moon_sprite.save(assets / "moon.png")
    frame_dir = ROOT / "artwork/frames/ship-it"
    frame_dir.mkdir(parents=True, exist_ok=True)
    # Bitmap text keeps letter positions stable; no font smoothing or fractional coordinates.
    font = ImageFont.load_default_imagefont()
    for n in range(60):
        t = n / 60
        frame = Image.new("RGBA", (64, 64), (0, 0, 0, 255))
        draw = ImageDraw.Draw(frame)
        frame.alpha_composite(moon_sprite, (51, 10))
        for i, (x, y) in enumerate(((5, 13), (15, 20), (42, 12), (59, 29))):
            color = (220, 255, 255) if math.sin(2 * math.pi * t + i * 1.5) > 0 else (60, 140, 190)
            draw.point((x, y), fill=color)
        bob = round(math.sin(2 * math.pi * t) * 1)
        anchor = (10, 21 + bob)
        frame.alpha_composite(sprite, anchor)
        dock = (anchor[0] + cargo_offset[0], anchor[1] + cargo_offset[1])
        # 0–15: ready; 16–45: a full orbital deployment; 46–59: back at dock.
        if 16 <= n <= 45:
            u = (n - 15) / 31
            cx = dock[0] + round(16 * math.sin(2 * math.pi * u))
            cy = dock[1] - round(17 * (1 - math.cos(2 * math.pi * u)) / 2)
            angle = -round(360 * u / 90) * 90
            flying = box_sprite.rotate(angle, resample=Image.Resampling.NEAREST, expand=True)
            draw = ImageDraw.Draw(frame)
            if n <= 24:
                draw.rectangle((cx + 1, cy + box_sprite.height, cx + 3, cy + box_sprite.height + 2 + n % 2), fill=(255, 190, 0))
            frame.alpha_composite(flying, (cx, cy))
        else:
            frame.alpha_composite(box_sprite, dock)
        # Two quiet sea bands. Integer offsets complete an exact period over 60 frames.
        draw = ImageDraw.Draw(frame)
        for band in range(2):
            for x in range(3, 61):
                y = 55 + band * 3 + round(math.sin(2 * math.pi * (x / 20 + 3 * t + band / 3)))
                if (x + n // 5 + band * 3) % 12 < 7:
                    draw.point((x, y), fill=(0, 185, 230) if band == 0 else (0, 90, 160))
        draw.text((11, 1), "SHIP IT", font=font, fill=(180, 240, 255))
        frame.convert("RGB").save(frame_dir / f"{n:03}.png")
    files = sorted(frame_dir.glob("*.png"))
    subprocess.run([str(ROOT / "animate"), *map(str, files), "--name", "ship-it-pro", "--duration", "100"], check=True)
    (assets / "extraction.json").write_text(json.dumps({"source": SOURCE.name, "hero_bounds": bounds,
                                                       "cargo_bounds": cargo_bounds, "scale": scale,
                                                       "motion": "60 frames; whale bob, stars, waves, cargo orbit"}, indent=2) + "\n")


if __name__ == "__main__":
    main()
