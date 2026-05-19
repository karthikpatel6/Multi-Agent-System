import streamlit as st
import time
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Pipeline",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg:       #080c14;
    --surface:  #0f1724;
    --border:   #1d2d44;
    --accent:   #00d4aa;
    --accent2:  #0090ff;
    --warn:     #f59e0b;
    --danger:   #ef4444;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --card-bg:  #111927;
}

html, body, [class*="css"], .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1400px; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Hero ── */
.hero { padding: 2.5rem 0 2rem; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem; }
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; letter-spacing: 0.25em; color: var(--accent);
    text-transform: uppercase; margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 4vw, 3.4rem); font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent) 60%, var(--accent2) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0;
}
.hero-sub {
    color: var(--muted); font-size: 1rem; font-weight: 300;
    margin-top: 0.75rem; max-width: 540px; line-height: 1.6;
}

/* ── Input card ── */
.input-card {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 16px; padding: 1.75rem 2rem; margin-bottom: 2rem;
}

/* ── Text inputs ── */
.stTextInput > div > div > input {
    background: #0a1220 !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-family: 'Inter', sans-serif !important; font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important; transition: border-color .2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,.12) !important;
}
.stTextInput label { color: var(--muted) !important; font-size: 0.8rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, #00a88a 100%) !important;
    color: #000 !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    border: none !important; border-radius: 10px !important;
    padding: 0.75rem 2.2rem !important; letter-spacing: 0.04em !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,212,170,.35) !important;
}
.stDownloadButton > button {
    background: transparent !important; border: 1px solid var(--accent) !important;
    color: var(--accent) !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; border-radius: 8px !important;
    padding: 0.5rem 1.4rem !important; transition: all .2s !important;
}
.stDownloadButton > button:hover { background: rgba(0,212,170,.1) !important; }

/* ── Pipeline tracker ── */
.pipeline-track {
    display: flex; align-items: center;
    margin: 2rem 0; padding: 1.5rem 2rem;
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 16px; overflow-x: auto; gap: 0;
}
.step-node {
    display: flex; flex-direction: column; align-items: center;
    flex: 1; min-width: 90px; position: relative;
}
.step-node:not(:last-child)::after {
    content: ''; position: absolute; top: 20px;
    left: calc(50% + 22px); width: calc(100% - 44px);
    height: 2px; background: var(--border);
}
.step-node.done:not(:last-child)::after  { background: var(--accent); }
.step-icon {
    width: 44px; height: 44px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; border: 2px solid var(--border);
    background: var(--surface); z-index: 1; transition: all .4s;
}
.step-node.done   .step-icon { border-color: var(--accent);  background: rgba(0,212,170,.15); }
.step-node.active .step-icon { border-color: var(--accent2); background: rgba(0,144,255,.15); animation: pulse 1.5s infinite; }
.step-node.idle   .step-icon { opacity: 0.4; }
@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0   rgba(0,144,255,.5); }
    50%      { box-shadow: 0 0 0 10px rgba(0,144,255,.0); }
}
.step-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.62rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-top: 0.5rem; text-align: center; color: var(--muted);
}
.step-node.done   .step-label { color: var(--accent); }
.step-node.active .step-label { color: var(--accent2); }

/* ── Stat chips ── */
.stat-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
.stat-chip {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 8px; padding: 0.5rem 1rem;
    font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--muted);
    display: flex; align-items: center; gap: 0.4rem;
}
.stat-chip span { color: var(--text); font-weight: 500; }

/* ── Result cards ── */
.result-card {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 14px; padding: 1.6rem; margin-bottom: 1.25rem;
}
.result-card.accent-border { border-left: 3px solid var(--accent); }
.result-card.blue-border   { border-left: 3px solid var(--accent2); }
.result-card.warn-border   { border-left: 3px solid var(--warn); }
.card-header {
    display: flex; align-items: center; gap: 0.6rem;
    margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border);
}
.card-title { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 700; }
.card-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.15em;
    text-transform: uppercase; padding: 0.2rem 0.6rem; border-radius: 20px;
    background: rgba(0,212,170,.1); color: var(--accent);
    border: 1px solid rgba(0,212,170,.2); margin-left: auto;
}
.card-badge.blue { background: rgba(0,144,255,.1); color: var(--accent2); border-color: rgba(0,144,255,.2); }
.card-badge.warn { background: rgba(245,158,11,.1); color: var(--warn);   border-color: rgba(245,158,11,.2); }
.card-content {
    font-size: 0.875rem; line-height: 1.8; color: #b8c9e1;
    white-space: pre-wrap; word-break: break-word;
    max-height: 400px; overflow-y: auto; padding-right: 0.4rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card-bg) !important; border-radius: 10px !important;
    padding: 4px !important; border: 1px solid var(--border) !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 7px !important;
    color: var(--muted) !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
    padding: 0.5rem 1.2rem !important; border: none !important; transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,170,.2), rgba(0,144,255,.15)) !important;
    color: var(--text) !important; border: 1px solid var(--accent) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--card-bg) !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Sidebar misc ── */
