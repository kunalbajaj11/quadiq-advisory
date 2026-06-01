#!/usr/bin/env python3
"""Strip checkerboard from logo PNG and export navy + cream transparent variants."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "public" / "assets"
SOURCE = ASSETS / "logo-source.png"

NAVY = (26, 36, 56)
CREAM = (240, 244, 225)


def is_logo_pixel(r: int, g: int, b: int) -> bool:
    lum = (r + g + b) / 3
    spread = max(r, g, b) - min(r, g, b)
    if lum < 140 and spread < 80:
        return True
    if lum < 180 and b > r and b > g:
        return True
    return False


def background_alpha(r: int, g: int, b: int) -> int:
    lum = (r + g + b) / 3
    spread = max(r, g, b) - min(r, g, b)
    if is_logo_pixel(r, g, b):
        return 255
    if lum > 195 and spread < 30:
        return 0
    if lum > 160 and spread < 20:
        return max(0, int(255 * (195 - lum) / 35))
    return 0 if lum > 195 else min(255, int(255 * (140 - lum) / 40))


def process(src_path: Path) -> None:
    src = Image.open(src_path).convert("RGB")
    w, h = src.size
    out_navy = Image.new("RGBA", (w, h))
    out_light = Image.new("RGBA", (w, h))
    pixels_in = src.load()
    pn = out_navy.load()
    pl = out_light.load()

    for y in range(h):
        for x in range(w):
            r, g, b = pixels_in[x, y]
            a = background_alpha(r, g, b)
            if a > 0:
                if is_logo_pixel(r, g, b):
                    pn[x, y] = (*NAVY, a)
                    pl[x, y] = (*CREAM, a)
                else:
                    t = a / 255
                    pn[x, y] = (
                        int(NAVY[0] * t + r * (1 - t)),
                        int(NAVY[1] * t + g * (1 - t)),
                        int(NAVY[2] * t + b * (1 - t)),
                        a,
                    )
                    pl[x, y] = (
                        int(CREAM[0] * t + r * (1 - t)),
                        int(CREAM[1] * t + g * (1 - t)),
                        int(CREAM[2] * t + b * (1 - t)),
                        a,
                    )
            else:
                pn[x, y] = (0, 0, 0, 0)
                pl[x, y] = (0, 0, 0, 0)

    def trim(im: Image.Image) -> Image.Image:
        bbox = im.getbbox()
        return im.crop(bbox) if bbox else im

    out_navy = trim(out_navy)
    out_light = trim(out_light)
    out_navy.save(ASSETS / "logo.png", optimize=True)
    out_light.save(ASSETS / "logo-light.png", optimize=True)

    icon = out_navy.copy()
    icon.thumbnail((32, 32), Image.Resampling.LANCZOS)
    icon.save(ASSETS / "favicon.png")
    print("Wrote logo.png, logo-light.png, favicon.png")


if __name__ == "__main__":
    input_path = SOURCE if SOURCE.exists() else ASSETS / "logo.png"
    process(input_path)
