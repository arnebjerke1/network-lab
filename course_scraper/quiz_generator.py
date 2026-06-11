"""
Quiz Generator
--------------
Reads questions.json (produced by scraper.py) and generates a standalone
HTML quiz file.

Each question shows exactly 4 answer alternatives.
- Click the correct answer  → button turns GREEN  ✓
- Click a wrong answer      → button turns RED    ✗ (and the correct one turns green)

Usage
-----
    python quiz_generator.py                      # reads questions.json, writes quiz.html
    python quiz_generator.py my_questions.json    # custom input file
"""

import json
import os
import random
import sys
from html import escape

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_FILE  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCRIPT_DIR, "questions.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "quiz.html")


# ---------------------------------------------------------------------------
# Load & validate questions
# ---------------------------------------------------------------------------

def load_questions(path: str) -> list[dict]:
    if not os.path.exists(path):
        print(f"[!] Input file not found: {path}")
        print("    Run scraper.py first to generate questions.json")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    valid = []
    for i, q in enumerate(data):
        question = (q.get("question") or "").strip()
        choices   = [str(c).strip() for c in q.get("choices", []) if str(c).strip()]
        correct_raw = q.get("correct")
        if isinstance(correct_raw, list):
            correct = [str(c).strip() for c in correct_raw if str(c).strip()]
        else:
            cv = (str(correct_raw) if correct_raw is not None else "").strip()
            correct = [cv] if cv else []

        if not question or not choices or not correct:
            print(f"[!] Skipping question {i+1}: missing question, choices, or correct answer")
            continue

        # Ensure all correct answers are among the choices
        for c in correct:
            if c not in choices:
                choices.append(c)

        if len(correct) > 1:
            # Multi-select: keep all choices, just shuffle
            random.shuffle(choices)
            four_choices = choices
        else:
            # Single correct: keep exactly 4 choices
            wrong = [c for c in choices if c != correct[0]]
            random.shuffle(wrong)
            four_choices = [correct[0]] + wrong[:3]
            random.shuffle(four_choices)

        valid.append({
            "question": question,
            "choices":  four_choices,
            "correct":  correct,
        })

    return valid


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="no">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PCNSP Quiz</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}

    body {{
      font-family: "Segoe UI", Arial, sans-serif;
      background: #0f1923;
      color: #e8eaf0;
      margin: 0;
      padding: 20px;
      min-height: 100vh;
    }}

    header {{
      text-align: center;
      margin-bottom: 36px;
    }}
    header h1 {{
      font-size: 1.8rem;
      color: #fa582d;
      letter-spacing: 1px;
      margin: 0 0 6px;
    }}
    header p {{
      color: #8892a4;
      margin: 0;
      font-size: 0.95rem;
    }}

    #progress-bar-wrap {{
      background: #1e2b38;
      border-radius: 8px;
      height: 8px;
      margin: 0 auto 32px;
      max-width: 700px;
      overflow: hidden;
    }}
    #progress-bar {{
      height: 100%;
      background: #fa582d;
      width: 0%;
      transition: width 0.4s ease;
      border-radius: 8px;
    }}

    #quiz-container {{
      max-width: 700px;
      margin: 0 auto;
    }}

    .question-card {{
      display: none;
      background: #1a2533;
      border-radius: 14px;
      padding: 32px 28px 24px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.4);
      animation: fadeIn 0.3s ease;
    }}
    .question-card.active {{ display: block; }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}

    .question-number {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #fa582d;
      margin-bottom: 10px;
    }}

    .question-text {{
      font-size: 1.12rem;
      line-height: 1.6;
      margin-bottom: 26px;
      color: #dce3ed;
    }}

    .choices {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}

    .choice-btn {{
      background: #243040;
      border: 2px solid #2e3f54;
      color: #dce3ed;
      border-radius: 10px;
      padding: 14px 16px;
      font-size: 0.97rem;
      line-height: 1.4;
      cursor: pointer;
      text-align: left;
      transition: background 0.15s, border-color 0.15s, transform 0.1s;
      word-break: break-word;
    }}
    .choice-btn:hover:not(:disabled) {{
      background: #2d3f56;
      border-color: #fa582d;
      transform: translateY(-2px);
    }}

    .choice-btn.correct {{
      background: #0e4a2a !important;
      border-color: #27ae60 !important;
      color: #5ddb96 !important;
      cursor: default;
    }}
    .choice-btn.wrong {{
      background: #4a0e0e !important;
      border-color: #e74c3c !important;
      color: #f08080 !important;
      cursor: default;
    }}
    .choice-btn:disabled {{
      cursor: default;
    }}

    .choice-btn.selected {{
      background: #2d4a6e !important;
      border-color: #5b9bd5 !important;
      color: #a8d1f7 !important;
    }}

    .multi-choices {{
      grid-template-columns: 1fr;
    }}

    .check-btn {{
      background: #2e3f54;
      color: #dce3ed;
      border: 2px solid #4a6080;
      border-radius: 8px;
      padding: 11px 24px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      margin-right: 10px;
      transition: background 0.15s, transform 0.1s;
    }}
    .check-btn:hover:not(:disabled) {{ background: #3a5070; transform: translateY(-1px); }}
    .check-btn:disabled {{ cursor: default; opacity: 0.6; }}

    .feedback {{
      margin-top: 18px;
      min-height: 24px;
      font-size: 0.95rem;
      font-weight: 600;
      text-align: center;
    }}
    .feedback.correct {{ color: #27ae60; }}
    .feedback.wrong   {{ color: #e74c3c; }}

    .nav-row {{
      display: flex;
      justify-content: flex-end;
      margin-top: 22px;
    }}
    .next-btn {{
      background: #fa582d;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 11px 28px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      display: none;
      transition: background 0.15s, transform 0.1s;
    }}
    .next-btn:hover {{ background: #e04420; transform: translateY(-1px); }}

    #result-card {{
      display: none;
      text-align: center;
      background: #1a2533;
      border-radius: 14px;
      padding: 48px 28px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.4);
      animation: fadeIn 0.4s ease;
    }}
    #result-card h2 {{
      font-size: 2rem;
      color: #fa582d;
      margin-bottom: 12px;
    }}
    #result-card .score-text {{
      font-size: 1.25rem;
      color: #dce3ed;
      margin-bottom: 8px;
    }}
    #result-card .score-pct {{
      font-size: 3rem;
      font-weight: 700;
      color: #27ae60;
      margin: 12px 0 28px;
    }}
    #restart-btn {{
      background: #fa582d;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 13px 36px;
      font-size: 1.05rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s;
    }}
    #restart-btn:hover {{ background: #e04420; }}

    @media (max-width: 520px) {{
      .choices {{ grid-template-columns: 1fr; }}
      header h1 {{ font-size: 1.35rem; }}
    }}
  </style>