.hist-item {
    padding: 0.7rem 0.9rem; border: 1px solid var(--border); border-radius: 8px;
    margin-bottom: 0.5rem; background: var(--bg); transition: all .2s;
}
.hist-item:hover { border-color: var(--accent); background: rgba(0,212,170,.05); }
.hist-topic { font-family: 'Syne', sans-serif; font-size: 0.82rem; font-weight: 600; }
.hist-time  { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--muted); margin-top: 0.2rem; }

/* ── Divider ── */
.divider { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 1.5rem 0; }

/* ── Alert ── */
.alert-error {
    background: rgba(239,68,68,.1); border: 1px solid rgba(239,68,68,.3);
    border-left: 3px solid var(--danger); border-radius: 10px;
    padding: 1rem 1.25rem; color: #fca5a5; font-size: 0.88rem; margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = dict(running=False, results=None, error=None,
                    current_step=0, history=[], topic="", elapsed=0.0)
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search",  "Tavily web search"),
    ("📖", "Read",    "Scrape top source"),
    ("✍️",  "Write",   "Draft the report"),
    ("🧐", "Critic",  "Quality review"),
]


# ─────────────────────────────────────────────────────────────────────────────
# COMPONENT HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def render_tracker(current: int):
    """current: 0=idle, 1-4=active step, 5=done."""
    nodes = ""
    for i, (icon, label, _) in enumerate(STEPS):
        n = i + 1
        cls = "done" if n < current else ("active" if n == current and current < 5 else
              "done" if current == 5 else "idle")
        nodes += f"""
        <div class="step-node {cls}">
            <div class="step-icon">{icon}</div>
            <div class="step-label">{label}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-track">{nodes}</div>', unsafe_allow_html=True)


def render_stat_chips(results: dict, elapsed: float):
    chips = [
        ("⏱", "Time",    f"{elapsed:.1f}s"),
        ("📝", "Words",   f"{len(results.get('report','').split()):,}"),
        ("🔎", "Search",  f"{len(results.get('search_results','')):,} chars"),
        ("🌐", "Scraped", f"{len(results.get('scraped_content','')):,} chars"),
    ]
    html = '<div class="stat-row">' + "".join(
        f'<div class="stat-chip">{ic} {lb}: <span>{vl}</span></div>'
        for ic, lb, vl in chips) + "</div>"
    st.markdown(html, unsafe_allow_html=True)


def result_card(icon, title, badge, content, border="accent-border", badge_cls=""):
    esc = content.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    st.markdown(f"""
    <div class="result-card {border}">
        <div class="card-header">
            <span>{icon}</span>
            <span class="card-title">{title}</span>
            <span class="card-badge {badge_cls}">{badge}</span>
        </div>
        <div class="card-content">{esc}</div>
    </div>""", unsafe_allow_html=True)


def extract_score(text: str):
    import re
    m = re.search(r"Score[:\s]+(\d+(?:\.\d+)?)\s*/\s*10", text, re.I)
    return m.group(1) if m else None


def build_markdown_export(topic, results):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""# Research Report — {topic}
*Generated {ts} · ResearchMind AI Pipeline*

---

## Report

{results.get('report','')}

---

## Critic Feedback

{results.get('feedback','')}

---

## Raw Search Results

{results.get('search_results','')}

---

## Scraped Content

{results.get('scraped_content','')}
"""


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE RUNNER  (step-by-step to update tracker between stages)
# ─────────────────────────────────────────────────────────────────────────────
def run_stepwise(topic: str, status_placeholder):
    from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
    state = {}
    t0 = time.time()

    # Step 1
    st.session_state.current_step = 1
    with status_placeholder.status("🔍  Searching the web…", expanded=True) as s:
        agent = build_search_agent()
        r = agent.invoke({"messages": [("user",
            f"Find recent, reliable and detailed information about: {topic}")]})
        state["search_results"] = r["messages"][-1].content
        s.update(label="✅  Search complete", state="complete", expanded=False)

    # Step 2
    st.session_state.current_step = 2
    with status_placeholder.status("📖  Reading & scraping…", expanded=True) as s:
        agent = build_reader_agent()
        r = agent.invoke({"messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}")]})
        state["scraped_content"] = r["messages"][-1].content
        s.update(label="✅  Content scraped", state="complete", expanded=False)

    # Step 3
    st.session_state.current_step = 3
    with status_placeholder.status("✍️  Writing the report…", expanded=True) as s:
        research = (f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}\n\n")
        state["report"] = writer_chain.invoke({"topic": topic, "research": research})
        s.update(label="✅  Report drafted", state="complete", expanded=False)

    # Step 4
    st.session_state.current_step = 4
    with status_placeholder.status("🧐  Reviewing quality…", expanded=True) as s:
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        s.update(label="✅  Review complete", state="complete", expanded=False)

    st.session_state.current_step = 5
    st.session_state.elapsed = time.time() - t0
    return state


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 .5rem'>
        <div style='font-family:"JetBrains Mono",monospace;font-size:.6rem;
                    letter-spacing:.2em;text-transform:uppercase;color:#00d4aa'>
            ResearchMind
        </div>
        <div style='font-family:"Syne",sans-serif;font-size:1.3rem;font-weight:800'>
            AI Pipeline
        </div>
        <div style='font-size:.73rem;color:#64748b;margin-top:.25rem'>
            Mistral · Tavily · LangChain
        </div>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ How it works", expanded=False):
        for i, (icon, label, desc) in enumerate(STEPS, 1):
            st.markdown(f"""
            <div style='display:flex;gap:.7rem;align-items:flex-start;margin-bottom:.75rem'>
                <div style='font-size:1.1rem'>{icon}</div>
                <div>
                    <div style='font-family:"Syne",sans-serif;font-size:.82rem;font-weight:700'>
                        {i}. {label}
                    </div>
                    <div style='font-size:.73rem;color:#64748b'>{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family:"JetBrains Mono",monospace;font-size:.6rem;
                letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:.75rem'>
        Recent Searches
    </div>""", unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            "<div style='font-size:.75rem;color:#64748b;font-style:italic'>No searches yet.</div>",
            unsafe_allow_html=True)
    else:
        for entry in reversed(st.session_state.history[-8:]):
            trunc = entry["topic"][:32] + ("…" if len(entry["topic"]) > 32 else "")
            st.markdown(f"""
            <div class="hist-item">
                <div class="hist-topic">🔬 {trunc}</div>
                <div class="hist-time">{entry['time']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("🗑  Clear results", use_container_width=True):
        st.session_state.results = None
        st.session_state.error   = None
        st.session_state.current_step = 0
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN — HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent Research System</div>
    <h1 class="hero-title">ResearchMind</h1>
    <p class="hero-sub">
        Search → Read → Write → Critique.<br>
        Four AI agents, one polished research report.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
col_in, col_btn = st.columns([5, 1], vertical_alignment="bottom")

with col_in:
    topic_input = st.text_input(
        "Topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025  ·  GPT-5 release impact  ·  CRISPR gene therapy",
        label_visibility="collapsed",
        key="topic_field",
    )

with col_btn:
    run_btn = st.button(
        "⚡  Run",
        use_container_width=True,
        disabled=st.session_state.running,
    )

st.markdown("</div>", unsafe_allow_html=True)

# Trigger
if run_btn:
    if not topic_input.strip():
        st.markdown(
            '<div class="alert-error">⚠️ Please enter a research topic before running.</div>',
            unsafe_allow_html=True)
    else:
        st.session_state.running      = True
        st.session_state.results      = None
        st.session_state.error        = None
        st.session_state.current_step = 0
        st.session_state.topic        = topic_input.strip()
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# RUNNING
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.running:
    topic = st.session_state.topic
    render_tracker(st.session_state.current_step)
    status_slot = st.empty()

    try:
        results = run_stepwise(topic, status_slot)
        st.session_state.results = results
        st.session_state.running = False
        st.session_state.history.append({
            "topic": topic,
            "time":  datetime.now().strftime("%d %b %H:%M"),
        })
    except Exception as e:
        st.session_state.error        = str(e)
        st.session_state.running      = False
        st.session_state.current_step = 0

    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ERROR
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(
        f'<div class="alert-error">❌ <strong>Pipeline error:</strong> {st.session_state.error}</div>',
        unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.results and not st.session_state.running:
    results = st.session_state.results
    topic   = st.session_state.topic

    render_tracker(5)
    render_stat_chips(results, st.session_state.elapsed)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    tab_report, tab_search, tab_scraped, tab_critic = st.tabs([
        "📄  Final Report",
        "🔍  Search Results",
        "🌐  Scraped Content",
        "🧐  Critic Feedback",
    ])

    # ── Report tab ──────────────────────────────────────────────────────────
    with tab_report:
        dl_col, _ = st.columns([1, 5])
        with dl_col:
            st.download_button(
                "⬇  Download .md",
                data=build_markdown_export(topic, results),
                file_name=f"report_{topic[:30].replace(' ','_')}.md",
                mime="text/markdown",
            )

        report_text = results.get("report", "No report generated.")
        word_count  = len(report_text.split())

        st.markdown(f"""
        <div class="result-card accent-border" style="margin-top:1rem">
            <div class="card-header">
                <span>📄</span>
                <span class="card-title">Research Report — {topic}</span>
                <span class="card-badge">{word_count:,} words</span>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
<div style='background:var(--card-bg);border:1px solid var(--border);
            border-left:3px solid #00d4aa;border-radius:14px;
            padding:1.8rem 2.2rem;line-height:1.9;color:#cdd9ec;font-size:.9rem;'>

{report_text}

</div>""", unsafe_allow_html=True)

    # ── Search tab ──────────────────────────────────────────────────────────
    with tab_search:
        result_card("🔍", "Web Search Results", "STEP 1 · Tavily",
                    results.get("search_results", "No search results."),
                    "accent-border", "")

    # ── Scraped tab ─────────────────────────────────────────────────────────
    with tab_scraped:
        result_card("🌐", "Scraped Source Content", "STEP 2 · BeautifulSoup",
                    results.get("scraped_content", "No scraped content."),
                    "blue-border", "blue")

    # ── Critic tab ──────────────────────────────────────────────────────────
    with tab_critic:
        feedback = results.get("feedback", "No feedback.")
        score    = extract_score(feedback)

        if score:
            try:
                val = float(score)
                pct = val / 10 * 100
                col_r, col_f = st.columns([1, 4])
            except ValueError:
                score = None

        if score:
            with col_r:
                color = "#00d4aa" if val >= 7 else ("#f59e0b" if val >= 5 else "#ef4444")
                st.markdown(f"""
                <div style='display:flex;flex-direction:column;align-items:center;
                            justify-content:center;padding:2rem 1rem;gap:.6rem;'>
                    <div style='font-family:"JetBrains Mono",monospace;font-size:.58rem;
                                letter-spacing:.15em;text-transform:uppercase;color:#64748b'>
                        Quality Score
                    </div>
                    <div style='font-family:"Syne",sans-serif;font-size:4rem;
                                font-weight:800;color:{color};line-height:1'>
                        {score}
                    </div>
                    <div style='font-size:.78rem;color:#64748b'>out of 10</div>
                    <div style='width:80px;height:6px;background:var(--border);
                                border-radius:3px;overflow:hidden;margin-top:.4rem'>
                        <div style='height:100%;width:{pct:.0f}%;background:{color};
                                    border-radius:3px'></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            with col_f:
                result_card("🧐", "Critic Evaluation", "STEP 4 · Mistral",
                            feedback, "warn-border", "warn")
        else:
            result_card("🧐", "Critic Evaluation", "STEP 4 · Mistral",
                        feedback, "warn-border", "warn")


# ─────────────────────────────────────────────────────────────────────────────
# IDLE LANDING
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.results and not st.session_state.running and not st.session_state.error:
    render_tracker(0)

    st.markdown("""
    <div style='text-align:center;padding:3.5rem 1rem'>
        <div style='font-size:3.5rem;margin-bottom:1rem;filter:drop-shadow(0 0 20px rgba(0,212,170,.3))'>🧠</div>
        <div style='font-family:"Syne",sans-serif;font-size:1.15rem;font-weight:700;
                    color:#e2e8f0;margin-bottom:.6rem'>
            Ready to research anything
        </div>
        <div style='color:#64748b;font-size:.875rem;max-width:380px;margin:auto;line-height:1.7'>
            Type a topic above and hit <strong style="color:#00d4aa">Run</strong>.
            Four agents will search, scrape, write and critique — then hand you a polished report.
        </div>
    </div>
    """, unsafe_allow_html=True)
