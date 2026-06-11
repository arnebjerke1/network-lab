"""
Question Collector – browser-driven mode
=========================================
Opens a real browser window so YOU navigate the course.
The script watches the page and records questions automatically.

Usage
-----
    python course_scraper/collector.py

Workflow
--------
1. A browser window opens and goes to the Palo Alto login page.
2. Log in with your credentials (the browser is fully interactive).
3. Navigate to the first question page.
4. Press Enter in the terminal → the script reads the current page,
   records any questions it finds, and prints a live count.
5. Go to the next question page in the browser.
6. Press Enter again → records again.
7. Repeat until all pages are done.
8. Type  done  and press Enter (or press Ctrl-C) → saves to questions.json.

Correct answers
---------------
The course does not reveal correct answers, so they are stored as "".
You can fill them in questions.json later.

Requirements
------------
    pip install playwright
    playwright install chromium
"""

import json
import os
import sys

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "questions.json")
LOGIN_URL = "https://learn.paloaltonetworks.com/learn/signin"


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Page scraping (reused from scraper.py logic)
# ---------------------------------------------------------------------------

def _is_correct_element(el) -> bool:
    """
    Return True if an answer element is marked as the correct answer.
    Checks data attributes, aria attributes, class names, and child icons.
    """
    # data-correct / data-right attribute
    if el.get_attribute("data-correct") in ("true", "1", "yes"):
        return True
    if el.get_attribute("data-right") in ("true", "1", "yes"):
        return True

    # aria
    if el.get_attribute("aria-correct") == "true":
        return True

    # class names on the element itself
    cls = (el.get_attribute("class") or "").lower()
    if any(k in cls for k in ("correct", "right-answer", "rightanswer",
                               "is-correct", "answer-correct", "correct-answer",
                               "success", "true-answer")):
        return True

    # Check child elements for correctness markers
    for child_sel in [
        "[class*='correct']", "[class*='right']", "[class*='success']",
        "[data-correct='true']", "[aria-label*='correct' i]",
        # common icon patterns (checkmark SVG titles, sr-only text)
        "svg[class*='correct']", "[class*='check']",
    ]:
        try:
            child = el.query_selector(child_sel)
            if child and child.is_visible():
                return True
        except Exception:
            pass

    return False


def extract_questions_from_page(page) -> list[dict]:
    """
    Try several common quiz markup patterns.
    Returns a list of dicts with keys: question, choices, correct.
    'correct' is "" when the page does not reveal it (question pages).
    On review/results pages the correct answer is populated where detectable.
    """
    questions: list[dict] = []

    # Pattern 1 – DOM blocks with data/class markers
    q_blocks = page.query_selector_all(
        "[data-question], .quiz-question, .question-block, "
        ".assessment-question, [class*='question']"
    )
    for block in q_blocks:
        question_text = ""
        for sel in ["h2", "h3", "h4", "p.question", "[class*='question-text']",
                    "[class*='stem']", "legend"]:
            el = block.query_selector(sel)
            if el:
                question_text = el.inner_text().strip()
                if question_text:
                    break
        if not question_text:
            continue

        choices: list[str] = []
        correct = ""
        answer_els = block.query_selector_all(
            "li, label, [role='radio'], [role='checkbox'], "
            "[class*='answer'], [class*='choice'], [class*='option']"
        )
        for ans in answer_els:
            text = ans.inner_text().strip()
            if not text:
                continue
            choices.append(text)
            if not correct and _is_correct_element(ans):
                correct = text

        if question_text and choices:
            questions.append({
                "question": question_text,
                "choices": choices,
                "correct": correct,
            })

    # Pattern 2 – JSON embedded in <script type="application/json">
    scripts = page.query_selector_all('script[type="application/json"]')
    for s in scripts:
        try:
            data = json.loads(s.inner_text())
        except Exception:
            continue
        _extract_from_json(data, questions)

    return questions


