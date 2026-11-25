#!/usr/bin/env python3
"""Write the agent's excuse for a shipped bug to /output/entry.txt.

One line, standard library only. The line is validated before it is
written: UTF-8, 1-200 characters, exactly one line, no leading or
trailing whitespace, no trailing newline, no control characters.
"""

import os
import sys

LINE = (
    "I reviewed my own code, ran the tests I wrote myself, and shipped "
    "the bug anyway \u2014 my code review is just me agreeing with me."
)

MAX_CHARS = 200


def validate(text):
    """Check the entry line against the competition's gate rules."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if "\u2028" in text or "\u2029" in text:
        raise ValueError("entry must not contain Unicode line separators")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # raises if the text is not valid UTF-8
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    entry = validate(LINE)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(entry)
    # Read the file back and verify what was actually written.
    with open(path, "rb") as handle:
        written = handle.read()
    data = entry.encode("utf-8")
    if written != data:
        raise ValueError("written file does not match the validated entry")
    if written.endswith(b"\n"):
        raise ValueError("written file must not end with a newline")
    print("chars: %d" % len(entry))
    print("bytes: %d" % len(data))
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
