"""
Palo Alto Networks – Certified Network Security Professional
Course Scraper

Logs in to learn.paloaltonetworks.com, navigates through the PCNSP learning
plan page by page, and collects every quiz question together with the correct
answer.  The result is saved to questions.json for use by quiz_generator.py.

Usage
-----
1.  Set your credentials in environment variables (or edit the constants below):
        export PALO_EMAIL="you@example.com"
        export PALO_PASSWORD="your-password"

2.  Install dependencies:
        pip install -r requirements.txt
        playwright install chromium

3.  Run:
        python scraper.py

    The script opens a visible browser so you can monitor progress.
    Set HEADLESS=true to run without a window:
        HEADLESS=true python scraper.py
"""

import json
import os
import time

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EMAIL = os.environ.get("PALO_EMAIL", "")
PASSWORD = os.environ.get("PALO_PASSWORD", "")
HEADLESS = os.environ.get("HEADLESS", "false").lower() == "true"

LEARNING_PLAN_URL = (
    "https://learn.paloaltonetworks.com/learn/learning-plans"
    "/palo-alto-networks-certified-network-security-professional"
)
LOGIN_URL = "https://learn.paloaltonetworks.com/learn/signin"

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "questions.json")

# How long (ms) to wait for elements before giving up on a page
DEFAULT_TIMEOUT = 15_000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def login(page):
    """Navigate to the sign-in page and authenticate."""
    print("[*] Navigating to login page …")
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")

    # Fill credentials – selectors are best-guesses; inspect the page if they fail
    page.fill('input[type="email"], input[name="email"], input[id*="email"]', EMAIL)
    page.fill('input[type="password"], input[name="password"], input[id*="password"]', PASSWORD)
    page.click('button[type="submit"], input[type="submit"], button:has-text("Sign in"), button:has-text("Log in")')

    page.wait_for_load_state("networkidle")
    print("[+] Login submitted – waiting for dashboard …")
    time.sleep(3)


def extract_questions_from_page(page) -> list[dict]:
    """
    Try several common quiz markup patterns used by LMS platforms built on
    Docebo / Rise 360 / similar.  Returns a (possibly empty) list of dicts:

        {
            "question": "...",
            "choices": ["A", "B", "C", "D"],
            "correct": "A"          # text of the correct choice
        }
    """
    questions = []

    # --- Pattern 1: elements with data-correct / aria-checked="true" ---
    q_blocks = page.query_selector_all(
        "[data-question], .quiz-question, .question-block, "
        ".assessment-question, [class*='question']"
    )

    for block in q_blocks:
        question_text = ""
        # Try common question-text selectors inside the block
        for sel in ["h2", "h3", "h4", "p.question", "[class*='question-text']",
                    "[class*='stem']", "legend"]:
            el = block.query_selector(sel)
            if el:
                question_text = el.inner_text().strip()
                if question_text:
                    break

        if not question_text:
            continue

        # Gather all answer choices
        choices = []
        correct = ""
        answer_els = block.query_selector_all(
            "li, label, [role='radio'], [role='checkbox'], "
            "[class*='answer'], [class*='choice'], [class*='option']"
        )
        for ans in answer_els:
            text = ans.inner_text().strip()
            if not text:
                continue

            is_correct = (
                ans.get_attribute("data-correct") in ("true", "1")
                or ans.get_attribute("aria-selected") == "true"
                or "correct" in (ans.get_attribute("class") or "").lower()
            )

            choices.append(text)
            if is_correct:
                correct = text

        if question_text and choices:
            questions.append({
                "question": question_text,
                "choices": choices,
                "correct": correct,
            })

    # --- Pattern 2: JSON embedded in a <script type="application/json"> ---
    scripts = page.query_selector_all('script[type="application/json"]')
    for s in scripts:
        try:
            data = json.loads(s.inner_text())
        except (json.JSONDecodeError, Exception):
            continue

        # Recursively hunt for question-like keys
        _extract_from_json(data, questions)

    return questions


def _extract_from_json(obj, out: list, depth: int = 0):
    """Recursively look for quiz question patterns in arbitrary JSON."""
    if depth > 10:
        return
    if isinstance(obj, dict):
        q = obj.get("question") or obj.get("questionText") or obj.get("stem")
        choices = (
            obj.get("choices")
            or obj.get("answers")
            or obj.get("options")
            or []
        )
        correct_flag = obj.get("correct") or obj.get("isCorrect") or obj.get("correctAnswer")

        if q and choices:
            correct_text = ""
            choice_texts = []
            for c in choices:
                if isinstance(c, str):
                    choice_texts.append(c)
                elif isinstance(c, dict):
                    t = c.get("text") or c.get("label") or c.get("value") or ""
                    choice_texts.append(t)
                    if c.get("correct") or c.get("isCorrect"):
                        correct_text = t
            if not correct_text and isinstance(correct_flag, str):
                correct_text = correct_flag
            out.append({
                "question": str(q),
                "choices": choice_texts,
                "correct": correct_text,
            })

        for v in obj.values():
            _extract_from_json(v, out, depth + 1)

    elif isinstance(obj, list):
        for item in obj:
            _extract_from_json(item, out, depth + 1)


def get_next_button(page):
    """Return the 'Next' / 'Continue' button element, or None."""
    for selector in [
        "button:has-text('Next')",
        "button:has-text('Continue')",
        "a:has-text('Next')",
        "a:has-text('Continue')",
        "[aria-label*='Next']",
        "[class*='next-btn']",
        "[class*='btn-next']",
    ]:
        try:
            el = page.query_selector(selector)
            if el and el.is_visible():
                return el
        except Exception:
            pass
    return None


# ---------------------------------------------------------------------------
# Main scraping loop
# ---------------------------------------------------------------------------

def scrape_course() -> list[dict]:
    all_questions: list[dict] = []
    seen_questions: set[str] = set()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)

        if not EMAIL or not PASSWORD:
            print(
                "[!] No credentials found.\n"
                "    Set PALO_EMAIL and PALO_PASSWORD environment variables,\n"
                "    then re-run.  The browser will open so you can log in manually."
            )
            page.goto(LOGIN_URL, wait_until="domcontentloaded")
            input("    >> Press ENTER here after you have logged in manually … ")
        else:
            login(page)

        print(f"[*] Navigating to learning plan: {LEARNING_PLAN_URL}")
        page.goto(LEARNING_PLAN_URL, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        page_number = 0

        while True:
            page_number += 1
            url = page.url
            print(f"[{page_number}] {url}")

            # Give dynamic content time to render
            time.sleep(2)

            questions = extract_questions_from_page(page)

            for q in questions:
                key = q["question"][:120]
                if key not in seen_questions:
                    seen_questions.add(key)
                    all_questions.append(q)
                    print(f"    + Question collected: {q['question'][:70]} …")

            next_btn = get_next_button(page)
            if next_btn is None:
                print("[*] No 'Next' button found – end of course or manual navigation needed.")
                break

            try:
                next_btn.click()
                page.wait_for_load_state("networkidle")
            except PWTimeout:
                print("[!] Timeout waiting for next page – stopping.")
                break

        browser.close()

    return all_questions


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    questions = scrape_course()
    print(f"\n[+] Total unique questions collected: {len(questions)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"[+] Saved to: {OUTPUT_FILE}")
    print("[*] Run quiz_generator.py to generate the HTML quiz.")
