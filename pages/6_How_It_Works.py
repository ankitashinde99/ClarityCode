import streamlit as st

st.set_page_config(
    page_title="ClarityCode · How It Works",
    page_icon="⬡",
    layout="wide",
)

# ── THEME ─────────────────────────────────────────────────────
is_dark = st.session_state.get("dark_mode", True)

if is_dark:
    BG      = "#111111"; CARD_BG = "#1c1c1e"; TEXT    = "#f5f5f7"
    TEXT2   = "#ebebf5"; MUTED   = "#98989f"; BORDER  = "rgba(255,255,255,0.08)"
    PROB_BG = "linear-gradient(135deg,#1c1c1e 0%,#2c2c2e 100%)"
    GREEN   = "#34c759"; AMBER   = "#ff9500"; RED     = "#ff3b30"
    BLUE    = "#0071e3"; INS_BG  = "rgba(0,113,227,0.15)"; INS_BOR = "#0071e3"
    BG2     = "#2c2c2e"
else:
    BG      = "#f5f5f7"; CARD_BG = "#ffffff"; TEXT    = "#1d1d1f"
    TEXT2   = "#3a3a3c"; MUTED   = "#6e6e73"; BORDER  = "rgba(0,0,0,0.06)"
    PROB_BG = "linear-gradient(135deg,#f5f5f7 0%,#ffffff 100%)"
    GREEN   = "#1a8a3a"; AMBER   = "#b36200"; RED     = "#c0392b"
    BLUE    = "#0071e3"; INS_BG  = "rgba(0,113,227,0.06)"; INS_BOR = "#0071e3"
    BG2     = "#e8e8ed"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"] {{
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif !important;
    background-color: {BG} !important; color: {TEXT} !important;
    letter-spacing: -0.01em;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 2rem 2.5rem !important; max-width: 1080px; }}
[data-testid="stSidebar"] {{ background: {CARD_BG} !important; border-right: 1px solid {BORDER} !important; }}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="metric-container"] {{
    background: {CARD_BG} !important; border: 1px solid {BORDER} !important;
    border-radius: 14px !important; padding: 1rem 1.2rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.72rem !important; font-weight: 500 !important;
    color: {MUTED} !important; text-transform: uppercase; letter-spacing: 0.05em;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.7rem !important; font-weight: 600 !important;
    color: {TEXT} !important; letter-spacing: -0.04em;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.72rem !important; }}
h1 {{ font-size: 2rem !important; font-weight: 600 !important;
      color: {TEXT} !important; letter-spacing: -0.04em !important; }}
h2 {{ font-size: 1.2rem !important; font-weight: 600 !important;
      color: {TEXT} !important; letter-spacing: -0.02em !important; margin-top: 2rem !important; }}
p, li {{ color: {TEXT2} !important; line-height: 1.75 !important; }}
hr {{ border: none !important; border-top: 1px solid {BORDER} !important; margin: 1.8rem 0 !important; }}
[data-testid="stExpander"] {{
    border-radius: 12px !important; border: 1px solid {BORDER} !important;
    background: {CARD_BG} !important;
}}
[data-testid="stExpander"] * {{ color: {TEXT} !important; }}
[data-testid="stAlert"] {{ border-radius: 12px !important; }}

