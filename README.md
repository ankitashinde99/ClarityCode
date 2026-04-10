# Clinical Coding Intelligence

> A data-driven tool that identifies revenue leakage from undercoded visits and missing add-on codes — built by a Health Systems Product Manager using Python, pandas, and Streamlit.

---

## The Problem

Healthcare organizations lose significant reimbursement revenue every day because:

- **Providers undercode visits** — submitting a lower E&M code than the visit duration justifies
- **Add-on codes are never submitted** — qualifying codes like CCM (99490), BHI (99484), and G2211 exist but are routinely missed
- **No visibility exists** — without a systematic review, these gaps are invisible until an external audit

---

## What This Tool Found

Analyzing **250 visits** across Primary Care, Behavioral Health, and Psychiatry:

| Finding | Result |
|---|---|
| Total revenue gap | **$4,819** (this sample) |
| E&M undercode rate | **30.4%** — 31 of 102 Primary Care visits |
| Missing add-on visits | **76 visits** — $3,279 unclaimed |
| Projected annual gap | **$76,000+** at 500 visits/month |

**Top findings:**
- 99213 was the most submitted code (54 times) — but Case Management, Chronic Disease, and Telehealth visits averaging 30–45 minutes justify 99214 or 99215
- Dr. Kevin Walsh missing the 90833 psychotherapy add-on on every combined visit — $845 in this sample, $10,140/year
- 31 patients qualify for Chronic Care Management (99490) at $62/month — $23,064/year in recurring revenue

---

## Live Dashboard

**[View the interactive dashboard →](https://ankitashinde99-coding-intelligence.streamlit.app)**

Four pages:
- Executive summary with revenue gap projector
- Provider analysis and scorecard
- Add-on code gaps by location and payer
- Flagged visit queue with CSV export

> **Note:** Dashboard runs on synthetic/de-identified data only. No real patient information is used.

---

## How It Works

This is a **rule-based system** — not AI. Every flag has a documented, auditable reason.

### Step 1 — Load and inspect
```bash
python step1_load_data.py
```
Loads the EHR Excel extract, checks shape, columns, and missing values.

### Step 2 — Exploratory analysis
```bash
python step2_explore.py
```
Visit distribution by service line, top CPT codes, average duration by visit type.

### Step 3 — E&M undercode detection
```bash
python step3_undercode_flag.py
```
Applies CMS 2021 time-based E&M thresholds to Primary Care visits:

| Duration | Expected Code |
|---|---|
| ≤ 9 min | 99211 |
| 10–19 min | 99212 |
| 20–29 min | 99213 |
| 30–39 min | 99214 |
| 40+ min | 99215 |

Flags visits where submitted code is below expected. Calculates revenue gap using Medicare average rates.

### Step 4C — Add-on code detector
```bash
python step4c_addon_code_detector.py
```
Checks four add-on code opportunities:

| Code | Description | Value |
|---|---|---|
| 99490 | Chronic Care Management — 2+ chronic conditions | $62/visit |
| 99484 | BH Integration — BH diagnosis in primary care visit | $45/visit |
| G2211 | Complex primary care add-on — 3 diagnoses | $16/visit |
| 90833 | Psychotherapy add-on — combined psych + therapy visit | $65/visit |

### Step 5 — Interactive dashboard
```bash
streamlit run dashboard_app.py
```

---

## Project Structure

```
coding_intelligence/
├── dashboard_app.py              # Streamlit dashboard — main app
├── ehr_raw_data.xlsx             # Synthetic EHR visit data (250 visits)
├── requirements.txt              # Python dependencies
├── step1_load_data.py            # Data loading and inspection
├── step2_explore.py              # Exploratory data analysis
├── step3_undercode_flag.py       # E&M undercode detection engine
├── step4c_addon_code_detector.py # Add-on code gap detector
├── pages/
│   └── 5_Methodology.py         # Streamlit methodology page
└── outputs/
    ├── step3_undercode_results.xlsx
    └── step4c_addon_results.xlsx
```

---

## Setup

```bash
# Clone the repo
git clone https://github.com/ankitashinde99/coding-intelligence.git
cd coding-intelligence

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard_app.py
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.13 | Core language |
| pandas | Data manipulation and analysis |
| openpyxl | Excel file reading and writing |
| Streamlit | Interactive web dashboard |
| Plotly | Charts and visualizations |
| GitHub | Version control |
| Streamlit Cloud | Free deployment |

---

## Data Sources and References

| Source | Used for |
|---|---|
| [CMS 2021 E&M Guidelines](https://www.cms.gov/medicare/physician-fee-schedule/2021-office-outpatient-evaluation-and-management) | Time-based E&M coding thresholds |
| [CMS Physician Fee Schedule](https://www.cms.gov/medicare/payment/fee-schedules/physician) | Medicare reimbursement rates |
| [CMS CCM Fact Sheet](https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/mlnproducts/downloads/chroniccaremanagement.pdf) | 99490 billing requirements |
| [CDC ICD-10-CM Browser](https://icd.cdc.gov/icd10cm/) | Diagnosis code classification |
| [AAPC CPT Code Lookup](https://www.aapc.com/codes/) | CPT code reference |

---

## What's Next — AI/ML Layer

This tool is rule-based today. The roadmap adds:

1. **Claude API on visit notes** — LLM analysis of free-text provider notes to extract MDM complexity signals
2. **ML classifier** — Random Forest trained on labeled visits to predict correct CPT code
3. **NLP pipeline** — ClinicalBERT or spaCy to parse clinical language from visit notes
4. **Real-time flagging** — flag visits at point of care before the claim is submitted
5. **Azure deployment** — HIPAA-compliant internal hosting for real patient data

---

## Important Notes

- All data in this repository is **synthetic** — no real patient information
- Revenue figures use **Medicare average national rates** — actual rates vary by payer and geography
- Every flagged visit requires **human review by a certified coder** before any action
- Self-pay patients should be **excluded** from CCM and G2211 recommendations — these are insurance-only codes

---

## About

Built by **Ankita Shinde** — Health Systems Product Manager with a background in business analytics and AI/ML.

This project demonstrates how product managers in healthcare can apply data science to solve real revenue cycle problems — without waiting for a vendor or a data team.

---

*Built with Python · Streamlit · pandas · CMS 2021 Guidelines*
