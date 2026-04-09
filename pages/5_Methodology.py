import streamlit as st

st.set_page_config(page_title="Methodology", page_icon="🔬", layout="wide")

st.title("How this analysis was built")
st.caption("A step-by-step methodology for clinical coding intelligence — from EHR data to revenue insights")
st.divider()

# ── OVERVIEW ──────────────────────────────────────────────────
st.subheader("Overview")
st.markdown("""
This tool was built by a Ankita, Health Systems Product Manager working at a Healthcare organization using dummy EHR data, Python, pandas, and rule-based 
clinical coding logic grounded in **CMS 2021 E&M guidelines**. It analyzes raw EHR visit data 
to identify two types of revenue leakage:

1. **E&M undercoding** — visits where the submitted CPT code is lower than what the visit duration justifies
2. **Missing add-on codes** — qualifying visits where additional billable codes were never submitted
""")

st.divider()

# ── FLOWCHART ─────────────────────────────────────────────────
st.subheader("Analysis pipeline")

flowchart_html = """
<style>
  .flow-wrap { font-family: sans-serif; padding: 10px 0; }
  .phase-row { display: flex; gap: 0; align-items: stretch; margin-bottom: 0; }
  .phase-box { flex: 1; border-radius: 10px; padding: 14px 16px; margin: 4px; }
  .phase-title { font-size: 13px; font-weight: 600; margin-bottom: 6px; }
  .phase-desc { font-size: 11px; line-height: 1.6; }
  .phase-tag { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 20px; margin-top: 8px; }
  .arrow-row { display: flex; justify-content: center; align-items: center; margin: 2px 0; color: #888; font-size: 20px; }
  .step-row { display: flex; gap: 8px; align-items: stretch; }
  .step-box { flex: 1; border-radius: 8px; padding: 12px 14px; margin: 3px; border: 1px solid #ddd; }
  .step-num { font-size: 11px; font-weight: 700; margin-bottom: 4px; }
  .step-title { font-size: 12px; font-weight: 600; margin-bottom: 4px; }
  .step-desc { font-size: 11px; color: #555; line-height: 1.5; }
  .output-row { display: flex; gap: 8px; margin-top: 6px; }
  .output-box { flex: 1; background: #f0faf4; border: 1px solid #b2dfca; border-radius: 8px; padding: 10px 12px; margin: 3px; }
  .output-title { font-size: 11px; font-weight: 700; color: #1a7a4a; margin-bottom: 3px; }
  .output-desc { font-size: 10px; color: #2d6a4f; line-height: 1.5; }
</style>

<div class="flow-wrap">

  <!-- PHASE 1: DATA -->
  <div class="phase-row">
    <div class="phase-box" style="background:#E6F1FB;border:1px solid #185FA5;">
      <div class="phase-title" style="color:#0C447C;">Phase 1 — Data extraction</div>
      <div class="step-row">
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#185FA5;">STEP 1</div>
          <div class="step-title">EHR data request</div>
          <div class="step-desc">Requested visit-level extract from EHR vendor. Fields: Visit ID, Date, Location, Provider, Service Line, Visit Type, ICD-10 diagnoses (primary, secondary, tertiary), CPT code submitted, Visit duration, Lab orders, Payer, Visit note text</div>
        </div>
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#185FA5;">STEP 2</div>
          <div class="step-title">Data loading & inspection</div>
          <div class="step-desc">Loaded Excel file using pandas. Checked shape (250 visits × 34 columns), data types, and missing values. Confirmed Lab and Tertiary diagnosis nulls were expected — not data quality issues.</div>
        </div>
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#185FA5;">STEP 3</div>
          <div class="step-title">Exploratory analysis</div>
          <div class="step-desc">Analyzed visit distribution by service line (Primary Care 41%, BH 33%, Psychiatry 26%). Identified 99213 as most submitted code at 54 times. Mapped average duration by visit type to establish baseline.</div>
        </div>
      </div>
      <span class="phase-tag" style="background:#185FA5;color:#fff;">Python · pandas · openpyxl</span>
    </div>
  </div>

  <div class="arrow-row">↓</div>

  <!-- PHASE 2: E&M -->
  <div class="phase-row">
    <div class="phase-box" style="background:#FCEBEB;border:1px solid #E24B4A;">
      <div class="phase-title" style="color:#791F1F;">Phase 2 — E&M undercode detection (Step 3)</div>
      <div class="step-row">
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#E24B4A;">RULE 1</div>
          <div class="step-title">Expected CPT by time</div>
          <div class="step-desc">Applied CMS 2021 time-based E&M thresholds to every Primary Care visit:<br>
          ≤9 min → 99211 &nbsp;|&nbsp; 10–19 → 99212<br>
          20–29 → 99213 &nbsp;|&nbsp; 30–39 → 99214<br>
          40+ min → 99215</div>
        </div>
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#E24B4A;">RULE 2</div>
          <div class="step-title">Compare submitted vs expected</div>
          <div class="step-desc">Compared each visit's submitted CPT against the expected CPT. Flagged as UNDERCODED when submitted level was below expected. Flagged OVERCODED when above. Otherwise CORRECT.</div>
        </div>
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#E24B4A;">RESULT</div>
          <div class="step-title">Revenue gap calculation</div>
          <div class="step-desc">For each undercoded visit: Gap = Medicare rate (expected) − Medicare rate (submitted). Aggregated by provider, location, visit type, and payer. Total E&M gap: $1,540 across 31 visits (30.4% undercode rate).</div>
        </div>
      </div>
      <span class="phase-tag" style="background:#E24B4A;color:#fff;">CMS 2021 guidelines · Rule-based logic</span>
    </div>
  </div>

  <div class="arrow-row">↓</div>

  <!-- PHASE 3: ADD-ON -->
  <div class="phase-row">
    <div class="phase-box" style="background:#FAEEDA;border:1px solid #EF9F27;">
      <div class="phase-title" style="color:#633806;">Phase 3 — Add-on code gap detection (Step 4C)</div>
      <div class="step-row">
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#854F0B;">CHECK 1</div>
          <div class="step-title">CCM — 99490</div>
          <div class="step-desc">Flagged Primary Care visits where 2+ of the 3 diagnosis codes were chronic conditions (diabetes, hypertension, COPD, depression, etc.) and 99490 was not submitted. Value: $62/visit.</div>
        </div>
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#854F0B;">CHECK 2</div>
          <div class="step-title">BHI — 99484</div>
          <div class="step-desc">Flagged Primary Care visits where any diagnosis was a behavioral health ICD-10 code (F32.1, F41.1, etc.) and 99484 was not submitted. Indicates BH condition managed by PCP. Value: $45/visit.</div>
        </div>
        <div class="step-box" style="background:#fff;">
          <div class="step-num" style="color:#854F0B;">CHECK 3</div>
          <div class="step-title">G2211 + 90833</div>
          <div class="step-desc">G2211: flagged E&M visits with 3 diagnoses (complexity proxy). Value: $16. 90833: flagged Psychiatry visits typed as combined med mgmt + therapy where only E&M code submitted. Value: $65.</div>
        </div>
      </div>
      <span class="phase-tag" style="background:#854F0B;color:#fff;">CPT guidelines · ICD-10 logic · Medicare rates</span>
    </div>
  </div>

  <div class="arrow-row">↓</div>

  <!-- PHASE 4: OUTPUT -->
  <div class="phase-row">
    <div class="phase-box" style="background:#EAF3DE;border:1px solid #3B6D11;">
      <div class="phase-title" style="color:#27500A;">Phase 4 — Outputs & dashboard</div>
      <div class="output-row">
        <div class="output-box">
          <div class="output-title">Excel reports</div>
          <div class="output-desc">step3_undercode_results.xlsx and step4c_addon_results.xlsx — 9 sheets each with provider, location, payer, and visit-level detail. Shareable via SharePoint or email.</div>
        </div>
        <div class="output-box">
          <div class="output-title">Streamlit dashboard</div>
          <div class="output-desc">4-page interactive app built in Python. Executive summary, provider scorecard, add-on gap analysis, and flagged visit queue with CSV export for coding specialists.</div>
        </div>
        <div class="output-box">
          <div class="output-title">Business case</div>
          <div class="output-desc">$4,819 gap across 250 visits. Annualized to $28,000–$115,000+ depending on total visit volume. Provider-level findings ready for targeted coding education.</div>
        </div>
      </div>
      <span class="phase-tag" style="background:#3B6D11;color:#fff;">Streamlit · Plotly · pandas · openpyxl</span>
    </div>
  </div>

</div>
"""

