"""
Schedule Generator
------------------
Reads schedule.json (from weekly_planner.py) and generates:
  - schedule.html      – interactive week-by-week study dashboard
  - quiz_week_N.html   – one standalone quiz per week (uses quiz_generator.py)

Usage
-----
    python schedule_generator.py
"""

import json
import os
import sys

SCRIPT_DIR    = os.path.dirname(__file__)
SCHEDULE_FILE = os.path.join(SCRIPT_DIR, "schedule.json")
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "progress.json")
SCHEDULE_HTML = os.path.join(SCRIPT_DIR, "schedule.html")

# Import quiz generation logic from sibling module
sys.path.insert(0, SCRIPT_DIR)
try:
    from quiz_generator import load_questions as _load_qs, build_html as _build_quiz_html
    _QUIZ_GEN_AVAILABLE = True
except ImportError:
    _QUIZ_GEN_AVAILABLE = False


# ---------------------------------------------------------------------------
# Per-week quiz HTML
# ---------------------------------------------------------------------------

def generate_week_quizzes(schedule: dict) -> None:
    if not _QUIZ_GEN_AVAILABLE:
        print("[!] quiz_generator.py not importable – skipping quiz HTML generation")
        return
    for week in schedule["weeks"]:
        n    = week["week"]
        path = os.path.join(SCRIPT_DIR, f"questions_week_{n}.json")
        if not os.path.exists(path):
            print(f"  [!] {os.path.basename(path)} not found – run weekly_planner.py first")
            continue
        qs   = _load_qs(path)
        if not qs:
            print(f"  [!] Week {n}: no valid questions, skipping quiz")
            continue
        html = _build_quiz_html(qs)
        out  = os.path.join(SCRIPT_DIR, f"quiz_week_{n}.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Week {n}: {len(qs)} questions → quiz_week_{n}.html")


# ---------------------------------------------------------------------------
# schedule.html template pieces
# ---------------------------------------------------------------------------

_HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PCNSP Study Plan</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }

    body {
      font-family: "Segoe UI", Arial, sans-serif;
      background: #0f1923;
      color: #e8eaf0;
      margin: 0;
      padding: 0 0 60px;
      min-height: 100vh;
    }

    /* ── Header ── */
    header {
      background: #141f2b;
      border-bottom: 2px solid #fa582d;
      padding: 22px 32px 18px;
    }
    header h1 { font-size: 1.6rem; color: #fa582d; margin: 0 0 4px; }
    header p  { color: #8892a4; margin: 0; font-size: 0.92rem; }

    /* ── Overview stats ── */
    #overview {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      padding: 20px 32px 0;
    }
    .stat-card {
      background: #1a2533;
      border-radius: 10px;
      padding: 14px 22px;
      min-width: 130px;
      text-align: center;
    }
    .stat-card .stat-num {
      font-size: 1.8rem;
      font-weight: 700;
      color: #fa582d;
      display: block;
    }
    .stat-card .stat-label {
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #8892a4;
    }

    /* ── Week tabs ── */
    #week-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 24px 32px 0;
    }
    .tab-btn {
      background: #1a2533;
      border: 2px solid #2e3f54;
      color: #8892a4;
      border-radius: 8px;
      padding: 8px 18px;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.15s;
    }
    .tab-btn:hover  { border-color: #fa582d; color: #e8eaf0; }
    .tab-btn.active { background: #fa582d; border-color: #fa582d; color: #fff; font-weight: 600; }
    .tab-done { position: relative; }
    .tab-done::after {
      content: "✓";
      font-size: 0.65rem;
      position: absolute;
      top: -4px;
      right: -4px;
      background: #27ae60;
      color: #fff;
      border-radius: 50%;
      width: 14px; height: 14px;
      display: flex; align-items: center; justify-content: center;
    }

    /* ── Week panel ── */
    .week-panel { display: none; padding: 28px 32px 0; max-width: 820px; }
    .week-panel.active { display: block; }

    .week-header h2 {
      font-size: 1.35rem;
      color: #fa582d;
      margin: 0 0 6px;
    }
    .week-header .theme-desc {
      color: #8892a4;
      font-size: 0.9rem;
      margin: 0 0 16px;
    }
    .week-meta {
      display: flex;
      gap: 20px;
      font-size: 0.85rem;
      color: #8892a4;
      margin-bottom: 18px;
      flex-wrap: wrap;
    }
    .week-meta span { color: #dce3ed; }

    /* ── Week progress bar ── */
    .week-progress-wrap {
      background: #1e2b38;
      border-radius: 6px;
      height: 6px;
      margin-bottom: 22px;
      overflow: hidden;
    }
    .week-progress-bar {
      height: 100%;
      background: #27ae60;
      border-radius: 6px;
      transition: width 0.4s ease;
    }

    /* ── Course cards ── */
    .course-card {
      background: #1a2533;
      border-radius: 12px;
      margin-bottom: 12px;
      overflow: hidden;
      border: 1px solid #2e3f54;
      transition: border-color 0.15s;
    }
    .course-card.done { border-color: #27ae60; }

    .course-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 14px 18px;
      cursor: pointer;
      user-select: none;
    }
    .course-header:hover { background: #1f2f40; }

    .course-checkbox {
      width: 18px; height: 18px;
      accent-color: #27ae60;
      cursor: pointer;
      flex-shrink: 0;
    }
    .course-title-text {
      flex: 1;
      font-size: 1rem;
      font-weight: 600;
      color: #dce3ed;
    }
    .course-card.done .course-title-text { color: #5ddb96; }

    .duration-badge {
      background: #243040;
      border: 1px solid #2e3f54;
      border-radius: 6px;
      padding: 3px 10px;
      font-size: 0.78rem;
      color: #8892a4;
      white-space: nowrap;
    }
    .status-badge {
      font-size: 0.72rem;
      border-radius: 6px;
      padding: 3px 8px;
      white-space: nowrap;
    }
    .status-completed { background: #0e4a2a; color: #5ddb96; }
    .status-progress  { background: #3a2800; color: #f39c12; }
    .status-failed    { background: #4a0e0e; color: #f08080; }
    .status-none      { background: #243040; color: #8892a4; }

    .expand-arrow {
      color: #8892a4;
      font-size: 0.8rem;
      transition: transform 0.2s;
      flex-shrink: 0;
    }
    .course-card.open .expand-arrow { transform: rotate(90deg); }

    .course-body {
      display: none;
      padding: 0 18px 16px 48px;
      border-top: 1px solid #2e3f54;
    }
    .course-card.open .course-body { display: block; }

    .course-body h4 {
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #fa582d;
      margin: 14px 0 8px;
    }
    .course-body ul {
      margin: 0 0 4px;
      padding-left: 18px;
    }
    .course-body li {
      font-size: 0.9rem;
      color: #b0bbc8;
      margin-bottom: 4px;
      line-height: 1.5;
    }

    /* ── Quiz section ── */
    .quiz-section {
      background: #141f2b;
      border: 1px solid #2e3f54;
      border-radius: 12px;
      padding: 20px 22px;
      margin-top: 20px;
    }
    .quiz-section h3 {
      font-size: 1rem;
      color: #fa582d;
      margin: 0 0 6px;
    }
    .quiz-section p {
      color: #8892a4;
      font-size: 0.88rem;
      margin: 0 0 14px;
    }
    .quiz-link {
      display: inline-block;
      background: #fa582d;
      color: #fff;
      border-radius: 8px;
      padding: 10px 24px;
      font-weight: 600;
      font-size: 0.95rem;
      text-decoration: none;
      transition: background 0.15s;
      margin-right: 14px;
    }
    .quiz-link:hover { background: #e04420; }
    .quiz-link.unavailable {
      background: #2e3f54;
      color: #8892a4;
      pointer-events: none;
    }

    .score-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 14px;
      flex-wrap: wrap;
    }
    .score-row label { font-size: 0.88rem; color: #8892a4; }
    .score-input {
      background: #243040;
      border: 1px solid #2e3f54;
      color: #e8eaf0;
      border-radius: 6px;
      padding: 6px 10px;
      width: 70px;
      font-size: 0.95rem;
      text-align: center;
    }
    .score-input:focus { outline: none; border-color: #fa582d; }
    .score-pct {
      font-weight: 700;
      font-size: 1.05rem;
    }
    .save-score-btn {
      background: #2e3f54;
      border: none;
      color: #dce3ed;
      border-radius: 6px;
      padding: 7px 16px;
      cursor: pointer;
      font-size: 0.88rem;
    }
    .save-score-btn:hover { background: #3a4f68; }

    /* ── Weak topics ── */
    .weak-topics-box {
      display: none;
      background: #2d1a00;
      border: 1px solid #c0590a;
      border-radius: 10px;
      padding: 14px 18px;
      margin-top: 14px;
    }
    .weak-topics-box h4 {
      color: #f39c12;
      margin: 0 0 8px;
      font-size: 0.92rem;
    }
    .weak-topics-box p {
      color: #c9a060;
      font-size: 0.85rem;
      margin: 0;
    }

    /* ── Separator ── */
    .section-sep {
      border: none;
      border-top: 1px solid #2e3f54;
      margin: 24px 0;
    }

    @media (max-width: 580px) {
      header, #overview, #week-tabs, .week-panel { padding-left: 16px; padding-right: 16px; }
      .week-meta { flex-direction: column; gap: 4px; }
    }
  </style>
</head>
<body>

<header>
  <h1>🎓 PCNSP Personalised Study Plan</h1>
  <p>Palo Alto Networks Certified Network Security Professional</p>
</header>

<div id="overview">
  <div class="stat-card">
    <span class="stat-num" id="ov-weeks">–</span>
    <span class="stat-label">Weeks</span>
  </div>
  <div class="stat-card">
    <span class="stat-num" id="ov-courses">–</span>
    <span class="stat-label">Courses</span>
  </div>
  <div class="stat-card">
    <span class="stat-num" id="ov-questions">–</span>
    <span class="stat-label">Quiz Questions</span>
  </div>
  <div class="stat-card">
    <span class="stat-num" id="ov-done">0%</span>
    <span class="stat-label">Completed</span>
  </div>
</div>

<div id="week-tabs"></div>
<div id="week-panels"></div>

<script>
"""

# The JS data + logic is inserted between _HTML_HEAD and _HTML_FOOT
_HTML_FOOT = """\

</script>
</body>
</html>
"""

_JS_LOGIC = r"""
// ── Utility ──────────────────────────────────────────────────────────────────

function esc(s) {
  return String(s)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;")
    .replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

function statusBadge(status) {
  const s = (status || "").toLowerCase();
  if (s.includes("complet")) return `<span class="status-badge status-completed">✓ Completed</span>`;
  if (s.includes("progress")) return `<span class="status-badge status-progress">⏳ In Progress</span>`;
  if (s.includes("fail"))     return `<span class="status-badge status-failed">✗ Failed</span>`;
  return `<span class="status-badge status-none">Not started</span>`;
}

// ── State (localStorage) ─────────────────────────────────────────────────────

function saveState(key, val) {
  try { localStorage.setItem("pcnsp_" + key, JSON.stringify(val)); } catch(e) {}
}
function loadState(key, def) {
  try {
    const v = localStorage.getItem("pcnsp_" + key);
    return v !== null ? JSON.parse(v) : def;
  } catch(e) { return def; }
}

// completedCourses: Set of "weekNum|courseId" strings
// weekScores:       { "1": {score, total}, ... }
let completedCourses = new Set(loadState("completed", []));
let weekScores       = loadState("scores", {});

function persistCompleted() { saveState("completed", [...completedCourses]); }
function persistScores()    { saveState("scores", weekScores); }

// ── Render ────────────────────────────────────────────────────────────────────

function renderOverview() {
  const totalCourses = SCHEDULE.total_courses;
  const totalWeeks   = SCHEDULE.weeks.length;
  const totalQs      = SCHEDULE.total_questions;
  document.getElementById("ov-weeks").textContent    = totalWeeks;
  document.getElementById("ov-courses").textContent  = totalCourses;
  document.getElementById("ov-questions").textContent = totalQs;
  updateOverallProgress();
}

function updateOverallProgress() {
  const totalCourses = SCHEDULE.total_courses || 1;
  const done         = completedCourses.size;
  const pct          = Math.round(done / totalCourses * 100);
  document.getElementById("ov-done").textContent = pct + "%";
}

function renderTabs() {
  const container = document.getElementById("week-tabs");
  container.innerHTML = SCHEDULE.weeks.map(w => {
    const allIds = w.courses.map(c => w.week + "|" + c.id);
    const allDone = allIds.length > 0 && allIds.every(k => completedCourses.has(k));
    return `<button class="tab-btn${allDone ? " tab-done" : ""}"
              id="tab-${w.week}" onclick="showWeek(${w.week})">
              Wk ${w.week}
            </button>`;
  }).join("");
}

function renderWeekPanel(w) {
  const wNum      = w.week;
  const doneIds   = w.courses.map(c => wNum + "|" + c.id).filter(k => completedCourses.has(k));
  const donePct   = w.courses.length ? Math.round(doneIds.length / w.courses.length * 100) : 0;
  const scoreData = weekScores[String(wNum)];
  const quizFile  = `quiz_week_${wNum}.html`;
  const hasQuiz   = w.question_count > 0;

  const coursesHtml = w.courses.map(c => {
    const key  = wNum + "|" + c.id;
    const done = completedCourses.has(key);

    const objHtml = (c.objectives || []).length
      ? `<h4>Objectives</h4><ul>${c.objectives.map(o => `<li>${esc(o)}</li>`).join("")}</ul>`
      : "";
    const lesHtml = (c.lessons || []).length
      ? `<h4>Lessons</h4><ul>${c.lessons.map(l => `<li>${esc(l)}</li>`).join("")}</ul>`
      : "";

    return `
      <div class="course-card${done ? " done" : ""}" id="card-${wNum}-${c.id}">
        <div class="course-header" onclick="toggleCard(${wNum},'${c.id}',event)">
          <input class="course-checkbox" type="checkbox" ${done ? "checked" : ""}
            onclick="event.stopPropagation(); toggleDone(${wNum},'${c.id}',this)">
          <span class="course-title-text">${esc(c.title)}</span>
          ${statusBadge(c.status)}
          <span class="duration-badge">~${c.duration_minutes || 25} min</span>
          <span class="expand-arrow">▶</span>
        </div>
        <div class="course-body">
          ${objHtml}
          ${lesHtml}
        </div>
      </div>`;
  }).join("");

  // Score display
  let scorePctHtml = "";
  if (scoreData) {
    const pct = Math.round(scoreData.score / (scoreData.total || 1) * 100);
    const col = pct >= 80 ? "#27ae60" : pct >= 60 ? "#f39c12" : "#e74c3c";
    scorePctHtml = `<span class="score-pct" style="color:${col}">${scoreData.score}/${scoreData.total} (${pct}%)</span>`;
  }

  // Weak topics warning
  let weakHtml = "";
  if (scoreData) {
    const pct = Math.round(scoreData.score / (scoreData.total || 1) * 100);
    if (pct < 70) {
      weakHtml = `
        <div class="weak-topics-box" id="weak-${wNum}" style="display:block">
          <h4>⚠ Score below 70% – extra review recommended</h4>
          <p>Re-read the course material for Week ${wNum} and retake the quiz before moving to Week ${wNum + 1}.</p>
        </div>`;
    }
  }

  return `
    <div class="week-panel" id="panel-${wNum}">
      <div class="week-header">
        <h2>Week ${wNum}: ${esc(w.title)}</h2>
        <p class="theme-desc">${esc(w.theme_desc)}</p>
      </div>
      <div class="week-meta">
        <div>Content: <span>${w.content_minutes} min</span></div>
        <div>Review: <span>${w.recap_minutes} min</span></div>
        <div>Total: <span>~${w.total_minutes} min</span></div>
        <div>Courses: <span>${doneIds.length}/${w.courses.length} done</span></div>
      </div>
      <div class="week-progress-wrap">
        <div class="week-progress-bar" id="wpbar-${wNum}" style="width:${donePct}%"></div>
      </div>

      ${coursesHtml}

      <hr class="section-sep">

      <div class="quiz-section">
        <h3>End-of-Week Self-Test</h3>
        <p>${hasQuiz ? w.question_count + " questions covering this week&apos;s topics" : "No quiz questions mapped to this week yet"}</p>
        <a href="${quizFile}" class="quiz-link${hasQuiz ? "" : " unavailable"}" target="_blank">
          Take Week ${wNum} Quiz →
        </a>
        <div class="score-row">
          <label>My score:</label>
          <input class="score-input" type="number" min="0" max="${w.question_count}"
            id="score-input-${wNum}" value="${scoreData ? scoreData.score : ""}"
            placeholder="0">
          <span style="color:#8892a4">/ ${w.question_count}</span>
          <button class="save-score-btn" onclick="saveScore(${wNum},${w.question_count})">Save</button>
          ${scorePctHtml}
        </div>
        ${weakHtml}
      </div>
    </div>`;
}

function renderAllPanels() {
  document.getElementById("week-panels").innerHTML =
    SCHEDULE.weeks.map(renderWeekPanel).join("");
}

// ── Interactions ──────────────────────────────────────────────────────────────

function showWeek(n) {
  document.querySelectorAll(".week-panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  const panel = document.getElementById("panel-" + n);
  const tab   = document.getElementById("tab-"   + n);
  if (panel) panel.classList.add("active");
  if (tab)   tab.classList.add("active");
}

function toggleCard(weekNum, courseId, evt) {
  // Don't toggle if clicking the checkbox itself
  if (evt.target.type === "checkbox") return;
  const card = document.getElementById(`card-${weekNum}-${courseId}`);
  if (card) card.classList.toggle("open");
}

function toggleDone(weekNum, courseId, checkbox) {
  const key  = weekNum + "|" + courseId;
  const card = document.getElementById(`card-${weekNum}-${courseId}`);
  if (checkbox.checked) {
    completedCourses.add(key);
    card && card.classList.add("done");
  } else {
    completedCourses.delete(key);
    card && card.classList.remove("done");
  }
  persistCompleted();
  updateWeekProgress(weekNum);
  updateOverallProgress();
  renderTabs();
}

function updateWeekProgress(weekNum) {
  const week = SCHEDULE.weeks.find(w => w.week === weekNum);
  if (!week) return;
  const done = week.courses.filter(c => completedCourses.has(weekNum + "|" + c.id)).length;
  const pct  = week.courses.length ? Math.round(done / week.courses.length * 100) : 0;
  const bar  = document.getElementById(`wpbar-${weekNum}`);
  const meta = document.querySelector(`#panel-${weekNum} .week-meta`);
  if (bar) bar.style.width = pct + "%";
  if (meta) {
    const el = meta.querySelectorAll("div")[3];
    if (el) el.innerHTML = `Courses: <span>${done}/${week.courses.length} done</span>`;
  }
}

function saveScore(weekNum, total) {
  const inp = document.getElementById(`score-input-${weekNum}`);
  if (!inp) return;
  const score = parseInt(inp.value, 10);
  if (isNaN(score) || score < 0 || score > total) {
    inp.style.borderColor = "#e74c3c";
    setTimeout(() => inp.style.borderColor = "", 1500);
    return;
  }
  weekScores[String(weekNum)] = { score, total };
  persistScores();

  // Refresh this panel in place
  const week = SCHEDULE.weeks.find(w => w.week === weekNum);
  if (!week) return;
  const container = document.getElementById("week-panels");
  const oldPanel  = document.getElementById("panel-" + weekNum);
  const wasActive = oldPanel && oldPanel.classList.contains("active");
  if (oldPanel) oldPanel.outerHTML = renderWeekPanel(week);
  if (wasActive) showWeek(weekNum);
}

// ── Boot ──────────────────────────────────────────────────────────────────────

renderOverview();
renderTabs();
renderAllPanels();
showWeek(1);
"""


# ---------------------------------------------------------------------------
# Build schedule.html
# ---------------------------------------------------------------------------

def build_schedule_html(schedule: dict) -> str:
    data_js = (
        "const SCHEDULE = "
        + json.dumps(schedule, ensure_ascii=False)
        + ";\n"
    )
    return _HTML_HEAD + data_js + _JS_LOGIC + _HTML_FOOT


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.path.exists(SCHEDULE_FILE):
        print(f"[!] {SCHEDULE_FILE} not found – run weekly_planner.py first")
        sys.exit(1)

    with open(SCHEDULE_FILE, encoding="utf-8") as f:
        schedule = json.load(f)

    print("[*] Generating per-week quiz files …")
    generate_week_quizzes(schedule)

    print("[*] Building schedule.html …")
    html = build_schedule_html(schedule)
    with open(SCHEDULE_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Dashboard saved to: {SCHEDULE_HTML}")
    print("    Open schedule.html in your browser to start studying.")
