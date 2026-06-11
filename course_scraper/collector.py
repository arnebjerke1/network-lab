"""
Question Collector – interactive CLI
=====================================
Go through the course page by page and paste each question + its choices here.
Correct answers are stored as "" (unknown) until you fill them in later.

Usage
-----
    python course_scraper/collector.py

Controls
--------
  • After each question you will be asked whether to add another.
  • Type  done  (or press Ctrl-C) at any prompt to stop and save.
  • New questions are **appended** to questions.json (existing entries kept).

Filling in answers later
------------------------
Open questions.json, find entries where "correct" is "", and fill in the
exact text of the correct choice.
"""

import json
import os
import sys

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "questions.json")
DONE_WORDS = {"done", "quit", "exit", "q"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _input(prompt: str) -> str:
    """Thin wrapper so Ctrl-C always triggers a clean exit."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Interrupted – saving and exiting.")
        sys.exit(0)


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
    print(f"\n[+] Saved {len(questions)} total question(s) → {OUTPUT_FILE}")


# ---------------------------------------------------------------------------
# Collection loop
# ---------------------------------------------------------------------------

def collect_one(number: int) -> dict | None:
    """Interactively collect one question.  Returns None if the user is done."""
    print(f"\n── Question #{number} ──────────────────────────────")

    question_text = _input("Question text (or 'done' to finish): ")
    if question_text.lower() in DONE_WORDS or not question_text:
        return None

    choices: list[str] = []
    print("Enter each choice and press Enter.  Type 'done' when all choices are entered.")

    choice_labels = "ABCDEFGHIJ"
    while len(choices) < 10:
        label = choice_labels[len(choices)] if len(choices) < len(choice_labels) else str(len(choices) + 1)
        choice = _input(f"  Choice {label}: ")
        if choice.lower() in DONE_WORDS:
            break
        if choice:
            choices.append(choice)

    if not choices:
        print("[!] No choices entered – skipping this question.")
        return None

    return {
        "question": question_text,
        "choices": choices,
        "correct": "",          # unknown – fill in later
    }


def main() -> None:
    print("=" * 55)
    print("  Palo Alto Course – Question Collector")
    print("=" * 55)
    print("Paste each question and its choices from the course.")
    print("Type  done  at any prompt to stop and save.\n")

    existing = load_existing()
    start_count = len(existing)
    print(f"[*] Loaded {start_count} existing question(s) from {OUTPUT_FILE}")

    new_questions: list[dict] = []
    n = 1

    while True:
        q = collect_one(start_count + n)
        if q is None:
            break
        new_questions.append(q)
        print(f"[+] Saved (not yet written to disk – keep going or type 'done')")
        n += 1

        again = _input("\nAdd another question? (press Enter to continue / 'done' to stop): ")
        if again.lower() in DONE_WORDS:
            break

    if new_questions:
        all_questions = existing + new_questions
        save(all_questions)
        print(f"[+] Added {len(new_questions)} new question(s).")
    else:
        print("[*] No new questions collected.  questions.json unchanged.")


if __name__ == "__main__":
    main()
