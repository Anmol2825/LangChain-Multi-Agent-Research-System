import streamlit as st
import time

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Researcher AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

* {
    box-sizing: border-box;
}

html, body {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(56, 189, 248, 0.12),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(139, 92, 246, 0.12),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #050b14 0%,
            #07111f 50%,
            #050a12 100%
        );

    color: #f8fafc;
}

/* Subtle background grid */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;

    background-image:
        linear-gradient(
            rgba(255,255,255,0.018) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(255,255,255,0.018) 1px,
            transparent 1px
        );

    background-size: 60px 60px;

    mask-image: linear-gradient(
        to bottom,
        black,
        transparent 75%
    );

    z-index: 0;
}

#MainMenu,
header,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1250px;
    padding: 1.2rem 2rem 5rem;
}


/* ============================================================
   NAVBAR
   ============================================================ */

.top-nav {
    height: 52px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-bottom: 1px solid rgba(255,255,255,0.06);

    margin-bottom: 3rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;

    font-family: "Space Grotesk", sans-serif;

    font-size: 16px;
    font-weight: 700;

    color: #f8fafc;
}

.brand-mark {
    width: 30px;
    height: 30px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 9px;

    background:
        linear-gradient(
            135deg,
            #38bdf8,
            #8b5cf6
        );

    box-shadow:
        0 0 25px rgba(56,189,248,0.25);

    font-size: 15px;
}

.nav-status {
    display: flex;
    align-items: center;
    gap: 7px;

    font-family: "DM Mono", monospace;

    font-size: 10px;

    letter-spacing: 0.08em;

    text-transform: uppercase;

    color: #64748b;
}

.status-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 12px rgba(34,197,94,0.8);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;

    padding: 1rem 0 3.5rem;
}

.hero-badge {
    display: inline-flex;

    align-items: center;

    padding: 7px 13px;

    margin-bottom: 22px;

    border-radius: 999px;

    border: 1px solid rgba(56,189,248,0.2);

    background: rgba(56,189,248,0.06);

    color: #7dd3fc;

    font-family: "DM Mono", monospace;

    font-size: 10px;

    letter-spacing: 0.12em;

    text-transform: uppercase;
}

.hero h1 {
    margin: 0;

    font-family: "Space Grotesk", sans-serif;

    font-size: clamp(55px, 8vw, 92px);

    line-height: 0.95;

    letter-spacing: -0.065em;

    font-weight: 700;

    color: #f8fafc;
}

.hero h1 .gradient {
    background:
        linear-gradient(
            110deg,
            #38bdf8,
            #818cf8,
            #c084fc
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 620px;

    margin: 24px auto 0;

    color: #8b9bb0;

    font-size: 16px;

    line-height: 1.7;

    font-weight: 300;
}


/* ============================================================
   INPUT CARD
   ============================================================ */

.research-card {
    padding: 28px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.018)
        );

    border: 1px solid rgba(255,255,255,0.09);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.28);

    backdrop-filter: blur(20px);
}

.card-label {
    font-family: "DM Mono", monospace;

    font-size: 10px;

    color: #38bdf8;

    letter-spacing: 0.16em;

    text-transform: uppercase;

    margin-bottom: 8px;
}

.card-title {
    font-family: "Space Grotesk", sans-serif;

    font-size: 24px;

    font-weight: 600;

    color: #f8fafc;

    margin-bottom: 7px;
}

.card-description {
    color: #64748b;

    font-size: 13px;

    line-height: 1.6;

    margin-bottom: 22px;
}


/* ============================================================
   TEXT INPUT
   ============================================================ */

.stTextInput {
    margin-bottom: 10px;
}

.stTextInput label {
    display: none !important;
}

.stTextInput > div > div > input {

    height: 54px !important;

    background: rgba(2,7,15,0.8) !important;

    color: #f8fafc !important;

    border: 1px solid rgba(148,163,184,0.16) !important;

    border-radius: 13px !important;

    font-family: "DM Sans", sans-serif !important;

    font-size: 14px !important;

    padding: 0 16px !important;
}

.stTextInput > div > div > input:focus {

    border-color: rgba(56,189,248,0.55) !important;

    box-shadow:
        0 0 0 3px rgba(56,189,248,0.08) !important;
}

.stTextInput input::placeholder {
    color: #475569 !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton {
    margin-top: 8px;
}