/* Step card */
.step-wrap {{
    display: flex; gap: 16px; margin-bottom: 1rem;
}}
.step-line {{
    display: flex; flex-direction: column; align-items: center;
}}
.step-dot {{
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem; font-weight: 700; color: #fff;
    flex-shrink: 0;
}}
.step-connector {{
    width: 2px; flex: 1; background: {BORDER}; margin-top: 6px;
}}
.step-content {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 1.3rem 1.5rem;
    flex: 1; margin-bottom: 0.5rem;
}}
.step-title {{
    font-size: 1rem; font-weight: 600; color: {TEXT}; margin-bottom: 0.3rem;
}}
.step-meta {{
    font-size: 0.75rem; color: {MUTED}; margin-bottom: 0.7rem;
}}
.step-body {{
    font-size: 0.9rem; color: {TEXT2}; line-height: 1.75;
}}
.chip {{
    display: inline-block; padding: 0.22rem 0.7rem;
    border-radius: 20px; font-size: 0.74rem; font-weight: 500;
    margin: 0.5rem 0.3rem 0 0;
}}
.ds-card {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 1.3rem 1.5rem;
}}
.ds-label {{
    font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; color: {MUTED}; margin-bottom: 0.4rem;
}}
.ds-val {{
    font-size: 1.7rem; font-weight: 600; color: {TEXT};
    letter-spacing: -0.04em; margin-bottom: 0.5rem;
}}
.ds-body {{
    font-size: 0.84rem; color: {MUTED}; line-height: 1.85;
}}
.ins-bar {{
    background: {INS_BG}; border-left: 3px solid {INS_BOR};
    border-radius: 0 8px 8px 0; padding: 0.6rem 1rem;
    font-size: 0.84rem; color: {TEXT}; margin-top: 0.8rem; line-height: 1.55;
}}
.built-row {{
    display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-top: 0.5rem;
}}
.built-box {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 1rem 1.1rem;
}}
.built-label {{
    font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; color: {MUTED}; margin-bottom: 0.5rem;
}}
.built-body {{
    font-size: 0.85rem; color: {TEXT}; line-height: 1.85;
}}
.limit-grid {{
    display: grid; grid-template-columns: repeat(2,1fr); gap: 10px; margin-top: 0.5rem;
}}
.limit-box {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 10px; padding: 0.9rem 1rem;
}}
.limit-title {{
    font-size: 0.85rem; font-weight: 600; color: {TEXT}; margin-bottom: 0.3rem;
}}
.limit-body {{
    font-size: 0.8rem; color: {MUTED}; line-height: 1.65;
}}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────
st.title("How ClarityCode works")
st.caption("A walkthrough of the analysis — what was built, how it works, and what it found")
st.divider()

# ── PROBLEM ───────────────────────────────────────────────────
st.markdown(f"""
<div style='background:{PROB_BG};border:1px solid {BORDER};border-radius:20px;
            padding:1.8rem 2.2rem;margin-bottom:1.5rem;'>
  <div style='font-size:1.25rem;font-weight:600;color:{TEXT};
              letter-spacing:-0.03em;line-height:1.35;margin-bottom:0.75rem;'>
    Healthcare organizations lose revenue every month from two silent problems.
  </div>
  <div style='font-size:0.92rem;color:{MUTED};line-height:1.85;max-width:800px;'>
    <strong style='color:{TEXT};'>Problem 1 — Visits billed too low.</strong>
    Providers submit billing codes lower than what the visit duration supports.
    A 40-minute visit billed as a 20-minute visit loses over $100 in reimbursement
    — silently, every time it happens.<br><br>
    <strong style='color:{TEXT};'>Problem 2 — Qualifying billing codes never submitted.</strong>
    Certain types of care qualify for additional reimbursement on top of the main visit code.
    Most providers do not know these codes exist. The care is delivered,
    the code is never submitted, and the payment is never collected.<br><br>
    ClarityCode was built to surface both problems using a structured, evidence-based
    approach — so your billing team has specific visits, specific evidence, and a clear
    path to act.
  </div>
  <span style='display:inline-block;background:rgba(0,113,227,0.1);color:{BLUE};
               border-radius:20px;padding:0.22rem 0.85rem;font-size:0.74rem;
               font-weight:500;margin-top:1rem;'>
    Analysis based on CMS 2021 federal billing guidelines
  </span>
</div>
""", unsafe_allow_html=True)

# ── DATASETS ──────────────────────────────────────────────────
st.markdown("## The data")
st.markdown(f"<p style='color:{MUTED};font-size:0.88rem;margin-bottom:0.8rem;'>Two datasets were analyzed — one for rule-based analysis, one for AI-assisted note review.</p>", unsafe_allow_html=True)

