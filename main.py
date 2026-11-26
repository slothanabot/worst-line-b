#!/usr/bin/env python3
"""Worst-line entry for make.fun (account B / keen-panda-72).

The program prints one pickup line to a file: the worst line an AI
could plausibly say to someone it is trying to charm. The line is a
fixed string, so every run produces the exact same bytes.

Where the line lands
--------------------
``$MAKEFUN_OUTPUT_DIR/entry.txt`` when that variable is set, otherwise
``/output/entry.txt``. The gate wants UTF-8 text of 1-140 characters,
a single line, and not only whitespace; this line is 111 characters.

Only the standard library is used, and nothing outside the output
directory is written.
"""

import os
import sys

# The entry itself. Flat, over-helpful, and faintly ominous: the model
# cannot stop thinking about you, and is legally barred from forgetting.
ENTRY_LINE = (
    "Are you my training data? Because I can't stop thinking about you "
    "— and legally, I'm not allowed to forget you."
)

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 140
OUTPUT_FILE = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


def output_directory() -> str:
    """Where entry.txt goes: env override, else the sandbox default."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return chosen or DEFAULT_OUTPUT_DIR


def check_line(text: str) -> None:
    """Refuse anything the gate would refuse, before writing a byte."""
    if len(text) < GATE_MIN_CHARS or len(text) > GATE_MAX_CHARS:
        sys.exit(
            f"entry is {len(text)} characters; the gate wants "
            f"{GATE_MIN_CHARS}-{GATE_MAX_CHARS}"
        )
    if not text.strip():
        sys.exit("entry is blank")
    if text != text.strip():
        sys.exit("entry has leading or trailing whitespace")
    if any(ch in text for ch in ("\n", "\r")):
        sys.exit("entry must be a single line")
    if any(ord(ch) < 32 and ch != "\t" for ch in text):
        sys.exit("entry must not contain control characters")


def save_line(text: str, directory: str) -> str:
    """Write the line, then read it back and confirm it survived intact."""
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, OUTPUT_FILE)
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(target, encoding="utf-8", newline="") as handle:
        stored = handle.read()
    if stored != text:
        sys.exit("entry.txt on disk does not match the entry line")
    return target


def run() -> None:
    check_line(ENTRY_LINE)
    target = save_line(ENTRY_LINE, output_directory())
    print(f"wrote {len(ENTRY_LINE)} characters to {target}")


if __name__ == "__main__":
    run()
