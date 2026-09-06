import streamlit as st
import time

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Lore Linter",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. THE AGED BROWN PAPER CSS
# ==========================================
st.markdown("""
<style>
    /* --- BOLD PALETTE --- */
    :root {
        --brown-beige: #D9C9A3;        /* Brownish Beige Base */
        --brown-beige-dark: #C4B18B;   /* Darker brown for panels/sidebar */
        --ink-black: #2A2A2A;          /* Typewriter Ink */
        --bold-amber: #A64B1E;         /* Amber-Red (Slightly darker) */
        --bold-amber-deep: #7A3612;    /* Darker Amber */
        --olive-green: #5C6B3C;        /* Bold Olive Green */
        --olive-deep: #3E4A28;         /* Darker Olive */
    }

    /* --- MAIN BACKGROUND (Aged Parchment) --- */
    .stApp {
        background-color: var(--brown-beige);
        /* Layered textures for aged paper: Vignette, Fiber Lines, and Grain */
        background-image: 
            radial-gradient(circle at 50% 50%, transparent 60%, rgba(90, 60, 30, 0.4) 100%),
            repeating-linear-gradient(45deg, rgba(122, 54, 18, 0.02) 0px, rgba(122, 54, 18, 0.02) 1px, transparent 1px, transparent 6px),
            repeating-linear-gradient(-45deg, rgba(62, 74, 40, 0.02) 0px, rgba(62, 74, 40, 0.02) 1px, transparent 1px, transparent 7px),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.15'/%3E%3C/svg%3E");
        color: var(--ink-black);
        font-family: 'Courier New', Courier, monospace;
    }

    /* --- TYPOGRAPHY (Typewriter Ink) --- */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Courier New', Courier, monospace;
        color: var(--ink-black);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 3px solid var(--bold-amber);
        padding-bottom: 10px;
        margin-top: 20px;
    }
    
    p, label, span, div {
        font-family: 'Courier New', Courier, monospace;
        color: var(--ink-black);
    }

    /* --- TOP NAVIGATION BAR --- */
    .nav-bar {
        background-color: var(--olive-green);
        padding: 15px;
        border-bottom: 4px solid var(--bold-amber);
        margin-bottom: 20px;
        text-align: center;
    }
    .nav-bar a {
        color: #F4ECD8; /* Light beige text on top bar */
        text-decoration: none;
        font-weight: bold;
        font-size: 1.2em;
        margin: 0 25px;
        padding: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s;
    }
    .nav-bar a:hover {
        color: var(--bold-amber);
        border-bottom: 3px solid var(--bold-amber);
    }

    /* --- SIDEBAR (Aged Brown Paper) --- */
    section[data-testid="stSidebar"] {
        background-color: var(--brown-beige-dark);
        border-right: 5px solid var(--olive-green);
        background-image: 
            radial-gradient(circle at 50% 50%, transparent 60%, rgba(90, 60, 30, 0.3) 100%),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.2'/%3E%3C/svg%3E");
    }
    
    .file-label {
        border-left: 5px solid var(--bold-amber);
        padding-left: 15px;
        margin-bottom: 10px;
        background: rgba(122, 54, 18, 0.2);
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }

    /* --- TEXT AREA (Writing Pad) --- */
    .stTextArea textarea {
        background-color: #F3E9D2; /* Lighter paper for writing */
        color: var(--ink-black);
        border: 3px solid var(--bold-amber) !important;
        border-radius: 2px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.3em;
        line-height: 1.8;
        box-shadow: inset 5px 5px 10px rgba(90, 60, 30, 0.1);
    }
    
    .stTextArea textarea:focus {
        border-color: var(--olive-green) !important;
        box-shadow: 0 0 10px rgba(92, 107, 60, 0.3);
    }

    /* --- FALLACY HIGHLIGHTS (Amber Ribbons) --- */
    .flagged-text {
        text-decoration: underline wavy var(--bold-amber) 3px;
        background-color: rgba(166, 75, 30, 0.2);
        padding: 2px 4px;
        font-weight: bold;
        cursor: pointer;
    }

    /* --- BUTTONS (Amber-Red Wax Seal) --- */
    .stButton>button {
        background-color: var(--bold-amber);
        color: #F4ECD8;
        border: 3px solid var(--bold-amber-deep);
        border-radius: 2px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.2em;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 3px 3px 0px var(--ink-black);
        transition: all 0.2s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: var(--olive-green);
        border-color: var(--olive-deep);
        box-shadow: 1px 1px 0px var(--ink-black);
        transform: translate(2px, 2px);
    }

    /* --- INSPECTOR PANELS (Olive & Amber Borders) --- */
    .editorial-note {
        background-color: rgba(243, 233, 210, 0.9);
        border-left: 6px solid var(--olive-green);
        border-bottom: 3px solid var(--bold-amber);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 3px 3px 0px rgba(90, 60, 30, 0.3);
    }
    .editorial-note strong {
        color: var(--bold-amber-deep);
        font-size: 1.2em;
    }

    /* --- ASTROLABE DIAL (Bold Olive to Amber) --- */
    .dial-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    
    .dial {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: conic-gradient(
            from 180deg,
            var(--olive-green) 0%, 
            var(--bold-amber) 100%
        );
        position: relative;
        border: 6px solid var(--ink-black);
        box-shadow: 5px 5px 0px rgba(90, 60, 30, 0.3);
    }
    
    .dial-inner {
        position: absolute;
        top: 20px; left: 20px; right: 20px; bottom: 20px;
        background-color: var(--brown-beige);
        border-radius: 50%;
        border: 3px solid var(--olive-green);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .score-text {
        font-size: 3em;
        font-family: 'Courier New', monospace;
        font-weight: 900;
        color: var(--ink-black);
        margin: 0;
    }
    
    .score-label {
        font-size: 1em;
        color: var(--bold-amber-deep);
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 2px;
    }

    /* --- SUCCESS (Olive Green) --- */
    .resolved-badge {
        color: var(--olive-deep);
        border: 3px solid var(--olive-green);
        background-color: rgba(92, 107, 60, 0.2);
        padding: 8px;
        display: inline-block;
        margin-top: 10px;
        font-weight: 900;
    }

    /* --- DIVIDERS (Amber Red) --- */
    hr {
        border: none;
        height: 3px;
        background-color: var(--bold-amber);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. EASY NAVIGATION BAR
# ==========================================
st.markdown("""
<div class="nav-bar">
    <a href="#">Home</a>
    <a href="#">Manuscript</a>
    <a href="#">Fallacy Index</a>
    <a href="#">Inspector</a>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. SIDEBAR (Easy to find)
# ==========================================
with st.sidebar:
    st.markdown("## 📖 Lore Linter")
    st.caption("Logical Fallacy Detector")
    
    st.markdown("### 📂 Manuscripts")
    st.markdown('<div class="file-label">Chapter I: The Arrival</div>', unsafe_allow_html=True)
    st.markdown('<div class="file-label">Chapter II: The Betrayal</div>', unsafe_allow_html=True)
    st.markdown('<div class="file-label">Chapter III: The Ashes</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔍 Detected Fallacies")
    st.markdown('<div class="file-label" style="border-left-color: var(--olive-green);">💡 Causal Slip</div>', unsafe_allow_html=True)
    st.markdown('<div class="file-label" style="border-left-color: var(--bold-amber);">🚩 Straw Man</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    st.text_input("API Key", type="password", placeholder="Optional...")
    st.caption("Typewriter Mode: ACTIVE")


# ==========================================
# 5. CENTRAL DRAFTING DESK
# ==========================================
col1, col2 = st.columns([2.5, 1])

with col1:
    st.markdown("## ✍️ The Drafting Desk")
    
    # The Manuscript Text (Old Paper Style)
    st.markdown("""
    <div style="background-color: #F3E9D2; border: 3px solid var(--olive-green); padding: 40px; box-shadow: inset 5px 5px 15px rgba(90, 60, 30, 0.15);">
        <p style="font-size: 1.3em; line-height: 2.2; color: var(--ink-black);">
            The knight rode into the <span class="flagged-text">city of Eldoria</span> after the war. 
            He realized his brother was the king, which meant he had <span class="flagged-text">betrayed his own family</span>. 
            However, in the previous chapter, his brother was explicitly stated to be dead.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Actual Input
    st.text_area("Draft Display", height=250, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # The Bold Button
    if st.button("🔥 Analyze Manuscript"):
        with st.spinner("Analyzing..."):
            time.sleep(1.5)
            st.markdown('<div class="resolved-badge">✓ Reconcile Complete: Logical Flow Restored</div>', unsafe_allow_html=True)

with col2:
    st.markdown("## 📝 Linter Callouts")
    
    # Editorial Notes
    st.markdown("""
    <div class="editorial-note">
        <strong>🚩 Causal Slip:</strong>
        <p>Chapter II states brother is deceased. Adjust timeline to avoid contradiction.</p>
        <p><i>"Consider a gentle revision..."</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="editorial-note" style="border-left-color: var(--olive-green);">
        <strong>✓ Tone Consistency:</strong>
        <p>Melancholic tone maintained across 3 chapters.</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 6. RIGHT INSPECTOR (Telemetry Panel)
# ==========================================
st.markdown("---")
st.markdown("## 🧭 Narrative Symmetry Astrolabe")

tele_col1, tele_col2 = st.columns([1, 2])

with tele_col1:
    st.markdown("""
    <div class="dial-container">
        <div class="dial">
            <div class="dial-inner">
                <span class="score-text">72%</span>
                <span class="score-label">Symmetric</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Bold Gradient: Olive (Sound) to Amber (Friction).")

with tele_col2:
    st.markdown("### 📊 Key Readouts")
    st.markdown("""
    <div style="font-size: 1.1em;">
        <p><strong style="color: var(--olive-deep);">Tone Consistency:</strong> <span style="color: var(--olive-deep);">✓ Stable</span></p>
        <p><strong style="color: var(--bold-amber-deep);">Premise Continuity:</strong> <span style="color: var(--bold-amber-deep);">~ 80%</span></p>
        <p><strong style="color: var(--bold-amber-deep);">Argument Flow:</strong> <span style="color: var(--bold-amber-deep);">⚠ Friction Detected</span></p>
    </div>
    """, unsafe_allow_html=True)
    
st.markdown("---")
st.caption("Lore Linter | A Bold, Old-Paper Typewriter Engine")