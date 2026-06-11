"""
Question Collector – paste-and-record CLI
==========================================
Go through the course page by page and paste each question block here.

How it works
------------
1. Paste the question text and all its choices (one line at a time).
2. Press Enter on a **blank line** → the question is recorded automatically.
   You will see a live count of how many questions have been collected.
3. Keep going until you have entered all questions.
4. When you are completely finished, press Enter on a blank line when
   nothing has been pasted (i.e. two blank lines in a row, or blank line
   right after the previous question was saved) → saves to questions.json.

Ctrl-C also saves whatever has been collected so far and exits.

Parsing rules
-------------
The script auto-detects question vs. choice lines:
  • Lines that look like  "A. ...",  "B) ...",  "1. ...",  "- ..." etc.
    are treated as choices (the prefix is stripped).
  • The remaining lines (before the first choice line) form the question text.
  • Lines with only a question/page number (e.g. "1", "Question 1") are skipped.

Correct answers are stored as "" – fill them in questions.json later.
"""

import json
import os
import re
import sys

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "questions.json")

# Regex that matches typical choice prefixes:  A.  A)  a.  1.  1)  -
_CHOICE_PREFIX = re.compile(
    r"^(?:[A-Da-d][.)]\s+|[1-9]\d*[.)]\s+|-\s+)"
)
# Lines that are only a standalone number or "Question N" – skip them
_SKIP_LINE = re.compile(r"^\s*(?:question\s+)?\d+\.?\s*$", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_line(prompt: str = "") -> str:
    """Read one line from stdin.  Returns empty string on blank line."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        raise KeyboardInterrupt


def load_existing() -> list[dict]:
    if not os.path.exists(OUTPUT_FILE):
        return []
    try:
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save(questions: list[dict]) -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"\n✔  Saved {len(questions)} total question(s) → {OUTPUT_FILE}")


def parse_block(lines: list[str]) -> dict | None:
    """
    Split a list of raw lines into a question dict.
    Returns None if the block has no usable content.
    """
    # Remove leading/trailing blank lines
    lines = [l.rstrip() for l in lines if l.strip()]
    if not lines:
        return None

    question_lines: list[str] = []
    choices: list[str] = []
    in_choices = False

    for line in lines:
        if _SKIP_LINE.match(line):
            continue
        m = _CHOICE_PREFIX.match(line)
        if m:
            in_choices = True
            # Strip the prefix (e.g. "A. ", "1) ", "- ")
            choices.append(line[m.end():].strip())
        elif not in_choices:
            question_lines.append(line.strip())
        # Lines after choices started but without a prefix are continuations of
        # the last choice (rare, but handle gracefully)
        elif choices:
            choices[-1] += " " + line.strip()

    question_text = " ".join(question_lines).strip()
    if not question_text or not choices:
        return None

    return {
        "question": question_text,
        "choices": choices,
        "correct": "",  # unknown – fill in later
    }


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Palo Alto Course – Question Collector")
    print("=" * 60)
    print("Paste a question + its choices, then press Enter on a blank")
    print("line to record it.  Press Enter again (blank) when done.\n")

    existing = load_existing()
    new_questions: list[dict] = []
    total = len(existing)

    if total:
        print(f"[*] Loaded {total} existing question(s) from questions.json\n")

    current_block: list[str] = []

    try:
        while True:
            line = _read_line()

            if line.strip() == "":
                # Blank line = end of current block
                if current_block:
                    q = parse_block(current_block)
                    current_block = []
                    if q:
                        new_questions.append(q)
                        total += 1
                        print(f"  ✔  Recorded  [{total} total]  {q['question'][:65]}{'…' if len(q['question']) > 65 else ''}")
                    else:
                        print("  ⚠  Could not parse that block – skipped.")
                else:
                    # Second blank in a row with nothing pending → done
                    break
            else:
                current_block.append(line)

    except KeyboardInterrupt:
        # Also save whatever is buffered
        if current_block:
            q = parse_block(current_block)
            if q:
                new_questions.append(q)
                total += 1

    if new_questions:
        all_questions = existing + new_questions
        save(all_questions)
        print(f"[+] {len(new_questions)} new question(s) added this session.")
    else:
        print("[*] No new questions collected – questions.json unchanged.")


if __name__ == "__main__":
    main()