st.components.v1.html(flowchart_html, height=820, scrolling=False)

st.divider()

# ── WHAT IS RULE BASED ────────────────────────────────────────
st.subheader("This is a rule-based model")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**What this tool does**")
    st.markdown("""
- Applies published CMS time thresholds to flag duration mismatches
- Checks ICD-10 diagnosis combinations against known add-on code qualifiers
- Calculates revenue gaps using Medicare average reimbursement rates
- Aggregates findings by provider, location, payer, and visit type
- All logic is transparent — every flag has a documented reason
    """)

with col2:
    st.markdown("**What comes next — AI/ML layer**")
    st.markdown("""
- **NLP on visit notes** — parse free-text notes to extract MDM complexity signals
- **ML model** — train a classifier to predict correct CPT from duration + diagnoses + visit type
- **Claude API** — send each note to an LLM to get a second opinion on coding
- **Anomaly detection** — unsupervised ML to find patterns no human thought to look for
- **Real-time flagging** — flag visits at point of care before the claim is submitted
    """)

st.divider()

# ── DATA SOURCES ──────────────────────────────────────────────
st.subheader("Data sources and references")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**CMS E&M guidelines**")
    st.caption("2021 Evaluation and Management Office Visit Guidelines. Time-based coding thresholds for 99211–99215.")
with col2:
    st.markdown("**Medicare reimbursement rates**")
    st.caption("2024 Medicare Physician Fee Schedule average national rates. Actual rates vary by geography and payer contract.")
with col3:
    st.markdown("**ICD-10-CM codes**")
    st.caption("2024 ICD-10-CM Official Guidelines. Chronic condition and behavioral health diagnosis classification.")

st.divider()