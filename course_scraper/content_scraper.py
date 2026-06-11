"""
PCNSP Full Course Content Scraper
-----------------------------------
Goes through every slide/page of every SCORM course in the PCNSP learning
plan and copies all visible text content – headings, body text, bullets,
tabs, and accordion panels.

This gives a complete picture of every course so that weekly_planner.py
can build a study schedule tailored to the actual material.

Output: course_content.json

Usage
-----
    python content_scraper.py

Credentials (same as scraper.py):
    export PALO_EMAIL="you@example.com"
    export PALO_PASSWORD="your-password"
    HEADLESS=true python content_scraper.py   # no browser window
"""

import json
import os
import re
import time

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EMAIL    = os.environ.get("PALO_EMAIL", "")
PASSWORD = os.environ.get("PALO_PASSWORD", "")
HEADLESS = os.environ.get("HEADLESS", "false").lower() == "true"

LEARNING_PLAN_URL = (
    "https://learn.paloaltonetworks.com/learn/learning-plans/341"
    "/palo-alto-networks-certified-network-security-professional"
)
COURSE_URL_PREFIX = "https://learn.paloaltonetworks.com/learn/learning-plans/341/"
LOGIN_URL   = "https://learn.paloaltonetworks.com/learn/signin"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "course_content.json")

DEFAULT_TIMEOUT    = 20_000
MANUAL_TIMEOUT     = 60_000
MAX_PAGES_PER_COURSE = 300   # safety limit – most courses are under 60 slides