</head>
<body>

<header>
  <h1>🔐 PCNSP Quiz</h1>
  <p>Palo Alto Networks Certified Network Security Professional</p>
</header>

<div id="progress-bar-wrap"><div id="progress-bar"></div></div>

<div id="quiz-container">
{question_cards}
  <div id="result-card">
    <h2>Quiz fullført! 🎉</h2>
    <div class="score-text">Du svarte riktig på <span id="correct-count">0</span> av <span id="total-count">0</span> spørsmål</div>
    <div class="score-pct" id="score-pct">0%</div>
    <button id="restart-btn" onclick="restartQuiz()">Ta quizen på nytt</button>
  </div>
</div>

<script>
  const TOTAL = {total};
  let current = 0;
  let score   = 0;

  function showQuestion(index) {{
    document.querySelectorAll(".question-card").forEach(c => c.classList.remove("active"));
    const card = document.getElementById("q" + index);
    if (card) card.classList.add("active");
    document.getElementById("progress-bar").style.width =
      (index / TOTAL * 100) + "%";
  }}

  function answer(qIndex, btnEl, isCorrect, correctBtnId) {{
    // Disable all buttons in this question
    const card = document.getElementById("q" + qIndex);
    card.querySelectorAll(".choice-btn").forEach(b => b.disabled = true);

    const feedback = card.querySelector(".feedback");
    const nextBtn  = card.querySelector(".next-btn");

    if (isCorrect) {{
      btnEl.classList.add("correct");
      feedback.textContent = "✓ Riktig!";
      feedback.className   = "feedback correct";
      score++;
    }} else {{
      btnEl.classList.add("wrong");
      document.getElementById(correctBtnId).classList.add("correct");
      feedback.textContent = "✗ Feil – riktig svar er vist i grønt";
      feedback.className   = "feedback wrong";
    }}

    nextBtn.style.display = "inline-block";
  }}

  function nextQuestion(index) {{
    if (index >= TOTAL) {{
      showResult();
    }} else {{
      current = index;
      showQuestion(current);
    }}
  }}

  function showResult() {{
    document.querySelectorAll(".question-card").forEach(c => c.classList.remove("active"));
    const rc = document.getElementById("result-card");
    rc.style.display = "block";
    document.getElementById("correct-count").textContent = score;
    document.getElementById("total-count").textContent   = TOTAL;
    const pct = Math.round(score / TOTAL * 100);
    const pctEl = document.getElementById("score-pct");
    pctEl.textContent = pct + "%";
    pctEl.style.color = pct >= 80 ? "#27ae60" : pct >= 50 ? "#f39c12" : "#e74c3c";
    document.getElementById("progress-bar").style.width = "100%";
  }}

  function restartQuiz() {{
    score   = 0;
    current = 0;
    document.getElementById("result-card").style.display = "none";

    // Reset all cards
    document.querySelectorAll(".question-card").forEach(card => {{
      card.querySelectorAll(".choice-btn").forEach(b => {{
        b.disabled = false;
        b.classList.remove("correct", "wrong", "selected");
      }});
      const cb = card.querySelector(".check-btn");
      if (cb) {{ cb.disabled = false; }}
      const fb = card.querySelector(".feedback");
      if (fb) {{ fb.textContent = ""; fb.className = "feedback"; }}
      const nb = card.querySelector(".next-btn");
      if (nb) nb.style.display = "none";
    }});

    showQuestion(0);
  }}

  function toggleChoice(qIndex, btnEl) {{
    if (!btnEl.disabled) {{
      btnEl.classList.toggle("selected");
    }}
  }}

  function checkMulti(qIndex, correctIndices) {{
    const card     = document.getElementById("q" + qIndex);
    const buttons  = Array.from(card.querySelectorAll(".choice-btn"));
    const feedback = card.querySelector(".feedback");
    const nextBtn  = card.querySelector(".next-btn");
    const checkBtn = card.querySelector(".check-btn");

    buttons.forEach(b => b.disabled = true);
    if (checkBtn) checkBtn.disabled = true;

    const correctSet  = new Set(correctIndices);
    const selectedSet = new Set(
      buttons.map((b, j) => b.classList.contains("selected") ? j : -1).filter(j => j >= 0)
    );

    buttons.forEach((b, j) => {{
      if (correctSet.has(j)) {{
        b.classList.add("correct");
      }} else if (selectedSet.has(j)) {{
        b.classList.add("wrong");
      }}
      b.classList.remove("selected");
    }});

    const isCorrect = correctIndices.length === selectedSet.size &&
      correctIndices.every(i => selectedSet.has(i));

    if (isCorrect) {{
      feedback.textContent = "✓ Riktig!";
      feedback.className   = "feedback correct";
      score++;
    }} else {{
      feedback.textContent = "✗ Feil – riktige svar er vist i grønt";
      feedback.className   = "feedback wrong";
    }}

    nextBtn.style.display = "inline-block";
  }}

  showQuestion(0);
