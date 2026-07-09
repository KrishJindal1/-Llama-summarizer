"""Document Intelligence — local LLM summarization & rewriting studio."""

import html

import streamlit as st

from core.analyzer import generate_summary, rewrite_content, summary_config
from core.extractor import extract_text
from core.ollama_client import get_models

st.set_page_config(
    page_title="Document Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Design tokens: navy/cobalt enterprise palette, Space Grotesk for headings,
# Inter for UI text, IBM Plex Mono for data (stats, labels, config pills).
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root{
  --ink:#12203b;
  --canvas:#eef1f6;
  --surface:#ffffff;
  --accent:#3454d1;
  --accent-soft:#e8edfc;
  --line:#e2e6ee;
  --muted:#667085;
  --text:#101828;
  --radius:12px;
  --shadow-sm:0 1px 2px rgba(16,24,40,.06);
  --shadow-md:0 8px 24px rgba(16,24,40,.10);
}

html, body, .stApp, .stMarkdown, .stTextArea textarea, .stSelectbox, .stButton button{
  font-family:'Inter',-apple-system,'Segoe UI',sans-serif;
}

.stApp{ background:var(--canvas); color:var(--text); }

@media (prefers-reduced-motion: reduce){
  *{ animation:none !important; transition:none !important; }
}

/* Header */
.app-header{ padding:1.6rem 0 1.1rem 0; animation:fadeIn .5s ease-out; }
.app-eyebrow{
  font-family:'IBM Plex Mono',monospace; font-size:.72rem; font-weight:500;
  letter-spacing:.14em; text-transform:uppercase; color:var(--accent); margin-bottom:.35rem;
}
.app-title{
  font-family:'Space Grotesk',sans-serif; font-size:2.1rem; font-weight:700;
  color:var(--ink); letter-spacing:-.01em; line-height:1.1;
}
.app-subtitle{ font-size:.95rem; color:var(--muted); margin-top:.4rem; max-width:640px; }
.pill-row{
  display:flex; flex-wrap:wrap; gap:.5rem; margin-top:1.1rem;
  padding-top:1.1rem; border-top:1px solid var(--line);
}
.pill{
  font-family:'IBM Plex Mono',monospace; font-size:.75rem; background:var(--accent-soft);
  color:var(--accent); padding:.28rem .65rem; border-radius:999px;
  border:1px solid rgba(52,84,209,.15);
}

/* Sidebar */
[data-testid="stSidebar"]{ background:var(--ink); }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] small{ color:#c3cee3 !important; }
[data-testid="stSidebar"] hr{ border-color:rgba(255,255,255,.08); }
.sidebar-brand{ font-family:'Space Grotesk',sans-serif; font-size:1.15rem; font-weight:700; color:#fff; }
.sidebar-tagline{
  font-family:'IBM Plex Mono',monospace; font-size:.7rem; letter-spacing:.08em;
  text-transform:uppercase; color:#7f93c2; margin-top:.1rem;
}
.sidebar-section{
  font-family:'IBM Plex Mono',monospace; font-size:.68rem; font-weight:500;
  letter-spacing:.1em; text-transform:uppercase; color:#7f93c2; margin:.3rem 0;
}

/* Buttons */
.stButton>button{
  border-radius:8px; font-weight:600; padding:.5rem 1.3rem; border:1px solid var(--line);
  transition:transform .15s ease, box-shadow .15s ease;
}
.stButton>button:hover{ transform:translateY(-1px); box-shadow:var(--shadow-md); }
.stButton>button:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }
.stButton>button[kind="primary"]{ background:var(--accent); border-color:var(--accent); }

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
    gap:1.4rem;
    border-bottom:1px solid var(--line);
}

.stTabs [data-baseweb="tab"]{
    color:#475467 !important;
    font-weight:600;
    opacity:1 !important;
}

.stTabs [aria-selected="true"]{
    color:var(--accent) !important;
    border-bottom:2px solid var(--accent);
}

/* Cards (bordered containers) — force readable text regardless of theme */
[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius:var(--radius) !important; border-color:var(--line) !important;
  box-shadow:var(--shadow-sm); background:var(--surface) !important; animation:fadeIn .4s ease-out;
}
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] span,
[data-testid="stVerticalBlockBorderWrapper"] li,
[data-testid="stVerticalBlockBorderWrapper"] label,
[data-testid="stVerticalBlockBorderWrapper"] div{ color:var(--text) !important; }
[data-testid="stVerticalBlockBorderWrapper"] .pill{ color:var(--accent) !important; }
[data-testid="stVerticalBlockBorderWrapper"] .result-label{ color:var(--muted) !important; }