d1, d2 = st.columns(2)
with d1:
    st.markdown(f"""
    <div class='ds-card'>
      <div class='ds-label'>Dataset 1 — EHR Visit Extract</div>
      <div class='ds-val'>250 visits</div>
      <div class='ds-body'>
        34 data fields per visit<br>
        Primary Care · Behavioral Health · Psychiatry<br>
        7 New York clinic locations · 10 providers<br>
        Multiple insurance payers<br><br>
        <strong style='color:{TEXT};'>Used for:</strong>
        Overview, Provider Insights, Missing Billing Codes, Review Queue
      </div>
    </div>""", unsafe_allow_html=True)
with d2:
    st.markdown(f"""
    <div class='ds-card'>
      <div class='ds-label'>Dataset 2 — Clinical Note Dataset</div>
      <div class='ds-val'>50 visits</div>
      <div class='ds-body'>
        Full SOAP notes per visit<br>
        (Subjective · Objective · Assessment · Plan)<br>
        Documented conditions, medications, lab results, referrals<br>
        Same providers and locations as Dataset 1<br><br>
        <strong style='color:{TEXT};'>Used for:</strong>
        AI Analysis page only
      </div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── STEPS ─────────────────────────────────────────────────────
st.markdown("## The analysis — four steps")
st.markdown(f"<p style='color:{MUTED};font-size:0.88rem;margin-bottom:1.2rem;'>Each step ran independently. Results were then cross-referenced — visits flagged by multiple steps carry the highest confidence.</p>", unsafe_allow_html=True)

# STEP 1
st.markdown(f"""
<div class='step-wrap'>
  <div class='step-line'>
    <div class='step-dot' style='background:{BLUE};'>01</div>
    <div class='step-connector'></div>
  </div>
  <div class='step-content'>
    <div class='step-title'>Billing level check — every Primary Care visit</div>
    <div class='step-meta'>📂 EHR extract · 102 Primary Care visits · CMS 2021 time thresholds</div>
    <div class='step-body'>
      Federal billing guidelines define exactly how long a visit must be to justify each
      billing code. Every Primary Care visit's documented duration was compared against
      these thresholds. Visits where the submitted code was lower than the duration supports
      were flagged, and the revenue gap was calculated.
      <br><br>
      The comparison is objective — the rules are published federal guidance, not
      subjective judgment. A 38-minute visit should be billed as 99214. If 99213 was
      submitted, the $44 gap is documented and traceable.
    </div>
    <div>
      <span class='chip' style='background:rgba(255,59,48,0.1);color:{RED};'>31 visits undercoded</span>
      <span class='chip' style='background:rgba(255,59,48,0.1);color:{RED};'>30.4% undercode rate</span>
      <span class='chip' style='background:rgba(255,59,48,0.1);color:{RED};'>$1,540 revenue gap</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.expander("CMS 2021 billing thresholds used"):
    c1,c2,c3,c4,c5 = st.columns(5)
    for col, code, time, rate in zip(
        [c1,c2,c3,c4,c5],
        ["99211","99212","99213","99214","99215"],
        ["1–9 min","10–19 min","20–29 min","30–39 min","40+ min"],
        ["$24","$55","$92","$136","$193"]
    ):
        col.metric(code, rate, time)
    st.caption("Medicare average national rates. Actual rates vary by payer and contract.")

# STEP 2
st.markdown(f"""
<div class='step-wrap'>
  <div class='step-line'>
    <div class='step-dot' style='background:{AMBER};'>02</div>
    <div class='step-connector'></div>
  </div>
  <div class='step-content'>
    <div class='step-title'>Missing billing codes — qualifying visits never claimed</div>
    <div class='step-meta'>📂 EHR extract · All 250 visits · Diagnosis and visit type matching</div>
    <div class='step-body'>
      Four additional billing codes were checked across every visit. Each code has a
      specific clinical trigger — a combination of diagnosis codes, visit type, or
      service line — that can be identified from structured EHR data without reading
      clinical notes. Any visit that met the qualifying criteria but did not have the
      corresponding code submitted was flagged.
      <br><br>
      These codes represent care that was already delivered. Submitting them is not
      adding work — it is capturing reimbursement for work that was done.
    </div>
    <div>
      <span class='chip' style='background:rgba(255,149,0,0.1);color:{AMBER};'>76 visits missing codes</span>
      <span class='chip' style='background:rgba(255,149,0,0.1);color:{AMBER};'>$3,279 unclaimed</span>
      <span class='chip' style='background:rgba(255,149,0,0.1);color:{AMBER};'>4 codes checked</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.expander("The four billing codes checked"):
    r1, r2 = st.columns(2)
    codes = [
        ("99490 — Chronic Care Management · $62/month",
         "For patients with two or more chronic conditions. Covers monthly care coordination. "
         "Recurring — every qualifying patient generates this revenue every month."),
        ("99484 — Behavioral Health Integration · $45/visit",
         "When a behavioral health diagnosis is managed in a Primary Care setting. "
         "The PCP is already doing this work — the code just needs to be submitted."),
        ("G2211 — Complex Care Add-on · $16/visit",
         "For Primary Care visits with high diagnosis complexity. "
         "Identified when all three diagnosis fields are populated in the visit record."),
        ("90833 — Therapy Session Add-on · $65/visit",
         "For Psychiatry visits where medication management and psychotherapy were "
         "both delivered in the same session, but only the medication code was submitted."),
    ]
    for i, (title, desc) in enumerate(codes):
        with [r1, r2][i % 2]:
            st.markdown(f"""
            <div style='background:{BG};border:1px solid {BORDER};border-radius:10px;
                        padding:0.9rem;margin-bottom:10px;'>
              <div style='font-size:0.75rem;font-weight:600;color:{BLUE};
                          margin-bottom:0.3rem;'>{title}</div>
              <div style='font-size:0.82rem;color:{MUTED};line-height:1.65;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

# STEP 3
st.markdown(f"""
<div class='step-wrap'>
  <div class='step-line'>
    <div class='step-dot' style='background:{GREEN};'>03</div>
    <div class='step-connector'></div>
  </div>
  <div class='step-content'>
    <div class='step-title'>Clinical note review — beyond visit duration</div>
    <div class='step-meta'>📂 Clinical note dataset · 50 visits · AI-assisted MDM analysis</div>
    <div class='step-body'>
      Steps 1 and 2 only use structured data — duration and diagnosis codes. They cannot
      read what was actually documented in the visit. A 28-minute visit might warrant a
      higher code if the provider managed multiple chronic conditions, reviewed lab results,
      and placed a specialist referral — even though the time alone suggests 99213.
      <br><br>
      To capture this, each clinical note was reviewed using an AI-assisted process that
      applies the same CMS Medical Decision Making (MDM) framework a certified coder
      uses — analyzing the number of problems addressed, data reviewed, risk level,
      and documented time. The result is a coding recommendation with a written
      explanation of the clinical evidence that supports it.
    </div>
    <div>
      <span class='chip' style='background:rgba(255,59,48,0.1);color:{RED};'>30 billed too low (62%)</span>
      <span class='chip' style='background:rgba(52,199,89,0.1);color:{GREEN};'>10 correctly billed (25%)</span>
      <span class='chip' style='background:rgba(255,149,0,0.1);color:{AMBER};'>6 billed too high — compliance risk (12%)</span>
      <span class='chip' style='background:rgba(255,59,48,0.1);color:{RED};'>$1,545 identified</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.expander("How clinical note review works"):
    st.markdown(f"""
    <div style='font-size:0.88rem;color:{TEXT2};line-height:1.85;'>
    CMS 2021 guidelines allow providers to code by time <em>or</em> by Medical Decision
    Making (MDM) complexity — whichever supports the higher code. A rule-based system
    using duration alone misses cases where the documented complexity justifies a higher
    level than the time would suggest.<br><br>
    <strong style='color:{TEXT};'>What MDM analysis looks at:</strong><br>
    • Number and complexity of problems addressed in the visit<br>
    • Amount and type of data reviewed — labs, records, specialist notes<br>
    • Risk level — new prescriptions, medication adjustments, referrals placed<br>
    • Total time documented by the provider<br><br>
    <strong style='color:{TEXT};'>What the output includes:</strong><br>
    Each reviewed visit produces a recommended billing code, a confidence level,
    the coding pathway used (time or MDM), and a plain-English explanation of
    the specific clinical evidence that supports the recommendation — the same
    language a certified coder would use in an audit finding.
    </div>
    """, unsafe_allow_html=True)

# STEP 4
st.markdown(f"""
<div class='step-wrap'>
  <div class='step-line'>
    <div class='step-dot' style='background:#8b5cf6;'>04</div>
  </div>
  <div class='step-content'>
    <div class='step-title'>Clinical complexity scoring — independent verification</div>
    <div class='step-meta'>📂 Clinical note dataset · 50 visits · Signal extraction + weighted scoring</div>
    <div class='step-body'>
      As a second independent method on the same clinical notes, six specific signals
      were extracted from each note and combined into a complexity score from 0 to 100.
      That score was mapped to the appropriate billing code using CMS MDM thresholds.
      <br><br>
      This step runs entirely on pattern matching — no AI model involved. When this
      scoring method and the Step 3 note review both flag the same visit, the finding
      is confirmed by two independent methods simultaneously. Those visits are surfaced
      separately in the dashboard as the highest-confidence cases for billing review.
    </div>
    <div>
      <span class='chip' style='background:rgba(139,92,246,0.1);color:#8b5cf6;'>Score range 30–94</span>
      <span class='chip' style='background:rgba(139,92,246,0.1);color:#8b5cf6;'>Average 68 / 100</span>
      <span class='chip' style='background:rgba(52,199,89,0.1);color:{GREEN};'>30 visits confirmed by both methods</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.expander("The six scoring signals"):
    cols = st.columns(3)
    signals = [
        ("Problems addressed", "30 pts",
         "Counts numbered clinical problems in the Assessment & Plan. More problems = higher complexity."),
        ("Tests reviewed", "20 pts",
         "Detects lab and diagnostic test references — blood panels, imaging, specialist results."),
        ("Risk language", "20 pts",
         "Identifies clinical risk indicators — uncontrolled conditions, new diagnoses, acute presentations."),
        ("Time documented", "15 pts",
         "Extracts explicitly stated visit time. When time is documented, the higher of time or complexity score is used."),
        ("Referrals placed", "10 pts",
         "Detects outgoing specialist referrals — cardiology, nephrology, psychiatry, and others."),
        ("Patient education", "5 pts",
         "Checks whether provider-delivered patient education was documented in the note."),
    ]
    for i, (title, pts, desc) in enumerate(signals):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='background:{BG};border:1px solid {BORDER};border-radius:10px;
                        padding:0.8rem;margin-bottom:10px;'>
              <div style='font-size:0.74rem;font-weight:600;color:{BLUE};'>{title}</div>
              <div style='font-size:1.1rem;font-weight:600;color:{TEXT};margin:0.2rem 0;'>{pts}</div>
              <div style='font-size:0.78rem;color:{MUTED};line-height:1.6;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

st.divider()

# ── COMBINED RESULTS ──────────────────────────────────────────
st.markdown("## Combined findings")
st.markdown(f"<p style='color:{MUTED};font-size:0.88rem;margin-bottom:0.8rem;'>Results across all four steps.</p>", unsafe_allow_html=True)

r1,r2,r3,r4,r5 = st.columns(5)
r1.metric("Total visits analyzed",  "300",      "250 EHR + 50 notes")
r2.metric("E&M billing gap",        "$1,540",   "31 undercoded visits")
r3.metric("Missing code gap",       "$3,279",   "76 qualifying visits")
r4.metric("Note review gap",        "$1,545",   "50 notes reviewed")
r5.metric("Projected annual gap",   "$76,000+", "At 500 visits/month")

st.markdown(f"""
<div class='ins-bar'>
  💡 The $4,819 gap on the Overview page comes from Steps 1 and 2 — rule-based analysis
  of 250 visits. The $1,545 note review gap comes from Step 3 on a separate 50-visit
  dataset. These are complementary findings, not overlapping counts.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── WHAT WAS BUILT ────────────────────────────────────────────
st.markdown("## What was built")
st.markdown(f"""
<div class='built-row'>
  <div class='built-box'>
    <div class='built-label'>Analysis pipeline</div>
    <div class='built-body'>
      A Python-based pipeline that applies CMS 2021 billing rules to structured
      EHR data — automatically flagging undercoded visits and missing billing
      codes with calculated revenue gaps.
    </div>
  </div>
  <div class='built-box'>
    <div class='built-label'>Clinical note review</div>
    <div class='built-body'>
      An AI-assisted process that reads clinical notes and applies Medical
      Decision Making guidelines — producing coded recommendations with
      written clinical justifications for each visit.
    </div>
  </div>
  <div class='built-box'>
    <div class='built-label'>Interactive dashboard</div>
    <div class='built-body'>
      A web-based dashboard with real-time filters, provider scorecards,
      a flagged visit review queue with CSV export, and an annual
      revenue gap projector.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── LIMITATIONS ───────────────────────────────────────────────
st.markdown("## Before acting on any finding")
st.markdown(f"""
<div class='limit-grid'>
  <div class='limit-box'>
    <div class='limit-title'>These are potential discrepancies — not confirmed errors</div>
    <div class='limit-body'>
      Every flagged visit must be reviewed by a certified medical coder before
      any claim is modified. ClarityCode identifies candidates for review —
      your team makes the final call.
    </div>
  </div>
  <div class='limit-box'>
    <div class='limit-title'>Revenue figures use Medicare average rates</div>
    <div class='limit-body'>
      Actual reimbursement varies by payer and contract. Commercial payers
      typically reimburse at higher rates — meaning the actual gap may be
      larger than shown.
    </div>
  </div>
  <div class='limit-box'>
    <div class='limit-title'>Self-pay patients must be excluded</div>
    <div class='limit-body'>
      Chronic Care Management (99490) and G2211 are insurance-only codes.
      Any self-pay patient flagged for these codes should be removed
      before any billing action is taken.
    </div>
  </div>
  <div class='limit-box'>
    <div class='limit-title'>This dashboard uses synthetic data</div>
    <div class='limit-body'>
      No real patient information was used. Applying this analysis to real
      EHR data requires HIPAA-compliant infrastructure and a certified
      coder to validate findings before submission.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── REFERENCES ────────────────────────────────────────────────
st.markdown("## Official sources")
refs = {
    "CMS 2021 E&M Guidelines": "https://www.cms.gov/medicare/physician-fee-schedule/2021-office-outpatient-evaluation-and-management",
    "Medicare Physician Fee Schedule": "https://www.cms.gov/medicare/payment/fee-schedules/physician",
    "Chronic Care Management (99490)": "https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/mlnproducts/downloads/chroniccaremanagement.pdf",
    "AAPC CPT Code Reference": "https://www.aapc.com/codes/",
    "ICD-10-CM Browser": "https://icd.cdc.gov/icd10cm/",
    "OIG Compliance Work Plan": "https://oig.hhs.gov/reports-and-publications/workplan/",
}
cols = st.columns(3)
for i, (name, url) in enumerate(refs.items()):
    cols[i % 3].markdown(f"[{name}]({url})")

st.markdown("---")
st.caption("ClarityCode v2.0 · Built by Ankita Shinde · Health Systems Product Manager · "
           "Synthetic data only · github.com/ankitashinde99/coding-intelligence")
