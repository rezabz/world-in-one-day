#!/usr/bin/env python3
"""Entry program for news-image-20261118.

Writes the bundled poster (entry.png, 1024x1024, the world news of
Wednesday 18 November 2026) to /output/entry.png. Standard library only,
no network, fully deterministic: the same bundled bytes are copied on
every run, so two runs write identical files.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard: the gate allows at most 1 MiB; refuse to emit a bad file silently.
    if os.path.getsize(dst) > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB gate limit")


if __name__ == "__main__":
    main()
    sys.exit(0)