.stButton > button {

    width: 100%;

    height: 54px;

    border-radius: 13px !important;

    border: none !important;

    background:
        linear-gradient(
            135deg,
            #0ea5e9,
            #6366f1
        ) !important;

    color: white !important;

    font-family: "Space Grotesk", sans-serif !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    box-shadow:
        0 12px 35px rgba(14,165,233,0.18);

    transition: all 0.2s ease !important;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 18px 45px rgba(14,165,233,0.28);
}


/* ============================================================
   EXAMPLES
   ============================================================ */

.example-label {

    margin-top: 20px;

    margin-bottom: 9px;

    font-family: "DM Mono", monospace;

    font-size: 9px;

    color: #475569;

    letter-spacing: 0.14em;

    text-transform: uppercase;
}

.example-chip {

    display: inline-block;

    padding: 7px 10px;

    margin: 3px 4px 3px 0;

    border-radius: 8px;

    background: rgba(255,255,255,0.025);

    border: 1px solid rgba(255,255,255,0.07);

    color: #94a3b8;

    font-size: 11px;
}


/* ============================================================
   PIPELINE
   ============================================================ */

.pipeline-heading {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 15px;
}

.pipeline-title {

    font-family: "Space Grotesk", sans-serif;

    font-size: 18px;

    font-weight: 600;

    color: #f8fafc;
}

.pipeline-count {

    font-family: "DM Mono", monospace;

    font-size: 9px;

    color: #475569;

    letter-spacing: 0.12em;
}


/* ============================================================
   AGENT CARD
   ============================================================ */

.agent-card {

    display: flex;

    align-items: center;

    gap: 13px;

    min-height: 70px;

    padding: 12px 14px;

    margin-bottom: 7px;

    border-radius: 14px;

    background: rgba(255,255,255,0.025);

    border: 1px solid rgba(255,255,255,0.07);

    position: relative;

    overflow: hidden;
}

.agent-card.active {

    background:
        linear-gradient(
            90deg,
            rgba(56,189,248,0.09),
            rgba(56,189,248,0.02)
        );

    border-color: rgba(56,189,248,0.3);

    box-shadow:
        0 0 25px rgba(56,189,248,0.05);
}

.agent-card.active::before {

    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 3px;

    background: #38bdf8;
}

.agent-card.done {

    background:
        linear-gradient(
            90deg,
            rgba(34,197,94,0.07),
            rgba(34,197,94,0.015)
        );

    border-color: rgba(34,197,94,0.2);
}

.agent-card.done::before {

    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 3px;

    background: #22c55e;
}

.agent-icon {

    width: 38px;
    height: 38px;

    flex-shrink: 0;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.07);

    color: #cbd5e1;

    font-size: 15px;
}

.agent-info {
    min-width: 0;
}

.agent-name {

    font-family: "Space Grotesk", sans-serif;

    font-size: 13px;

    font-weight: 600;

    color: #e2e8f0;
}

.agent-desc {

    margin-top: 3px;

    font-size: 10px;

    color: #64748b;
}

.agent-status {

    margin-left: auto;

    font-family: "DM Mono", monospace;

    font-size: 8px;

    letter-spacing: 0.08em;

    color: #475569;
}

.agent-status.active {
    color: #38bdf8;
}

.agent-status.done {
    color: #22c55e;
}


/* ============================================================
   PIPELINE CONNECTOR
   ============================================================ */

.pipeline-connector {

    height: 10px;

    width: 1px;

    margin-left: 33px;

    background:
        linear-gradient(
            to bottom,
            rgba(56,189,248,0.25),
            rgba(255,255,255,0.04)
        );
}


/* ============================================================
   RESULTS
   ============================================================ */

.section-divider {

    height: 1px;

    margin: 55px 0 35px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(56,189,248,0.25),
            transparent
        );
}

.results-heading {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 18px;
}

.results-title {

    font-family: "Space Grotesk", sans-serif;

    font-size: 28px;

    font-weight: 600;

    color: #f8fafc;
}

.results-subtitle {

    font-family: "DM Mono", monospace;

    font-size: 9px;

    color: #475569;

    letter-spacing: 0.12em;

    text-transform: uppercase;
}


/* ============================================================
   REPORT
   ============================================================ */

.report-card {

    padding: 30px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(56,189,248,0.06),
            rgba(139,92,246,0.035),
            rgba(255,255,255,0.018)
        );

    border: 1px solid rgba(56,189,248,0.17);

    box-shadow:
        0 30px 80px rgba(0,0,0,0.22);
}