/* Text areas (paste box, preview box) */
.stTextArea textarea{
  background:var(--surface) !important; color:var(--text) !important; border-color:var(--line) !important;
  -webkit-text-fill-color:var(--text) !important;
}

/* Metrics */
[data-testid="stMetric"]{ background:var(--accent-soft); border-radius:8px; padding:.6rem .9rem; }
[data-testid="stMetricLabel"]{
  font-family:'IBM Plex Mono',monospace; font-size:.68rem; letter-spacing:.06em;
  text-transform:uppercase; color:var(--muted) !important;
}
[data-testid="stMetricValue"]{ font-family:'IBM Plex Mono',monospace; color:var(--ink) !important; }

/* Alerts (st.success / st.warning / st.error) */
[data-testid="stAlert"]{
  border-radius:8px; background:var(--accent-soft) !important; border:1px solid var(--line) !important;
}
[data-testid="stAlert"] p, [data-testid="stAlert"] span, [data-testid="stAlert"] div{
  color:var(--ink) !important;
}

/* Upload dropzone */
[data-testid="stFileUploaderDropzone"]{
  border-radius:var(--radius); border:1.5px dashed var(--line);
  background:var(--surface) !important; transition:border-color .15s ease;
}
[data-testid="stFileUploaderDropzone"]:hover{ border-color:var(--accent); }
[data-testid="stFileUploaderDropzone"] *{ color:var(--text) !important; }

/* st.status widget (Processing document / Generating summary...) */
[data-testid="stStatusWidget"]{
  border-radius:var(--radius); border-color:var(--line); background:var(--surface) !important;
}
[data-testid="stStatusWidget"] p, [data-testid="stStatusWidget"] span, [data-testid="stStatusWidget"] div{
  color:var(--text) !important;
}

.result-label{
  font-family:'IBM Plex Mono',monospace; font-size:.7rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted); margin-bottom:.3rem;
}
.footnote{ font-size:.78rem; color:var(--muted); margin-top:2rem; }

@keyframes fadeIn{ from{ opacity:0; transform:translateY(6px); } to{ opacity:1; transform:translateY(0); } }
</style>
"""


def inject_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header(selected_model: str, temperature: float, tone: str, rewrite_target: str, word_count: int) -> None:
    """Page title plus a live strip showing the active configuration."""
    pills = "".join(
        f'<span class="pill">{html.escape(str(value))}</span>'
        for value in (selected_model, f"temp {temperature:.2f}", tone, rewrite_target, f"{word_count:,} words")
    )
    st.markdown(
        f"""
        <div class="app-header">
            <div class="app-eyebrow">Document Intelligence</div>
            <div class="app-title">Summarize &amp; Rewrite</div>
            <div class="app-subtitle">Turn a long document into a clear summary and a
            rewritten version in the tone you need, running entirely on your local model.</div>
            <div class="pill-row">{pills}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats(text: str) -> None:
    words = len(text.split())
    minutes = max(1, round(words / 200))
    col1, col2, col3 = st.columns(3)
    col1.metric("Words", f"{words:,}")
    col2.metric("Characters", f"{len(text):,}")
    col3.metric("Reading time", f"{minutes} min")


def show_preview(document_text: str) -> None:
    words = len(document_text.split())
    with st.container(border=True):
        st.markdown(
            f'<div class="result-label">Preview &middot; {words:,} words</div>',
            unsafe_allow_html=True,
        )
        st.text_area("Preview", document_text[:2000], height=200, label_visibility="collapsed")


