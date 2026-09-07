import streamlit as st
import requests
import html
import time

# -----------------------------------------------------------------------------
# 1. PAGE SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Lore Linter — The Empathetic Logic Engine",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE
# -----------------------------------------------------------------------------
if "analysis_data" not in st.session_state:
    st.session_state["analysis_data"] = None
if "job_id" not in st.session_state:
    st.session_state["job_id"] = None
if "api_error" not in st.session_state:
    st.session_state["api_error"] = None

# -----------------------------------------------------------------------------
# 3. LITERARY LOGIC CSS (Keep your beautiful design)
# -----------------------------------------------------------------------------
DARK_ACADEMIA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap');
:root {
    --paper-bg: #D9C9A3; --paper-dark: #C7B589; --charcoal: #2A2A2A;
    --amber-red: #A64B1E; --olive-green: #5C6B3C; --sage-green: #6A7E54;
    --wax-gold: #C29B38;
}
html, body, [class*="css"], .stApp {
    font-family: 'Courier Prime', 'Courier New', monospace !important;
    background-color: var(--paper-bg) !important; color: var(--charcoal) !important;
}
.stApp::before {
    content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 1;
}
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }
.header-banner {
    border-bottom: 2px solid var(--amber-red); padding: 6px 0 16px 0; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: baseline;
}
.header-title {
    font-size: 1.85rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--amber-red); margin: 0;
}
.header-subtitle { font-size: 0.85rem; color: var(--olive-green); font-style: italic; letter-spacing: 0.05em; }
.nav-card {
    background-color: rgba(199, 181, 137, 0.45); border: 1px solid var(--olive-green); border-radius: 2px;
    padding: 16px; margin-bottom: 16px; box-shadow: 2px 3px 6px rgba(42, 42, 42, 0.08);
}
.nav-heading {
    font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em;
    color: var(--olive-green); border-bottom: 1px dashed var(--olive-green); padding-bottom: 6px; margin-bottom: 12px;
}
div[data-baseweb="textarea"] {
    background-color: #E2D5B5 !important; border: 2px solid var(--olive-green) !important;
    border-radius: 2px !important; box-shadow: inset 2px 2px 8px rgba(42, 42, 42, 0.15) !important;
}
div[data-baseweb="textarea"] textarea {
    font-family: 'Courier Prime', 'Courier New', monospace !important; font-size: 1.02rem !important;
    line-height: 1.8 !important; color: var(--charcoal) !important; background-color: transparent !important;
}
div.stButton > button {
    font-family: 'Courier Prime', monospace !important; font-weight: 700 !important; font-size: 0.95rem !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important; color: #FDFBF7 !important;
    background: linear-gradient(135deg, #943A14 0%, #A64B1E 60%, #C86A32 100%) !important;
    border: 2px solid var(--wax-gold) !important; border-radius: 3px !important; padding: 12px 24px !important;
    box-shadow: 3px 4px 0px var(--charcoal), 0 5px 12px rgba(166, 75, 30, 0.35) !important;
}
div.stButton > button:hover { transform: translate(-1px, -1px) !important; }
.editorial-card {
    background-color: #E2D5B5; border-radius: 2px; padding: 14px 16px; margin-bottom: 14px;
    box-shadow: 2px 3px 8px rgba(42, 42, 42, 0.08); border-left: 5px solid var(--amber-red);
}
.editorial-card.low-severity { border-left: 5px solid var(--olive-green); }
.card-header { display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.card-type { color: var(--amber-red); }
.card-location { color: var(--olive-green); }
.card-quote { font-style: italic; font-size: 0.88rem; background: rgba(199, 181, 137, 0.5); padding: 6px 10px; border-left: 2px solid var(--charcoal); margin: 8px 0; }
.card-explanation { font-size: 0.85rem; line-height: 1.5; margin-bottom: 8px; }
.card-suggestion { font-size: 0.82rem; color: var(--olive-green); border-top: 1px dashed var(--olive-green); padding-top: 6px; }
.astrolabe-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 18px 0; }
.astrolabe-outer-ring { width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(42, 42, 42, 0.15); border: 2px solid var(--wax-gold); }
.astrolabe-inner-core { width: 110px; height: 110px; background-color: var(--paper-bg); border-radius: 50%; border: 1px dashed var(--olive-green); display: flex; flex-direction: column; align-items: center; justify-content: center; }
.astrolabe-score { font-size: 1.8rem; font-weight: 700; color: var(--charcoal); line-height: 1; }
.astrolabe-subtext { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--olive-green); margin-top: 4px; }
</style>
"""
st.markdown(DARK_ACADEMIA_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="header-banner">
    <div>
        <div class="header-title">Lore Linter</div>
        <div class="header-subtitle">Chronicle Validation & Argument Symmetry Desk</div>
    </div>
    <div style="font-size: 0.8rem; color: var(--charcoal); letter-spacing: 0.08em;">STUDIO EDITION • 02:00 AM MODE</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. LAYOUT
# -----------------------------------------------------------------------------
col_nav, col_editor, col_inspector = st.columns([1.1, 2.5, 1.4], gap="medium")

# Left Panel
with col_nav:
    st.markdown('<div class="nav-card"><div class="nav-heading">Manuscript Index</div><div class="nav-item">📜 Act I: The Salt Flats</div><div class="nav-item" style="font-weight: bold; color: #A64B1E;">🖋 Act II: The Sovereign</div><div class="nav-item">📜 Act III: The Broken Covenant</div></div>', unsafe_allow_html=True)
    st.checkbox("Chapter 1", value=True)
    st.checkbox("Chapter 2", value=True)
    st.checkbox("Chapter 3", value=False)

# Center Workspace
with col_editor:
    st.markdown('<div class="nav-heading">Folio Drafting Canvas</div>', unsafe_allow_html=True)
    
    # Get user text
    manuscript_text = st.text_area("Manuscript", height=260, label_visibility="collapsed")
    
    # Button
    if st.button("⚖️ Analyze Manuscript"):
        st.session_state["api_error"] = None
        try:
            # Step 1: Upload to her API
            files = {"file": ("manuscript.txt", manuscript_text.encode("utf-8"), "text/plain")}
            data = {"title": "My Novel", "author": "User"}
            upload_resp = requests.post("http://127.0.0.1:8000/api/v1/analyze", files=files, data=data, timeout=10)
            
            if upload_resp.status_code == 200:
                st.session_state["job_id"] = upload_resp.json().get("job_id")
                
                # Step 2: Poll the status
                with st.spinner("Consulting the Astrolabe..."):
                    time.sleep(2)  # Initial wait
                    while True:
                        status_resp = requests.get(f"http://127.0.0.1:8000/api/v1/analyze/{st.session_state['job_id']}/status")
                        if status_resp.status_code == 200:
                            status = status_resp.json().get("status")
                            if status == "completed":
                                break
                            elif status == "failed":
                                st.session_state["api_error"] = "Analysis failed. Check backend."
                                break
                            else:
                                time.sleep(2)  # Wait more
                
                # Step 3: Get the results
                if status == "completed":
                    results_resp = requests.get(f"http://127.0.0.1:8000/api/v1/analyze/{st.session_state['job_id']}/results")
                    if results_resp.status_code == 200:
                        backend_data = results_resp.json()
                        
                        # Convert her backend data to fit our UI
                        violations = backend_data.get("violations", [])
                        score = max(0, 100 - (len(violations) * 15))
                        
                        formatted_fallacies = []
                        for v in violations:
                            formatted_fallacies.append({
                                "type": v.get("type", "Violation").replace("_", " ").title(),
                                "severity": "high" if v.get("severity") == "ERROR" else "low",
                                "location": f"Chapter {v.get('conflicting_facts', [{}])[0].get('chapter', '?')}",
                                "quote": v.get("conflicting_facts", [{}])[0].get("text", ""),
                                "explanation": v.get("description", ""),
                                "suggestion": v.get("suggested_fix", "")
                            })
                        
                        st.session_state["analysis_data"] = {
                            "overall_score": score,
                            "fallacies": formatted_fallacies
                        }
            else:
                st.session_state["api_error"] = f"Upload failed: {upload_resp.status_code}"
        except Exception as e:
            st.session_state["api_error"] = f"Cannot connect to backend: {e}"

    if st.session_state["api_error"]:
        st.error(st.session_state["api_error"])
    
    if st.session_state["analysis_data"]:
        raw_text = manuscript_text
        annotated_text = html.escape(raw_text)
        for item in st.session_state["analysis_data"]["fallacies"]:
            quote = item.get("quote", "").strip()
            if quote and quote in raw_text:
                annotated_text = annotated_text.replace(html.escape(quote), f'<span style="text-decoration: underline wavy var(--amber-red); background: rgba(166, 75, 30, 0.15); padding: 2px 4px;">{html.escape(quote)}</span>')
        st.markdown(f'<div style="margin-top: 20px; padding: 15px; border: 1px dashed var(--amber-red); background: #EDE2C8;">{annotated_text}</div>', unsafe_allow_html=True)

# Right Inspector
with col_inspector:
    st.markdown('<div class="nav-heading">Narrative Symmetry</div>', unsafe_allow_html=True)
    current_score = st.session_state["analysis_data"]["overall_score"] if st.session_state["analysis_data"] else 100
    gauge_deg = (current_score / 100.0) * 360
    st.markdown(f'<div class="astrolabe-wrapper"><div class="astrolabe-outer-ring" style="background: conic-gradient(var(--olive-green) 0deg {gauge_deg}deg, rgba(166, 75, 30, 0.2) {gauge_deg}deg 360deg);"><div class="astrolabe-inner-core"><div class="astrolabe-score">{current_score}%</div><div class="astrolabe-subtext">Symmetry</div></div></div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="nav-heading" style="margin-top: 8px;">Editorial Marginalia</div>', unsafe_allow_html=True)
    if st.session_state["analysis_data"]:
        for item in st.session_state["analysis_data"]["fallacies"]:
            sev_class = "high-severity" if item.get("severity") == "high" else "low-severity"
            st.markdown(f'<div class="editorial-card {sev_class}"><div class="card-header"><span class="card-type">{html.escape(item.get("type", "Violation"))}</span><span class="card-location">{html.escape(item.get("location", ""))}</span></div><div class="card-quote">"{html.escape(item.get("quote", ""))}"</div><div class="card-explanation">{html.escape(item.get("explanation", ""))}</div><div class="card-suggestion"><strong>Proposal:</strong> {html.escape(item.get("suggestion", ""))}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size: 0.82rem; color: var(--olive-green); font-style: italic; padding: 8px 0;">Press Analyze Manuscript to awaken the linter.</div>', unsafe_allow_html=True)