.report-label {

    display: flex;

    align-items: center;

    gap: 10px;

    font-family: "DM Mono", monospace;

    font-size: 10px;

    color: #38bdf8;

    letter-spacing: 0.15em;

    text-transform: uppercase;

    padding-bottom: 14px;

    margin-bottom: 20px;

    border-bottom: 1px solid rgba(56,189,248,0.12);
}


/* ============================================================
   CRITIC
   ============================================================ */

.critic-card {

    margin-top: 18px;

    padding: 24px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(34,197,94,0.05),
            rgba(255,255,255,0.018)
        );

    border: 1px solid rgba(34,197,94,0.15);
}

.critic-label {

    font-family: "DM Mono", monospace;

    font-size: 10px;

    color: #4ade80;

    letter-spacing: 0.15em;

    text-transform: uppercase;

    padding-bottom: 12px;

    margin-bottom: 15px;

    border-bottom: 1px solid rgba(34,197,94,0.12);
}


/* ============================================================
   EXPANDERS
   ============================================================ */

details {

    border-radius: 13px !important;

    border: 1px solid rgba(255,255,255,0.06) !important;

    background: rgba(255,255,255,0.02) !important;

    margin-bottom: 10px !important;
}

details summary {

    font-family: "DM Mono", monospace !important;

    font-size: 10px !important;

    color: #94a3b8 !important;

    letter-spacing: 0.08em !important;
}


/* ============================================================
   DOWNLOAD
   ============================================================ */

.stDownloadButton > button {

    border-radius: 11px !important;

    background: rgba(255,255,255,0.035) !important;

    border: 1px solid rgba(255,255,255,0.09) !important;

    color: #cbd5e1 !important;

    font-size: 12px !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    text-align: center;

    margin-top: 65px;

    padding-top: 20px;

    border-top: 1px solid rgba(255,255,255,0.05);

    font-family: "DM Mono", monospace;

    font-size: 8px;

    color: #334155;

    letter-spacing: 0.12em;

    text-transform: uppercase;
}

</style>
""")


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = {}

if "running" not in st.session_state:
    st.session_state.running = False

if "done" not in st.session_state:
    st.session_state.done = False


# ============================================================
# NAVBAR
# ============================================================

st.html("""
<div class="top-nav">

    <div class="brand">
        <div class="brand-mark">◈</div>
        Researcher AI
    </div>

    <div class="nav-status">
        <span class="status-dot"></span>
        Multi-Agent System Online
    </div>

</div>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        ✦ Autonomous Research Engine
    </div>

    <h1>
        Research
        <span class="gradient">Anything.</span>
    </h1>

    <div class="hero-subtitle">
        A team of specialized AI agents searches the web,
        extracts knowledge, synthesizes findings,
        and critiques the final report.
    </div>

</div>
""")


# ============================================================
# MAIN COLUMNS
# ============================================================

col_input, col_pipeline = st.columns(
    [1.15, 0.85],
    gap="large",
)


# ============================================================
# LEFT SIDE
# ============================================================

with col_input:

    st.html("""
    <div class="research-card">

        <div class="card-label">
            Research Command
        </div>

        <div class="card-title">
            What should we investigate?
        </div>

        <div class="card-description">
            Enter any topic and let your AI research team
            find sources, extract information, write the report,
            and independently critique it.
        </div>

    </div>
    """)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Future of AI agents in software engineering",
        key="topic_input",
        label_visibility="collapsed",
    )

    run_btn = st.button(
        "⚡  Run Research Pipeline",
        use_container_width=True,
    )

    st.html("""
    <div class="example-label">
        Suggested Research
    </div>

    <span class="example-chip">
        Future of LLMs in Tech
    </span>

    <span class="example-chip">
        AI Agents in 2026
    </span>

    <span class="example-chip">
        Roadmap to AGI
    </span>

    <span class="example-chip">
        Future of Software Engineering
    </span>
    """)


# ============================================================
# RIGHT SIDE
# ============================================================

with col_pipeline:

    r = st.session_state.results

    steps = [
        ("01", "⌕", "Search Agent", "Discovers recent sources", "search"),
        ("02", "◉", "Reader Agent", "Extracts deep content", "reader"),
        ("03", "✎", "Writer", "Synthesizes the report", "writer"),
        ("04", "◌", "Critic", "Reviews the final output", "critic"),
    ]

    st.html("""
    <div class="pipeline-heading">

        <div class="pipeline-title">
            Agent Pipeline
        </div>

        <div class="pipeline-count">
            4 SPECIALISTS
        </div>

    </div>
    """)

    for index, (num, icon, name, desc, key) in enumerate(steps):

        if key in r:

            state = "done"
            status = "✓ COMPLETE"

        elif st.session_state.running:

            previous = [
                item[4]
                for item in steps[:index]
            ]

            if all(k in r for k in previous):

                state = "active"
                status = "● RUNNING"

            else:

                state = ""
                status = "WAITING"

        else:

            state = ""
            status = "WAITING"

        st.html(
            f"""
            <div class="agent-card {state}">

                <div class="agent-icon">
                    {icon}
                </div>

                <div class="agent-info">

                    <div class="agent-name">
                        {num} · {name}
                    </div>

                    <div class="agent-desc">
                        {desc}
                    </div>

                </div>

                <div class="agent-status {state}">
                    {status}
                </div>

            </div>
            """
        )

        if index < len(steps) - 1:

            st.html("""
            <div class="pipeline-connector"></div>
            """)


# ============================================================
# RUN PIPELINE
# ============================================================

if run_btn:

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

    else:

        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False

        st.rerun()


# ============================================================
# EXECUTE AGENTS
# ============================================================

if (
    st.session_state.running
    and not st.session_state.done
):

    results = {}

    topic_val = st.session_state.topic_input


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    with st.spinner(
        "🔍 Search Agent is discovering sources..."
    ):

        search_agent = build_search_agent()

        sr = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"""
