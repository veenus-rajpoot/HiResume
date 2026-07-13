"""
Design direction: an editor's drafting desk, not a generic SaaS dashboard.

Palette:
  --ink       #1B2A4A   deep navy ink — headings, primary text
  --paper     #FAF8F2   warm paper white — page background
  --paper-2   #F1ECE0   slightly deeper paper — card backgrounds
  --accent    #B8722E   sealing-wax amber — CTAs, section rules, the signature meter
  --accent-2  #4E7A63   ledger green — "covered requirement" state
  --muted     #7A7266   faded pencil — secondary text
  --line      #DCD4C2   hairline rule color

Type:
  Display: 'Source Serif 4' (falls back to Georgia) — resume-like, editorial
  Body/UI: 'Inter' — clean, legible at small sizes
  Data/ATS: 'IBM Plex Mono' — the "typewriter" register for scores & keywords

Signature element: the "Match Meter" — a horizontal ruler/gauge (like a
typesetter's pica ruler) that fills with amber ink up to the ATS score,
with tick marks every 10%. It reframes "ATS score" as something drafted
by hand rather than a generic circular progress ring.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --ink: #1B2A4A;
    --paper: #FAF8F2;
    --paper-2: #F1ECE0;
    --accent: #B8722E;
    --accent-2: #4E7A63;
    --muted: #7A7266;
    --line: #DCD4C2;
}

.stApp {
    background: var(--paper);
    color: var(--ink);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, .desk-title {
    font-family: 'Source Serif 4', Georgia, serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em;
}

/* ---- header / masthead ---- */
.masthead {
    border-bottom: 2px solid var(--ink);
    padding-bottom: 14px;
    margin-bottom: 6px;
}
.masthead .eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 0.72rem;
    color: var(--accent);
}
.masthead h1 {
    font-size: 2.1rem;
    margin: 2px 0 4px 0;
}
.masthead p {
    color: var(--muted);
    font-size: 0.95rem;
    margin: 0;
}

/* ---- cards ---- */
.desk-card {
    background: var(--paper-2);
    border: 1px solid var(--line);
    border-radius: 4px;
    padding: 18px 20px;
    margin-bottom: 14px;
}

/* ---- match meter (signature element) ---- */
.match-meter-wrap {
    font-family: 'IBM Plex Mono', monospace;
}
.match-meter-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 6px;
}
.match-meter-score {
    color: var(--ink);
    font-weight: 600;
    font-size: 1.05rem;
}
.match-meter-track {
    position: relative;
    height: 22px;
    background: repeating-linear-gradient(
        90deg,
        var(--line) 0px, var(--line) 1px,
        transparent 1px, transparent 10%
    );
    border: 1px solid var(--ink);
    border-radius: 2px;
    overflow: hidden;
}
.match-meter-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), #D08A45);
}

/* ---- keyword chips ---- */
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    padding: 3px 8px;
    border-radius: 3px;
    border: 1px solid var(--line);
}
.chip-matched { background: #EAF1EC; color: var(--accent-2); border-color: #C6DACD; }
.chip-missing { background: #FBEFE6; color: var(--accent); border-color: #EAD2B8; }

/* ---- section divider ---- */
.desk-rule {
    border: none;
    border-top: 1px solid var(--line);
    margin: 18px 0;
}

/* ---- buttons ---- */
.stButton > button, .stDownloadButton > button {
    background: var(--ink);
    color: var(--paper);
    border-radius: 3px;
    border: none;
    font-weight: 500;
    padding: 0.5rem 1.1rem;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: var(--accent);
    color: white;
}

/* ---- resume preview paper ---- */
.resume-sheet {
    background: white;
    border: 1px solid var(--line);
    box-shadow: 0 2px 10px rgba(27,42,74,0.06);
    padding: 34px 40px;
    border-radius: 2px;
}
.resume-sheet h1 { font-size: 1.6rem; margin-bottom: 2px; }
.resume-sheet .contact-line { color: var(--muted); font-size: 0.88rem; margin-bottom: 2px; }
.resume-sheet h3 {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    border-bottom: 1px solid var(--line);
    padding-bottom: 3px;
    margin-top: 16px;
}
.resume-sheet li { margin-bottom: 4px; font-size: 0.92rem; line-height: 1.45; }

/* ---- sidebar ---- */
section[data-testid="stSidebar"] {
    background: #18263F;
    border-right: 1px solid #30405F;
}

/* ---- gap note ---- */
.gap-note {
    font-size: 0.85rem;
    color: var(--muted);
    border-left: 3px solid var(--accent);
    padding: 8px 12px;
    background: #FBF6EC;
    border-radius: 0 3px 3px 0;
}
</style>
"""
