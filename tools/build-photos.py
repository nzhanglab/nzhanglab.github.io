#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build web-ready lab photos for the team page.

Originals live OUTSIDE the repo, in ../Photos/, and are never modified:

    Photos/PhotoReel/       recent lab photos  -> assets/photos/reel/
    Photos/MemoryLane/      older lab photos   -> assets/photos/memory/
    Photos/CurrentMembers/  member portraits   -> assets/photos/members/
    Photos/PI/              the PI's portrait  -> assets/photos/pi/

Many originals are HEIC (which no browser displays) and 1-9 MB each, so this
script decodes them, applies the EXIF rotation, resizes to a couple of
sensible widths, and writes both JPEG and WebP. Output metadata is stripped,
which also removes the GPS coordinates the phone recorded.

It also writes _data/photos.yml so the Liquid template can loop over whatever
is actually on disk rather than a hand-maintained list.

Usage:  python tools/build-photos.py            (from the repo root)
        python tools/build-photos.py --force    (rebuild even if up to date)

Requires: pillow, pillow-heif
"""
import argparse
import io
import os
import re
import sys

from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    sys.exit("pillow-heif is required for the HEIC originals:  pip install pillow-heif")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = os.path.join(os.path.dirname(REPO), "Photos")

# source folder -> (output folder, widths, crop aspect or None)
SETS = {
    "PhotoReel":      ("reel",    (1600, 900), None),
    "MemoryLane":     ("memory",  (1600, 900), None),
    "CurrentMembers": ("members", (800, 400),  4 / 5.0),
    "PI":             ("pi",      (640, 320),  4 / 5.0),
}

JPEG_Q, WEBP_Q = 82, 80
EXTS = (".jpg", ".jpeg", ".png", ".heic", ".heif", ".tif", ".tiff", ".webp")


def slugify(name):
    stem = os.path.splitext(name)[0]
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
    return re.sub(r"-{2,}", "-", stem)


def shot_date(im):
    """Return 'YYYY-MM-DD' from EXIF, or '' when the camera recorded none."""
    try:
        exif = im.getexif()
        raw = exif.get(306) or exif.get_ifd(0x8769).get(36867) or ""
        m = re.match(r"(\d{4})[:\-](\d{2})[:\-](\d{2})", str(raw))
        return "-".join(m.groups()) if m else ""
    except Exception:
        return ""


def crop_to(im, aspect):
    """Centre-crop to a target width/height ratio, biased slightly upward so
    faces are not cut off in portraits."""
    w, h = im.size
    want = aspect
    have = w / float(h)
    if abs(have - want) < 0.01:
        return im
    if have > want:                      # too wide -> trim the sides
        new_w = int(round(h * want))
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(round(w / want))         # too tall -> trim, keeping the top
    top = int((h - new_h) * 0.30)
    return im.crop((0, top, w, top + new_h))


def emit(im, out_dir, slug, widths):
    """Write jpg+webp at each width; return (w, h) of the largest output."""
    os.makedirs(out_dir, exist_ok=True)
    biggest = None
    for width in widths:
        # Always write every width, even when the source is smaller than the
        # target - never upscaled, but it keeps the srcset in the template
        # uniform instead of needing per-image special cases.
        scale = min(1.0, width / float(im.width))
        size = (max(1, int(im.width * scale)), max(1, int(im.height * scale)))
        resized = im.resize(size, Image.LANCZOS)
        clean = Image.new("RGB", resized.size)      # drops all metadata
        clean.paste(resized)
        clean.save(os.path.join(out_dir, "%s-%d.jpg" % (slug, width)),
                   "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
        clean.save(os.path.join(out_dir, "%s-%d.webp" % (slug, width)),
                   "WEBP", quality=WEBP_Q, method=5)
        if biggest is None:
            biggest = size
    return biggest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="rebuild even when the output is newer than the source")
    args = ap.parse_args()

    manifest = {}
    total_in = total_out = 0

    for src_name, (out_name, widths, aspect) in SETS.items():
        src_dir = os.path.join(SRC_ROOT, src_name)
        out_dir = os.path.join(REPO, "assets", "photos", out_name)
        entries = []
        if not os.path.isdir(src_dir):
            print("  (skipping %s - not found)" % src_name)
            manifest[out_name] = entries
            continue

        print("== %s -> assets/photos/%s" % (src_name, out_name))
        for fname in sorted(os.listdir(src_dir)):
            if not fname.lower().endswith(EXTS) or fname.startswith("."):
                continue
            src = os.path.join(src_dir, fname)
            slug = slugify(fname)
            marker = os.path.join(out_dir, "%s-%d.jpg" % (slug, max(widths)))
            total_in += os.path.getsize(src)

            try:
                im = Image.open(src)
                date = shot_date(im)
                im = ImageOps.exif_transpose(im)
                if im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                if aspect:
                    im = crop_to(im, aspect)

                fresh = (not args.force and os.path.exists(marker)
                         and os.path.getmtime(marker) >= os.path.getmtime(src))
                if fresh:
                    with Image.open(marker) as done:
                        dims = done.size
                    print("   = %-46s (up to date)" % fname)
                else:
                    dims = emit(im, out_dir, slug, widths)
                    print("   + %-46s %dx%d  %s" % (fname, dims[0], dims[1], date or "no date"))
            except Exception as exc:
                print("   ! %-46s FAILED: %s" % (fname, exc))
                continue

            for width in widths:
                p = os.path.join(out_dir, "%s-%d.jpg" % (slug, width))
                if os.path.exists(p):
                    total_out += os.path.getsize(p) + os.path.getsize(p[:-4] + ".webp")

            entries.append({"slug": slug, "date": date,
                            "w": dims[0], "h": dims[1],
                            "orient": "portrait" if dims[1] > dims[0] else "landscape"})
        manifest[out_name] = entries

    data_path = os.path.join(REPO, "_data", "photos.yml")
    with io.open(data_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Generated by tools/build-photos.py - do not edit by hand.\n")
        fh.write("# Rerun the script after adding photos to ../Photos/.\n")
        for key in sorted(manifest):
            fh.write("\n%s:\n" % key)
            for e in manifest.get(key, []):
                fh.write('  - slug: "%s"\n    w: %d\n    h: %d\n    orient: %s\n'
                         % (e["slug"], e["w"], e["h"], e["orient"]))
                if e["date"]:
                    fh.write('    date: "%s"\n' % e["date"])

    print("\nwrote %s" % os.path.relpath(data_path, REPO))
    print("sources %.1f MB  ->  web derivatives %.1f MB"
          % (total_in / 1e6, total_out / 1e6))


if __name__ == "__main__":
    main()
