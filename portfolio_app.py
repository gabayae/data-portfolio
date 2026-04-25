"""Streamlit twin of index.html.

Run locally:
    streamlit run portfolio_app.py

Deploy on Streamlit Community Cloud:
    1. Push this repo to GitHub.
    2. share.streamlit.io → New app → repo: gabayae/data-portfolio,
       branch: main, file: portfolio_app.py.
"""

from __future__ import annotations
import streamlit as st

import portfolio_config as cfg

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{cfg.NAME} — Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": f"{cfg.NAME} — Data Science Portfolio. {cfg.SITE}"},
)

# ── Custom CSS (PasserellAI editorial palette) ────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {{
        background: {cfg.COLOR_BG};
        color: {cfg.COLOR_INK};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    h1, h2, h3, h4 {{
        font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif !important;
        color: {cfg.COLOR_PRIMARY} !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }}
    .eyebrow {{
        font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em;
        color: {cfg.COLOR_ACCENT}; font-weight: 600; margin-bottom: 0.5rem;
        display: block;
    }}

    .hero {{
        background: linear-gradient(135deg, #0f2a4a 0%, #1a3d66 100%);
        color: #fafaf7; padding: 3rem 2rem; border-radius: 16px;
        margin-bottom: 2rem; text-align: center;
    }}
    .hero h1 {{ color: #fafaf7 !important; font-size: 2.6rem !important; margin: 0.6rem 0 !important; }}
    .hero .badge {{
        display: inline-block; padding: 0.4rem 1.2rem;
        background: rgba(200, 92, 60, 0.12); border: 1px solid rgba(200, 92, 60, 0.4);
        border-radius: 50px; color: {cfg.COLOR_ACCENT};
        font-size: 0.78rem; font-weight: 600; letter-spacing: 0.06em;
        text-transform: uppercase; margin-bottom: 0.8rem;
    }}
    .hero .tagline {{ font-size: 1.05rem; color: #dfe6ef; max-width: 50rem; margin: 0.8rem auto 0; }}
    .hero .avatar {{
        width: 110px; height: 110px; border-radius: 50%;
        border: 3px solid {cfg.COLOR_ACCENT};
        background: linear-gradient(135deg, #1a3d66, #0f2a4a);
        display: inline-flex; align-items: center; justify-content: center;
        font-family: "Iowan Old Style", Georgia, serif;
        font-size: 2.4rem; font-weight: 700; color: {cfg.COLOR_ACCENT};
        margin-bottom: 0.6rem;
    }}

    .stat-card {{
        background: {cfg.COLOR_SURFACE}; border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 16px; padding: 1.4rem;
        box-shadow: 0 1px 3px rgba(15,42,74,0.06);
        height: 100%;
    }}
    .stat-card .value {{
        font-family: "Iowan Old Style", Georgia, serif; font-size: 2.2rem; font-weight: 600;
        color: {cfg.COLOR_ACCENT}; line-height: 1; margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }}
    .stat-card .label {{ font-size: 0.92rem; color: {cfg.COLOR_MUTED}; }}

    .pcard {{
        background: {cfg.COLOR_SURFACE}; border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 16px; padding: 1.4rem; height: 100%;
        box-shadow: 0 1px 3px rgba(15,42,74,0.06);
        position: relative; overflow: hidden;
    }}
    .pcard::before {{
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: {cfg.COLOR_ACCENT};
    }}
    .pcard .num {{
        display: inline-flex; align-items: center; justify-content: center;
        width: 34px; height: 34px;
        background: #e3e8ef; color: {cfg.COLOR_PRIMARY};
        border-radius: 8px; font-family: "JetBrains Mono", monospace;
        font-weight: 700; font-size: 0.82rem; margin-bottom: 0.7rem;
    }}
    .pcard .metric {{
        font-family: "Iowan Old Style", Georgia, serif; font-size: 1.2rem; font-weight: 600;
        color: {cfg.COLOR_ACCENT}; margin: 0 0 0.4rem; letter-spacing: -0.005em;
    }}
    .pcard h4 {{
        font-family: "Iowan Old Style", Georgia, serif !important;
        color: {cfg.COLOR_PRIMARY} !important; font-size: 1.1rem !important;
        margin: 0 0 0.4rem !important; font-weight: 600 !important;
    }}
    .pcard .tagline {{ font-size: 0.9rem; color: {cfg.COLOR_MUTED}; margin-bottom: 0.7rem; }}
    .pcard .pills {{ margin-bottom: 0.7rem; }}
    .pcard .pill {{
        display: inline-block; padding: 0.18rem 0.6rem; border-radius: 8px;
        font-size: 0.72rem; font-weight: 600; margin-right: 0.3rem; margin-bottom: 0.3rem;
    }}
    .pcard .tech {{ margin-bottom: 0.7rem; }}
    .pcard .tech .pill {{
        background: #f2efe8; color: {cfg.COLOR_MUTED}; border: 1px solid {cfg.COLOR_BORDER};
        font-weight: 500; font-size: 0.7rem;
    }}
    .pcard .dataset {{ font-size: 0.8rem; color: {cfg.COLOR_MUTED}; margin-bottom: 0.8rem; }}
    .pcard .links a {{
        font-size: 0.85rem; margin-right: 0.8rem; color: {cfg.COLOR_PRIMARY};
        text-decoration: underline; text-underline-offset: 3px;
    }}
    .pcard .links a.primary {{
        background: {cfg.COLOR_ACCENT}; color: #fff !important;
        padding: 0.35rem 0.8rem; border-radius: 8px;
        text-decoration: none; font-weight: 500;
    }}

    .skill-card {{
        background: {cfg.COLOR_SURFACE}; border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 16px; padding: 1.4rem; height: 100%;
        box-shadow: 0 1px 3px rgba(15,42,74,0.06);
    }}
    .skill-card h4 {{
        font-family: "Iowan Old Style", Georgia, serif !important;
        color: {cfg.COLOR_PRIMARY} !important; font-size: 1.05rem !important;
        margin: 0 0 0.8rem !important;
    }}
    .skill-row {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.45rem 0; border-bottom: 1px solid {cfg.COLOR_BORDER};
        font-size: 0.92rem;
    }}
    .skill-row:last-child {{ border-bottom: none; }}
    .skill-row .refs span {{
        display: inline-flex; align-items: center; justify-content: center;
        min-width: 26px; height: 22px; padding: 0 0.3rem;
        background: {cfg.COLOR_ACCENT_SOFT}; color: #b04b2e;
        border-radius: 4px; font-family: monospace;
        font-size: 0.7rem; font-weight: 600; margin-left: 0.25rem;
    }}

    .tool-pill {{
        display: inline-block; padding: 0.25rem 0.7rem; background: #f2efe8;
        border: 1px solid {cfg.COLOR_BORDER}; border-radius: 6px;
        font-size: 0.82rem; color: {cfg.COLOR_INK}; margin: 0 0.3rem 0.4rem 0;
    }}

    .process-step {{
        display: inline-block; background: {cfg.COLOR_SURFACE};
        border: 1px solid {cfg.COLOR_BORDER}; border-radius: 8px;
        padding: 0.6rem 1rem; font-size: 0.92rem; font-weight: 500;
        color: {cfg.COLOR_PRIMARY}; margin: 0.2rem;
    }}
    .process-arrow {{ color: {cfg.COLOR_ACCENT}; font-size: 1.2rem; margin: 0 0.2rem; }}

    /* hide Streamlit chrome */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    [data-testid="stHeader"] {{ background: transparent; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="hero">
      <div class="avatar">YG</div>
      <div class="badge">Real African + Global Open Data</div>
      <h1>13 projects. Real data. Real models.</h1>
      <p class="tagline">{cfg.TAGLINE}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown('<span class="eyebrow">At a glance</span>', unsafe_allow_html=True)
st.markdown("## Headline numbers from the portfolio")
cols = st.columns(len(cfg.STATS))
for col, (val, lbl) in zip(cols, cfg.STATS):
    col.markdown(f'<div class="stat-card"><div class="value">{val}</div><div class="label">{lbl}</div></div>', unsafe_allow_html=True)

st.write("")

# ── Projects ──────────────────────────────────────────────────────────────────
st.markdown('<br><span class="eyebrow">Thirteen projects</span>', unsafe_allow_html=True)
st.markdown("## Projects")

filter_options = list(cfg.CATEGORY_LABELS.values())
filter_keys = list(cfg.CATEGORY_LABELS.keys())
filter_label = st.radio(
    "Filter projects:",
    filter_options,
    horizontal=True,
    label_visibility="collapsed",
)
selected_key = filter_keys[filter_options.index(filter_label)]

filtered = [p for p in cfg.PROJECTS if selected_key == "all" or selected_key in p.categories]


def project_card(p: cfg.Project) -> str:
    cat_html = "".join(
        f'<span class="pill" style="background:{cfg.CATEGORY_COLORS[c][0]}; color:{cfg.CATEGORY_COLORS[c][1]};">'
        f'{cfg.CATEGORY_LABELS.get(c, c).split(" / ")[0]}</span>'
        for c in p.categories
    )
    tech_html = "".join(f'<span class="pill">{t}</span>' for t in p.tech)
    base = cfg.STATIC_BASE
    primary_link = (
        f'<a class="primary" href="{base}{p.case_study}" target="_blank">Case study →</a>'
        if p.case_study
        else f'<a class="primary" href="{base}{p.folder}/" target="_blank">Project →</a>'
    )
    return f"""
    <div class="pcard">
        <div class="num">{p.number:02d}</div>
        <div class="metric">{p.metric}</div>
        <h4>{p.title}</h4>
        <div class="tagline">{p.tagline}</div>
        <div class="pills">{cat_html}</div>
        <div class="tech pills">{tech_html}</div>
        <div class="dataset">📊 {p.dataset}</div>
        <div class="links">
            {primary_link}
            <a href="{base}{p.folder}/notebook.ipynb" target="_blank">Notebook</a>
        </div>
    </div>
    """


# 3-col responsive grid
ROW = 3
for i in range(0, len(filtered), ROW):
    row = filtered[i : i + ROW]
    cols = st.columns(len(row))
    for col, p in zip(cols, row):
        col.markdown(project_card(p), unsafe_allow_html=True)

if not filtered:
    st.info("No projects match this filter yet.")

# ── Process ───────────────────────────────────────────────────────────────────
st.write("")
st.markdown('<br><span class="eyebrow">Same shape, every time</span>', unsafe_allow_html=True)
st.markdown("## Process")
flow = ' <span class="process-arrow">→</span> '.join(
    f'<span class="process-step">{s}</span>' for s in cfg.PROCESS_STEPS
)
st.markdown(f'<div style="text-align:center;">{flow}</div>', unsafe_allow_html=True)

# ── Capabilities ──────────────────────────────────────────────────────────────
st.write("")
st.markdown('<br><span class="eyebrow">What this portfolio demonstrates</span>', unsafe_allow_html=True)
st.markdown("## Capabilities")

st.markdown("### Techniques")
groups = list(cfg.TECHNIQUES.items())
for i in range(0, len(groups), 2):
    row = groups[i : i + 2]
    cols = st.columns(2)
    for col, (group_name, items) in zip(cols, row):
        rows_html = "".join(
            f'<div class="skill-row"><span>{name}</span>'
            f'<span class="refs">{"".join(f"<span>{n:02d}</span>" for n in refs)}</span></div>'
            for name, refs in items
        )
        col.markdown(
            f'<div class="skill-card"><h4>{group_name}</h4>{rows_html}</div>',
            unsafe_allow_html=True,
        )

st.markdown("### Tools")
cols = st.columns(len(cfg.TOOLS))
for col, (group, pills) in zip(cols, cfg.TOOLS.items()):
    pills_html = "".join(f'<span class="tool-pill">{t}</span>' for t in pills)
    col.markdown(
        f'<div class="skill-card"><h4>{group}</h4>{pills_html}</div>',
        unsafe_allow_html=True,
    )

# ── Background ────────────────────────────────────────────────────────────────
st.write("")
st.markdown('<br><span class="eyebrow">Who</span>', unsafe_allow_html=True)
st.markdown("## Background")
st.markdown(
    f"PhD in Mathematics (Topology) from the University of Cape Town. Career split between "
    f"rigorous applied mathematics and hands-on data science, with 10+ years across healthcare, "
    f"finance, energy, insurance, retail, and government environments. Co-author of "
    f"[The Shape of Data]({cfg.BOOK}) (No Starch Press, 2024) — a graduate-level textbook on "
    f"geometry-based machine learning. h-index 12 across 18+ peer-reviewed papers. Bilingual EN/FR."
)

# ── Contact ───────────────────────────────────────────────────────────────────
st.write("")
st.markdown('<br><span class="eyebrow">Get in touch</span>', unsafe_allow_html=True)
st.markdown("## Contact")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"📧 **Email** \n[{cfg.EMAIL}](mailto:{cfg.EMAIL})")
c2.markdown(f"💼 **LinkedIn** \n[linkedin.com/in/gabayae]({cfg.LINKEDIN})")
c3.markdown(f"🐙 **GitHub** \n[github.com/gabayae]({cfg.GITHUB})")
c4.markdown(f"🌐 **Site** \n[gabayae.github.io]({cfg.SITE})")

st.write("")
st.markdown(
    f'<hr style="border:0;border-top:1px solid {cfg.COLOR_BORDER};margin:2rem 0 1rem;">'
    f'<div style="text-align:center; color:{cfg.COLOR_MUTED}; font-size:0.85rem;">'
    f"© 2026 {cfg.NAME} · Built end-to-end on real public data · MIT licensed · {cfg.LOCATION}"
    f"</div>",
    unsafe_allow_html=True,
)