</script>
</body>
</html>
"""

CARD_TEMPLATE = """\
  <div class="question-card{active}" id="q{index}">
    <div class="question-number">Spørsmål {num} av {total}</div>
    <div class="question-text">{question}</div>
    <div class="choices">
{buttons}
    </div>
    <div class="feedback"></div>
    <div class="nav-row">
      <button class="next-btn" onclick="nextQuestion({next_index})">
        {next_label} →
      </button>
    </div>
  </div>
"""

BUTTON_TEMPLATE = (
    '      <button class="choice-btn" id="{btn_id}" '
    'onclick="answer({q_index}, this, {is_correct}, \'{correct_btn_id}\')">'
    '{text}</button>'
)

MULTI_CARD_TEMPLATE = """\
  <div class="question-card{active}" id="q{index}">
    <div class="question-number">Spørsmål {num} av {total}</div>
    <div class="question-text">{question}</div>
    <div class="choices multi-choices">
{buttons}
    </div>
    <div class="feedback"></div>
    <div class="nav-row">
      <button class="check-btn" id="check{index}" onclick="checkMulti({index}, {correct_indices})">
        Sjekk svar
      </button>
      <button class="next-btn" onclick="nextQuestion({next_index})">
        {next_label} →
      </button>
    </div>
  </div>