def _extract_from_json(obj, out: list, depth: int = 0) -> None:
    if depth > 10:
        return
    if isinstance(obj, dict):
        q = obj.get("question") or obj.get("questionText") or obj.get("stem")
        choices_raw = obj.get("choices") or obj.get("answers") or obj.get("options") or []
        if q and choices_raw:
            choice_texts: list[str] = []
            for c in choices_raw:
                if isinstance(c, str):
                    choice_texts.append(c)
                elif isinstance(c, dict):
                    t = c.get("text") or c.get("label") or c.get("value") or ""
                    choice_texts.append(t)
            out.append({
                "question": str(q),
                "choices": choice_texts,
                "correct": "",
            })
        for v in obj.values():
            _extract_from_json(v, out, depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _extract_from_json(item, out, depth + 1)


def question_key(text: str) -> str:
    return " ".join(text.split()).strip().lower()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] Playwright is not installed.")
        print("    Run:  pip install playwright && playwright install chromium")
        sys.exit(1)

    print("=" * 60)
    print("  Palo Alto Course – Browser Question Collector")
    print("=" * 60)
    print()
    print("A browser will open. Log in, navigate to the first question,")
    print("then come back here and press Enter to record it.")
    print("Type  done  to finish and save.\n")

    existing = load_existing()
    new_questions: list[dict] = []
    seen_keys: set[str] = {question_key(q["question"]) for q in existing}
    total = len(existing)

    if total:
        print(f"[*] Loaded {total} existing question(s) from questions.json\n")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print(f"[*] Opening login page: {LOGIN_URL}")
        try:
            page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=15000)
        except Exception as e:
            print(f"[!] Could not open login page: {e}")

        print("[*] Log in to the course in the browser window, then navigate")
        print("    to the first question page.\n")

        try:
            while True:
                cmd = input("Press Enter to record current page  (or type 'done' to finish): ").strip().lower()
                if cmd in ("done", "quit", "exit", "q"):
                    break

                # Give the page a moment to settle after navigation
                try:
                    page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass

                found = extract_questions_from_page(page)
                added = 0
                updated = 0
                for q in found:
                    key = question_key(q["question"])
                    if key not in seen_keys:
                        seen_keys.add(key)
                        new_questions.append(q)
                        total += 1
                        added += 1
                        correct_tag = f"  ✓ answer: {q['correct']}" if q["correct"] else ""
                        print(f"  ✔  [{total} total]  {q['question'][:60]}{'…' if len(q['question']) > 60 else ''}{correct_tag}")
                    elif q["correct"]:
                        # Results page revealed the answer – back-fill it
                        for stored in new_questions:
                            if question_key(stored["question"]) == key and not stored["correct"]:
                                stored["correct"] = q["correct"]
                                updated += 1
                                print(f"  ↻  Answer filled: {q['correct'][:50]}  ← {q['question'][:45]}…")
                                break
                        # Also back-fill in the pre-existing list loaded from disk
                        for stored in existing:
                            if question_key(stored["question"]) == key and not stored["correct"]:
                                stored["correct"] = q["correct"]
                                updated += 1
                                print(f"  ↻  Answer filled (existing): {q['correct'][:40]}  ← {q['question'][:35]}…")
                                break

                if added == 0 and updated == 0:
                    print(f"  ⚠  No new questions or answers found on this page (URL: {page.url[:80]})")
                else:
                    parts = []
                    if added:
                        parts.append(f"{added} new question(s)")
                    if updated:
                        parts.append(f"{updated} answer(s) filled in")
                    print(f"  → {', '.join(parts)} from this page.\n")

        except KeyboardInterrupt:
            print("\n[!] Interrupted.")

        browser.close()

    if new_questions:
        all_questions = existing + new_questions
        save(all_questions)
        print(f"[+] {len(new_questions)} new question(s) added this session.")
    else:
        print("[*] No new questions collected – questions.json unchanged.")


if __name__ == "__main__":
    main()
