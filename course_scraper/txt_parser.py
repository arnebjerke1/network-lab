"""
TXT Quiz Parser
---------------
Parses the plain-text quiz export format from the Palo Alto Networks learning
platform and converts it to questions.json for use by quiz_generator.py.

Two text formats are handled automatically:

  Format A – scored quiz  (contains an "Options" / "Correct answer:" block)
  Format B – required quiz (inline "Correct answer: …" or "correct answer: …")

Multi-select questions ("Choose two") preserve all listed correct answers.

Usage
-----
    python txt_parser.py                            # reads part1.txt -> questions.json
    python txt_parser.py "My Quiz.txt"              # custom input file
    python txt_parser.py "My Quiz.txt" out.json     # custom output file
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_FILE  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    SCRIPT_DIR, "Network Security NetSec Professional subject 1.txt"
)
OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    SCRIPT_DIR, "questions.json"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_QUESTION_HEADER = re.compile(r"^Question \d+ of \d+", re.MULTILINE)

# Lines that are metadata, not choices
_SKIP_LINES = re.compile(
    r"^\(disabled\)$"
    r"|^Options$"
    r"|^You gave (the |a )?(correct|wrong|partially correct) answer"
    r"|^(Correct|Wrong|Partially correct) answer$"
    r"|^Score:\s*\d"
    r"|^Correct answers?:$",
    re.IGNORECASE,
)

_CORRECT_INLINE  = re.compile(r"^[Cc]orrect answer:\s+(.+)$")
_CORRECT_SECTION = re.compile(r"^[Cc]orrect answers?:$", re.IGNORECASE)


def _collect_choices(lines):
    """Return non-empty, non-metadata lines as a list of choice strings."""
    choices = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        if _SKIP_LINES.match(ln):
            continue
        if _CORRECT_INLINE.match(ln):
            continue
        if _CORRECT_SECTION.match(ln):
            continue
        choices.append(ln)
    return choices


# ---------------------------------------------------------------------------
# Per-block parsers
# ---------------------------------------------------------------------------

def _parse_scored_block(question_text, body_lines):
    """
    Parse Format A (has 'Options' + 'Correct answer(s):' section).

    Returns a dict or None.
    """
    # Split at the 'Options' sentinel
    options_idx = None
    for i, ln in enumerate(body_lines):
        if ln.strip() == "Options":
            options_idx = i
            break

    if options_idx is None:
        return None

    choice_lines  = body_lines[:options_idx]
    answer_lines  = body_lines[options_idx + 1:]

    choices = _collect_choices(choice_lines)
    if not choices:
        return None

    # Find correct answer(s) after "Correct answer:" / "Correct answers:"
    correct_list = []
    in_correct = False
    for ln in answer_lines:
        stripped = ln.strip()
        if _CORRECT_SECTION.match(stripped):
            in_correct = True
            continue
        if in_correct:
            if stripped:
                correct_list.append(stripped)
            # Stop at next question header or blank-line+data transition
        else:
            # Some single-answer blocks put it inline: "Correct answer:\nText"
            pass

    if not correct_list:
        return None

    correct_answers = list(dict.fromkeys(correct_list))
    return {
        "question": question_text,
        "choices": choices,
        "correct": correct_answers[0],
        "correct_answers": correct_answers,
    }


def _parse_required_block(question_text, body_lines):
    """
    Parse Format B (has inline 'Correct answer: …' or 'correct answer: …').

    Returns a dict or None.
    """
    choices = []
    correct_list = []
    in_correct_section = False

    for ln in body_lines:
        stripped = ln.strip()
        if not stripped:
            continue

        m = _CORRECT_INLINE.match(stripped)
        if m:
            correct_list.append(m.group(1).strip())
            in_correct_section = False
            continue

        if _CORRECT_SECTION.match(stripped):
            in_correct_section = True
            continue

        if in_correct_section:
            if not _SKIP_LINES.match(stripped):
                correct_list.append(stripped)
            continue

        if _SKIP_LINES.match(stripped):
            continue

        choices.append(stripped)

    correct_answers = [c for c in dict.fromkeys(correct_list) if c]
    if not choices or not correct_answers:
        return None

    return {
        "question": question_text,
        "choices": choices,
        "correct": correct_answers[0],
        "correct_answers": correct_answers,
    }


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse_txt(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        text = f.read()

    boundaries = [m.start() for m in _QUESTION_HEADER.finditer(text)]
    if not boundaries:
        print("[!] No question headers found in the file.")
        return []

    boundaries.append(len(text))

    questions = []
    seen = set()
    skipped = 0

    for i in range(len(boundaries) - 1):
        block = text[boundaries[i] : boundaries[i + 1]]
        lines = block.splitlines()

        header = lines[0].strip()
        is_required = "(required)" in header

        # Extract question text: non-empty lines immediately after the header
        idx = 1
        while idx < len(lines) and not lines[idx].strip():
            idx += 1

        q_lines = []
        while idx < len(lines) and lines[idx].strip():
            q_lines.append(lines[idx].strip())
            idx += 1
        question_text = " ".join(q_lines)

        if not question_text:
            skipped += 1
            continue

        body = lines[idx:]

        if is_required:
            q = _parse_required_block(question_text, body)
        else:
            q = _parse_scored_block(question_text, body)

        if q is None:
            skipped += 1
            print(f"[!] Could not parse block starting: {question_text[:60]}")
            continue

        # Deduplicate by normalised question text
        key = " ".join(q["question"].split()).lower()
        if key in seen:
            continue
        seen.add(key)

        questions.append(q)

    print(f"[+] Parsed {len(questions)} unique questions  ({skipped} skipped)")
    return questions


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"[*] Parsing: {INPUT_FILE}")
    questions = parse_txt(INPUT_FILE)

    if not questions:
        print("[!] Nothing to write.")
        sys.exit(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"[+] Saved {len(questions)} questions to: {OUTPUT_FILE}")
    print("[*] Run quiz_generator.py to regenerate quiz.html")
