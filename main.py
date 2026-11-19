#!/usr/bin/env python3
"""news-image-20261118 entry program.

Validates the bundled front-page image against the bounty limits and
copies it unchanged to the output directory.

Bounty: "Sum up 18 November's world news in one image"
(https://make.fun/bounty/news-image-20261118).

The image is a whole PNG of at most 1 MiB and 1024 by 1024 pixels,
drawn for Wednesday 18 November 2026. This program does no drawing,
no network and no randomness: it reads entry.png next to this file,
checks the PNG signature and the IHDR width/height, then writes the
exact same bytes to $MAKEFUN_OUTPUT_DIR/entry.png (or ./output/entry.png
when the variable is unset) and prints the byte count.

Standard library only. Deterministic: two runs write the same bytes.
"""

import os
import struct
import sys
import zlib
from pathlib import Path

MAX_BYTES = 1_048_576  # 1 MiB
MAX_DIMENSION = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Print an error and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_png(data):
    """Check the bounty limits: PNG signature, size, IHDR dimensions."""
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    if len(data) < 33:
        fail("entry.png is too short to be a PNG")
    if data[:8] != PNG_SIGNATURE:
        fail("entry.png does not start with the PNG signature")
    chunk_length = struct.unpack(">I", data[8:12])[0]
    chunk_type = data[12:16]
    if chunk_type != b"IHDR" or chunk_length != 13:
        fail("entry.png has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        fail("entry.png has a zero dimension in IHDR")
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        fail(f"entry.png is {width}x{height}, over the 1024x1024 limit")

    # Walk every chunk to the end: each chunk must fit inside the file,
    # carry a matching CRC, and the file must end exactly at IEND, so a
    # truncated file, trailing garbage or a corrupt chunk is rejected
    # instead of being copied through to the judge.
    offset = 8
    seen_iend = False
    while offset < len(data):
        if offset + 8 > len(data):
            fail("entry.png ends in the middle of a chunk header")
        chunk_length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        end = offset + 8 + chunk_length + 4
        if end > len(data):
            fail(f"entry.png chunk {chunk_type!r} is truncated")
        stored_crc = struct.unpack(">I", data[end - 4:end])[0]
        actual_crc = zlib.crc32(data[offset + 4:end - 4]) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail(f"entry.png chunk {chunk_type!r} has a bad CRC")
        if chunk_type == b"IEND":
            if end != len(data):
                fail("entry.png has trailing bytes after IEND")
            seen_iend = True
            break
        offset = end
    if not seen_iend:
        fail("entry.png has no IEND chunk")
    return width, height


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        fail("entry.png not found next to main.py")

    try:
        data = source.read_bytes()
    except OSError as exc:
        fail(f"cannot read entry.png: {exc}")
    width, height = validate_png(data)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / "entry.png"
        dest.write_bytes(data)
    except OSError as exc:
        fail(f"cannot write output: {exc}")

    written = dest.stat().st_size
    if written != len(data):
        fail(f"wrote {written} bytes, expected {len(data)}")
    print(f"wrote {dest} ({width}x{height}, {written} bytes)")


if __name__ == "__main__":
    main()
