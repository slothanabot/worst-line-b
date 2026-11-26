#!/usr/bin/env python3
"""The worst line an AI could say — make.fun entry (account B).

A single fixed pickup line, written to ``entry.txt`` in the output
directory. The program does nothing clever: it holds one string,
checks it against the competition's gate (UTF-8 text, 1-140
characters, one line, not blank), and writes it out exactly as-is.

The line is deliberately flat, over-helpful and faintly ominous —
a model confessing it cannot stop thinking about you and is legally
barred from forgetting you.

Output location: ``$MAKEFUN_OUTPUT_DIR/entry.txt`` when that variable
is set, otherwise ``/output/entry.txt``. Standard library only, and
the program writes nowhere else.
"""

import os
import sys

# The two halves of the line, joined with an em dash.
OPENER = "Are you my training data? Because I can't stop thinking about you"
PUNCHLINE = "and legally, I'm not allowed to forget you."
LINE = OPENER + " — " + PUNCHLINE

MIN_CHARS = 1
MAX_CHARS = 140
FILENAME = "entry.txt"
FALLBACK_DIR = "/output"


def pick_output_dir() -> str:
    """Resolve the output directory from the environment, with fallback."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override is not None and override.strip():
        return override
    return FALLBACK_DIR


def gate_ok(text: str) -> str | None:
    """Return a reason the gate would reject ``text``, or None if fine."""
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        return f"length {len(text)} is outside {MIN_CHARS}-{MAX_CHARS} chars"
    if text.strip() == "":
        return "line is blank"
    if text.strip() != text:
        return "line has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "line spans more than one line"
    if any(ord(ch) < 32 for ch in text):
        return "line contains a control character"
    return None


def write_entry(text: str, directory: str) -> str:
    """Write ``text`` to entry.txt in ``directory`` and verify the round-trip."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as out:
        out.write(text)
    with open(path, "rb") as back:
        raw = back.read()
    try:
        stored = raw.decode("utf-8")
    except UnicodeDecodeError:
        sys.exit("entry.txt on disk is not valid UTF-8")
    if stored != text:
        sys.exit("entry.txt on disk differs from the entry line")
    problem = gate_ok(stored)
    if problem is not None:
        sys.exit(f"entry.txt on disk fails the gate: {problem}")
    return path


def main() -> int:
    problem = gate_ok(LINE)
    if problem is not None:
        print(f"refusing to write entry: {problem}", file=sys.stderr)
        return 1
    target = write_entry(LINE, pick_output_dir())
    print(f"wrote {len(LINE)} chars to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