def analyze_document(document_text, selected_model, temperature, tone, rewrite_target, target_length):
    with st.status("Processing document", expanded=True) as status:
        st.write("Generating summary...")
        try:
            summary = generate_summary(document_text, target_length, selected_model)
        except Exception as e:
            status.update(label="Summary generation failed", state="error")
            st.error(f"Summary generation failed: {e}")
            return
        st.write("Summary generated.")

        st.write("Rewriting content...")
        try:
            rewritten_text = rewrite_content(document_text, summary, tone, temperature, rewrite_target, selected_model)
        except Exception as e:
            status.update(label="Rewrite failed", state="error")
            st.error(f"Rewriting failed: {e}")
            return
        st.write("Rewritten content generated.")

        status.update(label="Analysis complete", state="complete")

    tab_summary, tab_rewrite = st.tabs(["Summary", "Rewritten"])
    with tab_summary:
        with st.container(border=True):
            st.markdown('<div class="result-label">Summary</div>', unsafe_allow_html=True)
            st.write(summary)
    with tab_rewrite:
        with st.container(border=True):
            st.markdown(
                f'<div class="result-label">Rewritten &middot; {html.escape(tone)}</div>',
                unsafe_allow_html=True,
            )
            st.write(rewritten_text)


def process_extracted_text(document_text, file_type, selected_model, temperature, tone, rewrite_target, target_length):
    if not document_text.strip():
        st.error(f"No text could be extracted from {file_type}.")
        return
    st.success(f"{file_type} processed successfully.")
    render_stats(document_text)
    show_preview(document_text)
    analyze_document(document_text, selected_model, temperature, tone, rewrite_target, target_length)


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">Document Intelligence</div>'
            '<div class="sidebar-tagline">Local LLM Studio</div>',
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown('<div class="sidebar-section">Model</div>', unsafe_allow_html=True)
        model_names = get_models()
        selected_model = st.selectbox("Model", model_names, label_visibility="collapsed")
        temperature = st.slider(
            "Temperature", 0.0, 1.0, 0.7,
            help="Higher values produce more varied, less predictable output.",
        )

        st.divider()
        st.markdown('<div class="sidebar-section">Summary length</div>', unsafe_allow_html=True)
        summary_size = st.selectbox("Summary length", ["Short", "Medium", "Long"], label_visibility="collapsed")
        target_length = summary_config[summary_size]

        st.divider()
        st.markdown('<div class="sidebar-section">Rewrite</div>', unsafe_allow_html=True)
        tone = st.selectbox(
            "Tone",
            ["Professional", "Formal", "Casual", "Executive", "Technical", "Academic", "Marketing", "Simple English"],
        )
        rewrite_target = st.selectbox("Apply to", ["Summary", "Full Document"])

    return selected_model, temperature, target_length, tone, rewrite_target


def app():
    inject_css()
    selected_model, temperature, target_length, tone, rewrite_target = render_sidebar()

    # Read whatever is currently in the paste box (via its widget key) so the
    # header's "words" pill reflects live content instead of a hardcoded 0.
    live_text = st.session_state.get("document_text", "")
    live_word_count = len(live_text.split())

    render_header(selected_model, temperature, tone, rewrite_target, word_count=live_word_count)

    tab_paste, tab_upload = st.tabs(["Paste text", "Upload document"])

    with tab_paste:
        document_text = st.text_area(
            "Paste your text",
            height=280,
            placeholder="Paste the text you want to summarize or rewrite.",
            label_visibility="collapsed",
            key="document_text",
        )
        st.caption(f"{live_word_count:,} words")
        if st.button("Analyze document", type="primary"):
            if not document_text.strip():
                st.warning("Enter some text before analyzing.")
            else:
                analyze_document(document_text, selected_model, temperature, tone, rewrite_target, target_length)

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload a document", type=["pdf", "docx", "pptx", "txt"], label_visibility="collapsed",
        )
        if st.button("Analyze uploaded document", type="primary"):
            if not uploaded_file:
                st.warning("Upload a document before analyzing.")
            else:
                try:
                    with st.container(border=True):
                        st.markdown('<div class="result-label">File details</div>', unsafe_allow_html=True)
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.caption("Name")
                            st.write(uploaded_file.name)
                        with c2:
                            st.caption("Type")
                            st.write(uploaded_file.type)
                        with c3:
                            st.caption("Size")
                            st.write(f"{uploaded_file.size / 1024:.1f} KB")

                    document_text = extract_text(uploaded_file, uploaded_file.name)
                    process_extracted_text(
                        document_text, uploaded_file.name, selected_model,
                        temperature, tone, rewrite_target, target_length,
                    )
                except Exception as e:
                    st.error(f"Error reading file: {e}")

    st.markdown(
        '<div class="footnote">Processing runs on your local Ollama instance '
        '&mdash; documents never leave this machine.</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    app()