"""

MULTI_BUTTON_TEMPLATE = (
    '      <button class="choice-btn" id="{btn_id}" '
    'onclick="toggleChoice({q_index}, this)">'
    '{text}</button>'
)


# ---------------------------------------------------------------------------
# Build HTML
# ---------------------------------------------------------------------------

def build_html(questions: list[dict]) -> str:
    total = len(questions)
    cards_html = ""

    for i, q in enumerate(questions):
        is_last    = (i == total - 1)
        next_index = i + 1
        next_label = "Se resultat" if is_last else "Neste"
        is_multi   = len(q["correct"]) > 1

        if is_multi:
            correct_indices = [q["choices"].index(c) for c in q["correct"]]
            buttons_html = ""
            for j, choice in enumerate(q["choices"]):
                btn_id = f"q{i}b{j}"
                buttons_html += MULTI_BUTTON_TEMPLATE.format(
                    btn_id=btn_id,
                    q_index=i,
                    text=escape(choice),
                ) + "\n"

            cards_html += MULTI_CARD_TEMPLATE.format(
                active=" active" if i == 0 else "",
                index=i,
                num=i + 1,
                total=total,
                question=escape(q["question"]),
                buttons=buttons_html.rstrip(),
                correct_indices=correct_indices,
                next_index=next_index,
                next_label=next_label,
            )
        else:
            correct_val    = q["correct"][0]
            correct_btn_id = f"q{i}b{q['choices'].index(correct_val)}"

            buttons_html = ""
            for j, choice in enumerate(q["choices"]):
                btn_id     = f"q{i}b{j}"
                is_correct = "true" if choice == correct_val else "false"
                buttons_html += BUTTON_TEMPLATE.format(
                    btn_id=btn_id,
                    q_index=i,
                    is_correct=is_correct,
                    correct_btn_id=correct_btn_id,
                    text=escape(choice),
                ) + "\n"

            cards_html += CARD_TEMPLATE.format(
                active=" active" if i == 0 else "",
                index=i,
                num=i + 1,
                total=total,
                question=escape(q["question"]),
                buttons=buttons_html.rstrip(),
                next_index=next_index,
                next_label=next_label,
            )

    return HTML_TEMPLATE.format(
        question_cards=cards_html,
        total=total,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"[*] Loading questions from: {INPUT_FILE}")
    questions = load_questions(INPUT_FILE)
    print(f"[+] {len(questions)} valid questions loaded")

    if not questions:
        print("[!] No valid questions found – nothing to generate.")
        sys.exit(1)

    html = build_html(questions)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] Quiz saved to: {OUTPUT_FILE}")
    print("    Open it in your browser to start the quiz.")
