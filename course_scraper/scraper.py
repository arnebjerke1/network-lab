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
from collections import deque
from urllib.parse import urlparse, urlunparse

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EMAIL = os.environ.get("PALO_EMAIL", "")
PASSWORD = os.environ.get("PALO_PASSWORD", "")
HEADLESS = os.environ.get("HEADLESS", "false").lower() == "true"

LEARNING_PLAN_URL = (
    "https://learn.paloaltonetworks.com/learn/learning-plans/341"
    "/palo-alto-networks-certified-network-security-professional"
)
# First course in the learning plan – used as an additional seed URL
COURSE_URL = (
    "https://learn.paloaltonetworks.com/learn/learning-plans/341"
    "/palo-alto-networks-certified-network-security-professional"
    "/courses/2297/network-security-netsec-professional"
)
# Only follow links that stay within this learning plan
COURSE_URL_PREFIX = "https://learn.paloaltonetworks.com/learn/learning-plans/341/"
LOGIN_URL = "https://learn.paloaltonetworks.com/learn/signin"

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "questions.json")

# How long (ms) to wait for elements before giving up on a page
DEFAULT_TIMEOUT = 15_000
# Longer timeout used after manual login – complex LMS pages need more time to settle
MANUAL_TIMEOUT = 60_000
MAX_PAGES_TO_VISIT = 400


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


def normalize_url(url: str) -> str:
    """Normalize URL to avoid revisiting the same page with query/hash variants."""
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", ""))


def question_key(question_text: str) -> str:
    """Normalize question text for robust deduplication."""
    return " ".join(question_text.split()).strip().lower()


def collect_course_links(page) -> list[str]:
    """Collect course-related links from the current page."""
    try:
        links = page.eval_on_selector_all(
            "a[href]",
            """
            anchors => anchors
                .map(a => a.href)
                .filter(Boolean)
            """
        )
    except Exception:
        return []

    out = []
    for href in links:
        # Only follow links that stay within the specific learning plan (plan ID 341)
        if not href.startswith(COURSE_URL_PREFIX):
            continue
        if "/learn/sign" in href:
            continue
        normalized = normalize_url(href)
        if normalized:
            out.append(normalized)
    return out


def is_course_page(url: str) -> bool:
    """True when URL belongs to the target learning plan."""
    return normalize_url(url).startswith(COURSE_URL_PREFIX.rstrip("/"))


def navigate_to_course_page(page, url: str, retries: int = 3) -> bool:
    """Navigate robustly, tolerating auth redirects and interrupted navigations."""
    target = normalize_url(url)
    for attempt in range(1, retries + 1):
        try:
            page.goto(target, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle")
            except Exception:
                time.sleep(2)
        except Exception as e:
            if attempt == retries:
                print(f"[!] Error loading page {target}: {e}")
                return False
            time.sleep(1)

        current = normalize_url(page.url)
        if current == target or is_course_page(current):
            return True

        # If auth flow redirected us, wait a bit and retry target once authenticated.
        time.sleep(2)

    return is_course_page(page.url)


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


def get_next_button_selector(page):
    """Return selector for a visible 'Next'/'Continue' button/link, or None."""
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
            if page.locator(selector).first.is_visible():
                return selector
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
            try:
                page.goto(LOGIN_URL, wait_until="domcontentloaded")
            except Exception as e:
                print(f"[!] Could not open login page: {e}")
            input("    >> Press ENTER here after you have logged in manually … ")
            # Be more patient after manual login – the LMS page can be slow to settle
            page.set_default_timeout(MANUAL_TIMEOUT)
            # Give the LMS session a moment to fully settle after manual login
            time.sleep(5)
        else:
            login(page)

        print(f"[*] Navigating to learning plan: {LEARNING_PLAN_URL}")
        if not navigate_to_course_page(page, LEARNING_PLAN_URL):
            print("[!] Could not reach learning plan reliably; continuing with seed URLs.")

        # Seed the queue with the learning plan page and the first course URL
        queue = deque([normalize_url(page.url), normalize_url(COURSE_URL)])
        for link in collect_course_links(page):
            queue.append(link)

        visited_pages: set[str] = set()
        page_number = 0

        while queue and len(visited_pages) < MAX_PAGES_TO_VISIT:
            next_url = queue.popleft()
            if next_url in visited_pages:
                continue

            if not navigate_to_course_page(page, next_url):
                continue

            current_url = normalize_url(page.url)
            if current_url in visited_pages:
                continue

            visited_pages.add(current_url)
            page_number += 1
            print(f"[{page_number}] {current_url}")

            # Give dynamic content time to render
            time.sleep(2)

            questions = extract_questions_from_page(page)

            for q in questions:
                key = question_key(q["question"])
                if key not in seen_questions:
                    seen_questions.add(key)
                    all_questions.append(q)
                    print(f"    + Question collected: {q['question'][:70]} …")

            for discovered in collect_course_links(page):
                if discovered not in visited_pages:
                    queue.append(discovered)

            next_selector = get_next_button_selector(page)
            if next_selector is None:
                continue

            try:
                before = normalize_url(page.url)
                btn = page.locator(next_selector).first
                btn.scroll_into_view_if_needed()
                btn.click(timeout=5_000, force=True)
                try:
                    page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"[!] networkidle wait after Next click failed (continuing): {e}")
                    time.sleep(3)
                after = normalize_url(page.url)
                if after != before and after not in visited_pages:
                    queue.appendleft(after)
            except Exception as e:
                print(f"[!] Error clicking Next button with Playwright click: {e}")
                try:
                    before = normalize_url(page.url)
                    page.locator(next_selector).first.evaluate("el => el.click()")
                    time.sleep(2)
                    after = normalize_url(page.url)
                    if after != before and after not in visited_pages:
                        queue.appendleft(after)
                except Exception as fallback_error:
                    print(f"[!] Error clicking Next button with JS fallback: {fallback_error}")

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