# Lines to discard: pure navigation chrome, status banners, etc.
_NOISE = re.compile(
    r"^(Next|Previous|Back|Continue|Submit|Close|Menu|Home|Skip|"
    r"Page \d+ of \d+|\d+ of \d+|Loading\.\.\.|Please wait\.?|"
    r"Replay|Restart|Retake|Resume|Launch|Start course|Begin|"
    r"You have completed this lesson|There is no (previous|next) lesson"
    r"|Content status:.*|Content type:.*)$",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def login(page) -> None:
    print("[*] Logging in …")
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    page.fill('input[type="email"], input[name="email"], input[id*="email"]', EMAIL)
    page.fill('input[type="password"], input[name="password"], input[id*="password"]', PASSWORD)
    page.click(
        'button[type="submit"], input[type="submit"], '
        'button:has-text("Sign in"), button:has-text("Log in")'
    )
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    print("[+] Logged in")


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def _lines_from_frame(frame) -> list[str]:
    """Return all non-noise text lines from one frame/page context."""
    lines = []
    selectors = [
        "h1", "h2", "h3", "h4",
        "p", "li", "td", "th",
        "[class*='text']", "[class*='content']",
        "[class*='slide-text']", "[class*='body']",
        "span", "label", "figcaption",
    ]
    for sel in selectors:
        try:
            for el in frame.query_selector_all(sel):
                txt = el.inner_text().strip()
                if txt and len(txt) >= 4 and not _NOISE.match(txt):
                    lines.append(txt)
        except Exception:
            continue
    return lines


def extract_slide_content(page) -> dict:
    """
    Collect all meaningful text from the current state of the browser,
    including the main frame and every child iframe (SCORM lives in iframes).
    Returns {headings, body, raw} after deduplication.
    """
    raw: list[str] = []
    raw.extend(_lines_from_frame(page))
    for frame in page.frames:
        if frame == page.main_frame:
            continue
        raw.extend(_lines_from_frame(frame))

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for line in raw:
        key = " ".join(line.split()).lower()
        if key not in seen and len(key) >= 4:
            seen.add(key)
            unique.append(line)

    # Rough split: short title-like lines vs body text
    headings = [l for l in unique
                if len(l) <= 120 and not l.endswith((".", ",", ";"))
                and re.match(r"^[A-Z0-9\"\(]", l)]
    body = [l for l in unique if l not in headings]

    return {"headings": headings[:20], "body": body[:80], "raw": unique}


# ---------------------------------------------------------------------------
# Interactive element expansion
# ---------------------------------------------------------------------------

def expand_interactive(page) -> None:
    """
    Click tabs, accordions, and collapsed panels to surface hidden content
    before we scrape the slide.
    """
    expand_sels = [
        "[aria-expanded='false']",
        "[class*='tab']:not([class*='active'])",
        "[class*='accordion']",
        "button[class*='expand']",
        "[class*='toggle']:not([class*='active'])",
        "details:not([open]) > summary",
    ]
    for ctx in [page] + list(page.frames):
        for sel in expand_sels:
            try:
                for el in (ctx.query_selector_all(sel) or [])[:6]:
                    if el.is_visible():
                        el.click()
                        time.sleep(0.25)
            except Exception:
                continue


# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------

def _find_button(page, labels: list[str]):
    """Return the first visible button or link matching any of the labels."""
    for label in labels:
        for sel in [
            f"button:has-text('{label}')",
            f"a:has-text('{label}')",
            f"[aria-label*='{label}' i]",
            f"[title*='{label}' i]",
        ]:
            try:
                el = page.query_selector(sel)
                if el and el.is_visible():
                    return el
            except Exception:
                continue
    return None


def _page_indicator(page) -> str:
    """Read a 'N / M' or 'Page N of M' progress indicator from any frame."""
    patterns = [
        re.compile(r"Page\s+(\d+)\s*(?:of|/)\s*(\d+)", re.I),
        re.compile(r"\b(\d{1,3})\s*(?:of|/)\s*(\d{1,3})\b"),
    ]
    for ctx in [page] + list(page.frames):
        try:
            text = ctx.inner_text("body")
        except Exception:
            continue
        for pat in patterns:
            m = pat.search(text)
            if m and int(m.group(2)) <= MAX_PAGES_PER_COURSE:
                return f"{m.group(1)}/{m.group(2)}"
    return ""


# ---------------------------------------------------------------------------
# SCORM launch
# ---------------------------------------------------------------------------

def _launch_scorm(page, context):
    """
    Click the Start / Launch / Resume button and return the page that
    contains the SCORM content (same page, or a popup window).
    Returns the original page if no launch button is found.
    """
    launch_labels = ["Start", "Launch", "Resume", "Begin", "Open", "Continue"]
    btn = _find_button(page, launch_labels)
    if btn is None:
        return page

    # Watch for a new popup tab before clicking
    try:
        with context.expect_page(timeout=6000) as new_page_evt:
            btn.click()
        new_pg = new_page_evt.value
        new_pg.wait_for_load_state("domcontentloaded", timeout=DEFAULT_TIMEOUT)
        time.sleep(2)
        return new_pg
    except Exception:
        # No popup – content loaded inline / in an iframe
        time.sleep(2)
        return page


# ---------------------------------------------------------------------------
# Per-course scraping
# ---------------------------------------------------------------------------

def scrape_course(page, context, course_url: str) -> dict:
    """
    Navigate every slide in a single SCORM course and return structured data.
    """
    print(f"  URL: {course_url}")
    try:
        page.goto(course_url, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
        page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)
    except Exception as e:
        print(f"  [!] Load failed: {e}")
        return {}

    time.sleep(2)

    # Grab the page title before launching SCORM
    course_title = ""
    for sel in ["h1", "h2", "[class*='course-title']", "[class*='title']"]:
        try:
            el = page.query_selector(sel)
            if el:
                t = el.inner_text().strip()
                if t and len(t) < 200:
                    course_title = t
                    break
        except Exception:
            continue

    scorm_page = _launch_scorm(page, context)
    time.sleep(3)

    slides: list[dict] = []
    seen_indicators: set[str] = set()
    page_num = 0

    for _ in range(MAX_PAGES_PER_COURSE):
        time.sleep(1)

        # Expand collapsed content before scraping
        expand_interactive(scorm_page)
        time.sleep(0.4)

        content   = extract_slide_content(scorm_page)
        indicator = _page_indicator(scorm_page)
        page_num += 1

        slide_entry = {
            "page":      page_num,
            "indicator": indicator,
            "headings":  content["headings"],
            "body":      content["body"],
        }
        slides.append(slide_entry)

        snippet = content["raw"][0][:70] if content["raw"] else "(empty)"
        print(f"    [{page_num:3d}] {indicator:8s}  {snippet}")

        # Stop if the indicator loops (end of course)
        if indicator and indicator in seen_indicators:
            print("  [*] Loop detected – course complete")
            break
        if indicator:
            seen_indicators.add(indicator)

        # Check for "course complete" signals
        try:
            body_text = scorm_page.inner_text("body").lower()
            if any(s in body_text for s in [
                "you have completed this lesson",
                "course complete",
                "congratulations",
                "end of course",
            ]):
                # Grab the final slide text then stop
                next_btn = _find_button(scorm_page, ["Next", "Continue"])
                if next_btn is None:
                    print("  [*] Completion message found – done")
                    break
        except Exception:
            pass

        # Advance to next slide
        next_btn = _find_button(scorm_page, ["Next", "Continue", "→"])
        if next_btn is None:
            print("  [*] No Next button – end of course")
            break
        try:
            next_btn.click()
            try:
                scorm_page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                time.sleep(2)
        except Exception as e:
            print(f"  [!] Next click failed: {e}")
            break

    # Close popup window if SCORM opened one
    if scorm_page is not page:
        try:
            scorm_page.close()
        except Exception:
            pass

    return {
        "title":       course_title,
        "url":         course_url,
        "slide_count": len(slides),
        "slides":      slides,
    }


# ---------------------------------------------------------------------------
# Course URL discovery
# ---------------------------------------------------------------------------

def collect_course_urls(page) -> list[str]:
    """
    Collect all unique SCORM course URLs from the learning plan page.
    Excludes assessment pages (they have separate URLs with 'assessment' or
    are reached via the same course URL with a different path).
    """
    try:
        links = page.eval_on_selector_all(
            "a[href]",
            "els => els.map(a => a.href).filter(Boolean)"
        )
    except Exception:
        return []

    course_re = re.compile(r"/courses/\d+/")
    seen: set[str] = set()
    out: list[str] = []
    for href in links:
        if not href.startswith(COURSE_URL_PREFIX):
            continue
        if not course_re.search(href):
            continue
        norm = href.split("?")[0].split("#")[0].rstrip("/")
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
    return out


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def scrape_all_courses() -> list[dict]:
    all_courses: list[dict] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page    = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)

        if not EMAIL or not PASSWORD:
            print(
                "[!] No credentials found.\n"
                "    Set PALO_EMAIL and PALO_PASSWORD, or log in manually.\n"
                "    The browser will open the login page."
            )
            try:
                page.goto(LOGIN_URL, wait_until="domcontentloaded")
            except Exception as e:
                print(f"[!] {e}")
            input("\n    >> Log in in the browser, then press ENTER here … ")
            page.set_default_timeout(MANUAL_TIMEOUT)
            time.sleep(5)
        else:
            login(page)

        print(f"\n[*] Loading learning plan …")
        try:
            page.goto(LEARNING_PLAN_URL, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"[!] {e}")
            time.sleep(5)

        time.sleep(3)
        course_urls = collect_course_urls(page)
        print(f"[+] Found {len(course_urls)} course URLs\n")

        for i, url in enumerate(course_urls, 1):
            print(f"[{i}/{len(course_urls)}] Scraping …")
            data = scrape_course(page, context, url)
            if data:
                all_courses.append(data)
                print(
                    f"    ✓ {data.get('title', '(no title)')!r}"
                    f"  –  {data.get('slide_count', 0)} slides\n"
                )

        browser.close()

    return all_courses


if __name__ == "__main__":
    results = scrape_all_courses()
    print(f"\n[+] Scraped {len(results)} courses total")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[+] Saved full content to: {OUTPUT_FILE}")
    print("[*] Run weekly_planner.py to generate your study schedule.")