Find recent, reliable and detailed information about:

{topic_val}

Focus on high-quality and relevant sources.
""",
                    )
                ]
            }
        )

        results["search"] = (
            sr["messages"][-1].content
        )

        st.session_state.results = dict(results)


    # --------------------------------------------------------
    # READER
    # --------------------------------------------------------

    with st.spinner(
        "📄 Reader Agent is extracting deeper content..."
    ):

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"""
Based on the following search results about
'{topic_val}', select the most relevant URL
and scrape it for deeper content.

Search Results:

{results['search'][:800]}
""",
                    )
                ]
            }
        )

        results["reader"] = (
            rr["messages"][-1].content
        )

        st.session_state.results = dict(results)


    # --------------------------------------------------------
    # WRITER
    # --------------------------------------------------------

    with st.spinner(
        "✍️ Writer is synthesizing the research..."
    ):

        research_combined = (
            f"SEARCH RESULTS:\n"
            f"{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n"
            f"{results['reader']}"
        )

        results["writer"] = writer_chain.invoke(
            {
                "topic": topic_val,
                "research": research_combined,
            }
        )

        st.session_state.results = dict(results)


    # --------------------------------------------------------
    # CRITIC
    # --------------------------------------------------------

    with st.spinner(
        "🧐 Critic is evaluating the report..."
    ):

        results["critic"] = critic_chain.invoke(
            {
                "report": results["writer"]
            }
        )

        st.session_state.results = dict(results)


    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# ============================================================
# RESULTS
# ============================================================

r = st.session_state.results


if r:

    st.html("""
    <div class="section-divider"></div>

    <div class="results-heading">

        <div class="results-title">
            Research Output
        </div>

        <div class="results-subtitle">
            Analysis Complete
        </div>

    </div>
    """)


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if "search" in r:

        with st.expander(
            "⌕  SEARCH AGENT · RAW OUTPUT",
            expanded=False,
        ):

            st.markdown(r["search"])


    # --------------------------------------------------------
    # READER
    # --------------------------------------------------------

    if "reader" in r:

        with st.expander(
            "◉  READER AGENT · SCRAPED CONTENT",
            expanded=False,
        ):

            st.markdown(r["reader"])


    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    if "writer" in r:

        st.html("""
        <div class="report-card">

            <div class="report-label">
                ✦ Final Research Report
            </div>

        </div>
        """)

        st.markdown(r["writer"])

        st.download_button(
            label="⬇  Download Research Report",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )


    # --------------------------------------------------------
    # CRITIC
    # --------------------------------------------------------

    if "critic" in r:

        st.html("""
        <div class="critic-card">

            <div class="critic-label">
                ◌  Critic Evaluation
            </div>

        </div>
        """)

        st.markdown(r["critic"])


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    Researcher AI · LangChain Multi-Agent Research System · Streamlit
</div>
""")