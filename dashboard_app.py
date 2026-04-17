import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="ClarityCode",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── THEME TOGGLE ──────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

is_dark = st.session_state.dark_mode

if is_dark:
    BG        = "#111111"
    BG2       = "#1c1c1e"
    BG3       = "#2c2c2e"
    TEXT      = "#f5f5f7"
    TEXT2     = "#ebebf5"
    MUTED     = "#98989f"
    BORDER    = "rgba(255,255,255,0.08)"
    CARD_BG   = "#1c1c1e"
    PLOT_BG   = "rgba(0,0,0,0)"
    GRID_C    = "rgba(255,255,255,0.06)"
    FONT_C    = "#f5f5f7"
    SIDEBAR   = "#1c1c1e"
    INS_BG    = "rgba(0,113,227,0.15)"
    INS_BOR   = "#0071e3"
    HELP_BG   = "#2c2c2e"
    BTN_LABEL = "☀️  Light mode"
else:
    BG        = "#f5f5f7"
    BG2       = "#ffffff"
    BG3       = "#e8e8ed"
    TEXT      = "#1d1d1f"
    TEXT2     = "#3a3a3c"
    MUTED     = "#6e6e73"
    BORDER    = "rgba(0,0,0,0.06)"
    CARD_BG   = "#ffffff"
    PLOT_BG   = "rgba(0,0,0,0)"
    GRID_C    = "rgba(0,0,0,0.05)"
    FONT_C    = "#1d1d1f"
    SIDEBAR   = "rgba(250,250,252,0.95)"
    INS_BG    = "rgba(0,113,227,0.06)"
    INS_BOR   = "#0071e3"
    HELP_BG   = "#f5f5f7"
    BTN_LABEL = "🌙  Dark mode"

BLUE  = "#0071e3"
RED   = "#ff3b30"
GREEN = "#34c759"
AMBER = "#ff9500"

# ── CSS ───────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif !important;
    letter-spacing: -0.01em;
    background-color: {BG} !important;
    color: {TEXT} !important;
}}
footer {{ display: none !important; }}
#MainMenu {{ visibility: hidden !important; }}
.block-container {{ padding-top: 1.5rem !important; padding-right: 2.5rem !important; padding-bottom: 2rem !important; }}

[data-testid="stSidebar"] {{
    background: {SIDEBAR} !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
/* Hide auto-generated MPA nav at top of sidebar */
[data-testid="stSidebarNav"] {{ display: none !important; }}

[data-testid="metric-container"] {{
    background: {CARD_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.74rem !important; font-weight: 500 !important;
    color: {MUTED} !important; text-transform: uppercase; letter-spacing: 0.05em;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.9rem !important; font-weight: 600 !important;
    color: {TEXT} !important; letter-spacing: -0.04em;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.74rem !important; }}

h1 {{ font-size: 2rem !important; font-weight: 600 !important;
      color: {TEXT} !important; letter-spacing: -0.04em !important; }}
h2 {{ font-size: 1.3rem !important; font-weight: 600 !important;
      color: {TEXT} !important; letter-spacing: -0.02em !important; margin-top: 1.5rem !important; }}
h3 {{ font-size: 1.05rem !important; font-weight: 500 !important; color: {TEXT} !important; }}
p, li, span {{ color: {TEXT2} !important; }}
.stCaption, .stCaption * {{ color: {MUTED} !important; font-size: 0.8rem !important; }}

hr {{ border: none !important; border-top: 1px solid {BORDER} !important; margin: 1.5rem 0 !important; }}

[data-testid="stSelectbox"] > div > div {{
    border-radius: 10px !important; border: 1px solid {BORDER} !important;
    background: {CARD_BG} !important; color: {TEXT} !important;
}}
.stSlider > div > div > div > div {{ background: {BLUE} !important; }}

[data-testid="stDataFrame"] {{
    border-radius: 12px !important; overflow: hidden;
    border: 1px solid {BORDER} !important;
}}
[data-testid="stExpander"] {{
    border-radius: 12px !important; border: 1px solid {BORDER} !important;
    background: {CARD_BG} !important;
}}
[data-testid="stExpander"] * {{ color: {TEXT} !important; }}
[data-baseweb="tab"] {{ font-weight: 500 !important; color: {TEXT} !important; }}
[data-baseweb="tab-panel"] {{ background: transparent !important; }}
[data-testid="stAlert"] {{ border-radius: 12px !important; }}

.page-header {{
    border-left: 3px solid {BLUE};
    padding: 0.15rem 0 0.3rem 1rem;
    margin-bottom: 0.8rem;
}}
.prob-head {{
    font-size: 1.25rem; font-weight: 600; color: {TEXT};
    letter-spacing: -0.03em; line-height: 1.4; margin-bottom: 0.45rem;
}}
.prob-body {{ font-size: 0.9rem; color: {MUTED}; line-height: 1.75; max-width: 740px; }}
.prob-pill {{
    display: inline-block; background: rgba(0,113,227,0.1);
    color: {BLUE}; border-radius: 20px; padding: 0.18rem 0.75rem;
    font-size: 0.72rem; font-weight: 500; margin-top: 0.7rem; letter-spacing: 0.02em;
}}
.ins-bar {{
    background: {INS_BG}; border-left: 3px solid {INS_BOR};
    border-radius: 0 8px 8px 0; padding: 0.55rem 1rem;
    font-size: 0.83rem; color: {TEXT}; margin-top: 0.6rem; line-height: 1.55;
}}
.section-heading {{
    display: flex; align-items: center; gap: 7px;
    margin: 0.6rem 0 0.3rem; line-height: 1;
}}
.section-heading span.heading-text {{
    font-size: 1.05rem; font-weight: 700; color: {TEXT}; line-height: 1.2;
}}
.help-icon {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 16px; height: 16px; border-radius: 50%; flex-shrink: 0;
    background: transparent; border: 1.5px solid {MUTED};
    font-size: 0.6rem; font-weight: 800; color: {MUTED};
    cursor: help; position: relative;
    transition: border-color 0.15s, color 0.15s; align-self: center;
}}
.help-icon:hover {{ border-color: {BLUE}; color: {BLUE}; }}
.help-icon .help-tooltip {{
    visibility: hidden; opacity: 0;
    background: #18181b; color: #f4f4f5;
    border: 1px solid #3f3f46;
    font-size: 0.78rem; font-weight: 400; line-height: 1.65;
    border-radius: 10px; padding: 10px 14px;
    width: 260px; position: absolute;
    bottom: calc(100% + 10px); left: 50%; transform: translateX(-50%);
    box-shadow: 0 12px 32px rgba(0,0,0,0.45);
    transition: opacity 0.15s ease; z-index: 9999;
    white-space: normal; pointer-events: none; text-align: left;
}}
.help-icon .help-tooltip::after {{
    content: ""; position: absolute; top: 100%; left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent; border-top-color: #3f3f46;
}}
.help-icon:hover .help-tooltip {{ visibility: visible; opacity: 1; }}
.nav-lbl {{
    font-size: 0.68rem; font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.08em; color: {MUTED}; margin: 1rem 0 0.3rem;
}}
.info-card {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 1.2rem 1.4rem;
}}
.info-label {{
    font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.07em; color: {MUTED}; margin-bottom: 0.5rem;
}}
.info-value {{
    font-size: 1.6rem; font-weight: 600; color: {TEXT};
    letter-spacing: -0.03em;
}}
.info-body {{ font-size: 0.85rem; color: {MUTED}; line-height: 1.9; margin-top: 0.4rem; }}
.tech-card {{
    background: {CARD_BG}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 1rem 1.2rem;
}}
</style>
""", unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────
def insight(text):
    st.markdown(f"<div class='ins-bar'>💡 {text}</div>", unsafe_allow_html=True)

def whatis(label, text):
    st.markdown(f"""
    <div class='section-heading'>
      <span class='heading-text'>{label}</span>
      <span class='help-icon'>?<span class='help-tooltip'>{text}</span></span>
    </div>""", unsafe_allow_html=True)

def prob_card(headline, body, pill=None):
    pill_html = f"<span class='prob-pill'>{pill}</span>" if pill else ""
    st.markdown(f"""
    <div class='page-header'>
      <div class='prob-head'>{headline}</div>
      <div class='prob-body'>{body}</div>
      {pill_html}
    </div>""", unsafe_allow_html=True)

def make_plot_cfg(font_color=None):
    return dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PLOT_BG,
        font=dict(
            family="-apple-system, BlinkMacSystemFont, 'Helvetica Neue'",
            color=font_color or FONT_C,
        ),
        margin=dict(t=24, b=16, l=0, r=0),
    )

def make_grid():
    return dict(gridcolor=GRID_C, zerolinecolor=GRID_C)

# ── LOAD DATA ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("ehr_raw_data.xlsx", sheet_name="Raw Visit Data")
    df["Visit_Date"] = pd.to_datetime(df["Visit_Date"])
    CHRONIC = ["I10","E11.9","E78.5","E66.9","J44.1","E03.9",
               "I25.10","F32.1","F41.1","F33.0","F31.9","K21.0"]
    BH_DX   = ["F32.1","F41.1","F33.0","F43.10","F31.9",
               "F10.20","F40.10","F34.1","F43.22","F60.3"]
    EM_ORDER= ["99211","99212","99213","99214","99215"]
    EM_RATE = {"99211":24,"99212":55,"99213":92,"99214":136,"99215":193}

    def expected_cpt(m):
        if pd.isna(m): return None
        m = int(m)
        if m<=9:  return "99211"
        if m<=19: return "99212"
        if m<=29: return "99213"
        if m<=39: return "99214"
        return "99215"

    def flag(row):
        s,e = row["CPT_Code_Submitted"], row["Expected_CPT"]
        if s not in EM_ORDER or e not in EM_ORDER: return "Non E&M"
        si,ei = EM_ORDER.index(s), EM_ORDER.index(e)
        if si < ei: return "UNDERCODED"
        if si > ei: return "OVERCODED"
        return "CORRECT"

    def rev_gap(row):
        if row["Coding_Flag"] != "UNDERCODED": return 0.0
        return EM_RATE.get(row["Expected_CPT"],0) - EM_RATE.get(row["CPT_Code_Submitted"],0)

    pc = df[df["Service_Line"]=="Primary Care"].copy()
    pc["Expected_CPT"]  = pc["Visit_Duration_Min"].apply(expected_cpt)
    pc["Coding_Flag"]   = pc.apply(flag, axis=1)
    pc["Revenue_Gap"]   = pc.apply(rev_gap, axis=1)
    pc["Chronic_Count"] = pc.apply(lambda r: sum(
        str(r.get(c,"")) in CHRONIC
        for c in ["Primary_ICD10_Code","Secondary_ICD10_Code","Tertiary_ICD10_Code"]), axis=1)
    pc["CCM_Missing"]   = (pc["Chronic_Count"]>=2) & (pc["CPT_Code_Submitted"]!="99490")
    pc["BHI_Missing"]   = pc.apply(lambda r: any(
        str(r.get(c,"")) in BH_DX
        for c in ["Primary_ICD10_Code","Secondary_ICD10_Code","Tertiary_ICD10_Code"]),
        axis=1) & (pc["CPT_Code_Submitted"]!="99484")
    pc["G2211_Missing"] = (
        pc["CPT_Code_Submitted"].isin(["99212","99213","99214","99215"]) &
        pc["Tertiary_ICD10_Code"].notna() &
        (pc["Tertiary_ICD10_Code"].astype(str).str.strip()!="nan"))

    psych = df[df["Service_Line"]=="Psychiatry"].copy()
    psych["90833_Missing"] = (
        (psych["Visit_Type"]=="Psychotherapy + Med Mgmt") &
        psych["CPT_Code_Submitted"].isin(["99212","99213","99214","99215"]))
    return df, pc, psych

df, pc, psych = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⬡ ClarityCode")
    st.page_link("pages/6_How_It_Works.py", label="How It Works", icon="📖")
    st.divider()
    st.markdown(f"<div class='nav-lbl'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio("", [
        "Overview",
        "Provider Insights",
        "AI Analysis",
        "Missing Billing Codes",
        "Review Queue",
    ], label_visibility="collapsed")
    st.markdown(f"<div class='nav-lbl'>Filters</div>", unsafe_allow_html=True)
    sel_loc   = st.selectbox("Location",
        ["All locations"] + sorted(df["Location"].unique().tolist()),
        label_visibility="collapsed")
    sel_payer = st.selectbox("Insurance",
        ["All payers"] + sorted(df["Payer"].dropna().unique().tolist()),
        label_visibility="collapsed")
    st.markdown("---")
    st.caption("ClarityCode v2.0 · Synthetic data only")

def apply_f(data):
    d = data.copy()
    if sel_loc   != "All locations": d = d[d["Location"]==sel_loc]
    if sel_payer != "All payers":    d = d[d["Payer"]==sel_payer]
    return d

df_f    = apply_f(df)
pc_f    = apply_f(pc)
psych_f = apply_f(psych)

total_visits   = len(df_f)
undercoded     = (pc_f["Coding_Flag"]=="UNDERCODED").sum()
undercode_rate = undercoded/len(pc_f)*100 if len(pc_f)>0 else 0
em_gap         = pc_f["Revenue_Gap"].sum()
ccm_gap        = pc_f["CCM_Missing"].sum()*62
bhi_gap        = pc_f["BHI_Missing"].sum()*45
g2211_gap      = pc_f["G2211_Missing"].sum()*16
addon_90833    = psych_f["90833_Missing"].sum()*65
total_addon    = ccm_gap+bhi_gap+g2211_gap+addon_90833
total_gap      = em_gap+total_addon

# ══════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("ClarityCode")
    st.caption(f"Billing intelligence across {total_visits:,} visits · Primary Care, Behavioral Health, Psychiatry")
    st.divider()

    prob_card(
        "Your organization may be losing thousands of dollars every month, without knowing it.",
        "When providers see patients, they submit billing codes that describe the visit. "
        "If those codes are set too low — or qualifying codes are missed entirely — "
        "insurance pays less than what the visit was worth. This happens silently, visit after visit. "
        "<strong>ClarityCode</strong> surfaces exactly where billing does not match the care delivered — so your team can act on it.",
        pill="Based on CMS 2021 federal billing guidelines"
    )

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Estimated revenue gap",   f"${total_gap:,.0f}",  "Billing + missing codes")
    c2.metric("Visits billed too low",   f"{undercode_rate:.1f}%", f"{undercoded} of {len(pc_f)} primary care visits")
    c3.metric("Unclaimed billing codes", f"${total_addon:,.0f}", "Never submitted")
    c4.metric("Total visits reviewed",   f"{total_visits:,}",    "3 service lines")

    st.divider()
    # Scope note
    loc_label   = sel_loc   if sel_loc   != "All locations" else "all locations"
    payer_label = sel_payer if sel_payer != "All payers"    else "all payers"
    st.markdown(f"""
    <div style='font-size:0.8rem;color:{MUTED};margin-bottom:1rem;
                border:1px solid {BORDER};border-radius:10px;padding:0.55rem 1rem;
                display:inline-block;'>
        📊 &nbsp;Showing all 3 service lines
        &nbsp;·&nbsp; Location: <strong style='color:{TEXT}'>{loc_label}</strong>
        &nbsp;·&nbsp; Payer: <strong style='color:{TEXT}'>{payer_label}</strong>
    </div>""", unsafe_allow_html=True)

    PC = make_plot_cfg(); GR = make_grid()

    whatis("Where is the billing problem happening? (Primary Care E&M)",
               "Billing codes describe visit complexity by time:<br>"
               "• 99211 — 1–9 min &nbsp; ($24)<br>"
               "• 99212 — 10–19 min ($55)<br>"
               "• 99213 — 20–29 min ($92)<br>"
               "• 99214 — 30–39 min ($136)<br>"
               "• 99215 — 40+ min &nbsp; ($193)<br><br>"
               "When a 40-min visit is billed as 99213, the $101 difference goes uncollected.")

    em_codes = ["99211","99212","99213","99214","99215"]
    em_time  = ["1–9 min","10–19 min","20–29 min","30–39 min","40+ min"]
    pc_em    = pc_f.copy()

    def exp(m):
        if pd.isna(m): return None
        m = int(m)
        if m<=9:  return "99211"
        if m<=19: return "99212"
        if m<=29: return "99213"
        if m<=39: return "99214"
        return "99215"

    pc_em["Exp"] = pc_em["Visit_Duration_Min"].apply(exp)
    em_rate = {"99211":24,"99212":55,"99213":92,"99214":136,"99215":193}
    rows = []
    for code, time_label in zip(em_codes, em_time):
        bucket = pc_em[pc_em["Exp"] == code]
        if len(bucket) == 0: continue
        em_idx = {c:i for i,c in enumerate(em_codes)}
        correct = under = over = under_gap = 0
        for _, r in bucket.iterrows():
            s = r["CPT_Code_Submitted"]; e = r["Exp"]
            if s not in em_idx or e not in em_idx:
                correct += 1; continue
            si, ei = em_idx[s], em_idx[e]
            if si == ei:   correct += 1
            elif si < ei:  under += 1; under_gap += em_rate.get(e,0)-em_rate.get(s,0)
            else:          over += 1
        rows.append({
            "Time Range": time_label, "Correct code": code,
            "Correctly billed": correct,
            "Billed too low (undercoded)": under,
            "Billed too high (overcoded)": over,
            "Revenue gap ($)": under_gap,
        })

    stacked = pd.DataFrame(rows)
    if stacked.empty:
        st.info("No Primary Care E&M visits match the current location / payer filters.")
    else:
        x_labels = [f"{r['Time Range']} ({r['Correct code']})" for _, r in stacked.iterrows()]
        fig_cpt = go.Figure()
        fig_cpt.add_trace(go.Bar(
            name="Correctly billed", x=x_labels, y=stacked["Correctly billed"],
            marker_color=GREEN, marker_opacity=0.85,
            text=stacked["Correctly billed"],
            textposition="inside", textfont=dict(size=11, color="#fff"),
            hovertemplate="<b>%{x}</b><br>Correctly billed: <b>%{y}</b> visits<extra></extra>",
        ))
        fig_cpt.add_trace(go.Bar(
            name="Billed too low", x=x_labels, y=stacked["Billed too low (undercoded)"],
            marker_color=RED, marker_opacity=0.85,
            text=stacked["Billed too low (undercoded)"],
            textposition="inside", textfont=dict(size=11, color="#fff"),
            customdata=stacked["Revenue gap ($)"],
            hovertemplate="<b>%{x}</b><br>Billed too low: <b>%{y}</b> visits<br>Revenue lost: <b>$%{customdata:,.0f}</b><extra></extra>",
        ))
        fig_cpt.add_trace(go.Bar(
            name="Billed too high", x=x_labels, y=stacked["Billed too high (overcoded)"],
            marker_color=AMBER, marker_opacity=0.85,
            text=stacked["Billed too high (overcoded)"].apply(lambda v: v if v > 0 else ""),
            textposition="inside", textfont=dict(size=11, color="#fff"),
            hovertemplate="<b>%{x}</b><br>Billed too high: <b>%{y}</b> visits<extra></extra>",
        ))
        fig_cpt.update_layout(
            barmode="stack", height=400,
            xaxis=dict(title="Visit duration bucket", tickfont=dict(size=12), **GR),
            yaxis=dict(title="Number of visits", **GR),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=12), traceorder="reversed"),
            bargap=0.3, **PC
        )
        st.plotly_chart(fig_cpt, use_container_width=True)
        insight("Each bar = all visits in that time bucket. Green = billed correctly. "
                "Red = billed too low (revenue lost). Amber = billed too high (audit risk). "
                "Hover any segment to see visit count and revenue impact.")

    st.divider()
    col1, col2 = st.columns(2)

    # compute filter-scoped gap breakdown
    with col1:
        whatis("Where is the money going?",
               "The gap comes from two sources: visits billed at the wrong level, "
               "and billing codes that qualify for extra reimbursement but are never submitted.")
        if (em_gap + total_addon) > 0:
            fig_d = go.Figure(go.Pie(
                values=[em_gap, total_addon],
                labels=["Billed too low", "Missing codes"],
                hole=0.62,
                marker=dict(colors=[RED, AMBER], line=dict(color=BG, width=2)),
                textinfo="percent", textfont=dict(size=12, color="#ffffff"),
                hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
                pull=[0.03, 0.03],
            ))
            fig_d.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.05, font=dict(size=11), itemsizing="constant"),
                height=260, **make_plot_cfg(),
            )
            st.plotly_chart(fig_d, use_container_width=True)
        else:
            st.info("No revenue gap data for current filters.")
        insight("Missing billing codes (amber) are often the bigger problem — "
                "these are legitimate charges that qualify but are simply never submitted.")

    with col2:
        whatis("Which service line sees the most visits?",
               "Your organization provides care across three service lines. "
               "Billing issues exist across all three — this tool covers each one.")
        sl = df_f["Service_Line"].value_counts().reset_index()
        sl.columns = ["Service Line","Visits"]
        fig_sl = go.Figure(go.Pie(
            values=sl["Visits"].tolist(), labels=sl["Service Line"].tolist(),
            hole=0.62,
            marker=dict(colors=[BLUE, "#5ac8fa", GREEN], line=dict(color=BG, width=2)),
            textinfo="percent", textfont=dict(size=12, color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>%{value} visits (%{percent})<extra></extra>",
            pull=[0.03]*len(sl),
        ))
        fig_sl.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="top", y=-0.05, font=dict(size=11), itemsizing="constant"),
            height=260, **make_plot_cfg(),
        )
        st.plotly_chart(fig_sl, use_container_width=True)
        insight("Behavioral Health and Psychiatry together make up more than half of all "
                "visits — yet most billing audits only look at primary care.")

    st.divider()
    whatis("If nothing changes, how much is at stake?",
           "Slide to your actual monthly visit volume to see how the gap compounds annually.")
    monthly  = st.slider("Monthly visits across all locations", 100, 3000, 500, step=50)
    base_vis = max(total_visits, 1)
    p_em     = monthly * (em_gap / base_vis) * 12
    p_addon  = monthly * (total_addon / base_vis) * 12
    p1,p2,p3 = st.columns(3)
    p1.metric("Annual gap — billing level",  f"${p_em:,.0f}")
    p2.metric("Annual gap — missing codes",  f"${p_addon:,.0f}")
    p3.metric("Total projected annual gap",  f"${p_em+p_addon:,.0f}", f"At {monthly:,} visits/month")

# ══════════════════════════════════════════════════════════════
# PAGE 2 — PROVIDER INSIGHTS
# ══════════════════════════════════════════════════════════════
elif page == "Provider Insights":
    st.title("Provider Insights")
    prob_card(
        "Billing gaps are not random — they follow provider-specific patterns.",
        "This page shows which providers have the highest rate of visits billed below "
        "what the visit length supports. The goal is not to evaluate clinical performance — "
        "it is to identify who would benefit most from a billing education session. "
        "Every provider's patients deserve to have the full value of their visit captured."
    )

    prov = pc_f.groupby("Provider_Name").agg(
        Visits=("Visit_ID","count"),
        Undercoded=("Coding_Flag",lambda x:(x=="UNDERCODED").sum()),
        Revenue_Gap=("Revenue_Gap","sum"),
        Avg_Duration=("Visit_Duration_Min","mean"),
    ).reset_index()
    prov["Rate_%"] = (prov["Undercoded"]/prov["Visits"]*100).round(1)
    prov["Status"] = prov["Rate_%"].apply(
        lambda r: "Needs attention" if r>40 else ("Moderate" if r>20 else "Good"))

    sort_by = st.selectbox("Sort by",
        ["Estimated gap ($)","Billing error rate (%)","Total visits"])
    sort_map = {"Estimated gap ($)":"Revenue_Gap",
                "Billing error rate (%)":"Rate_%","Total visits":"Visits"}
    prov = prov.sort_values(sort_map[sort_by], ascending=False)

    whatis("Which providers have the largest billing gap?",
           "Each bar shows the estimated dollar gap between what was billed "
           "and what should have been billed based on visit length.")

    bar_colors = prov["Rate_%"].apply(
        lambda r: RED if r>40 else (AMBER if r>20 else GREEN)).tolist()
    PC = make_plot_cfg(); GR = make_grid()

    fig_bar = go.Figure(go.Bar(
        x=prov["Provider_Name"], y=prov["Revenue_Gap"],
        marker_color=bar_colors, marker_opacity=0.88,
        text=prov["Revenue_Gap"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside", textfont=dict(size=12, color=FONT_C),
        customdata=prov[["Rate_%","Visits","Avg_Duration"]],
        hovertemplate=(
            "<b>%{x}</b><br>Est. gap: $%{y:,.0f}<br>"
            "Error rate: %{customdata[0]:.1f}%<br>"
            "Visits: %{customdata[1]}<br>"
            "Avg visit: %{customdata[2]:.0f} min<extra></extra>"
        ),
    ))
    fig_bar.update_layout(
        height=380,
        xaxis=dict(tickangle=-15, **GR),
        yaxis=dict(title="Estimated billing gap ($)", tickprefix="$", tickformat=",", **GR),
        **PC
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    best = prov.loc[prov["Rate_%"].idxmin(), "Provider_Name"]
    insight(f"{best} has the lowest billing error rate — use their documentation "
            f"patterns as the benchmark for provider education sessions.")

    whatis("Provider scorecard",
           "Billing error rate = percentage of visits where the submitted code "
           "was lower than the visit length supports. Above 40% is a consistent "
           "pattern that billing education can fix.")
    display = prov[["Provider_Name","Visits","Undercoded",
                     "Rate_%","Revenue_Gap","Avg_Duration","Status"]].copy()
    display["Revenue_Gap"]  = display["Revenue_Gap"].apply(lambda x: f"${x:,.0f}")
    display["Avg_Duration"] = display["Avg_Duration"].apply(lambda x: f"{x:.0f} min")
    display["Rate_%"]       = display["Rate_%"].apply(lambda x: f"{x}%")
    display.columns = ["Provider","Visits","Billed too low",
                       "Error rate","Est. gap","Avg visit","Status"]
    st.dataframe(display, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# PAGE 3 — AI ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "AI Analysis":
    st.title("AI Analysis")
    prob_card(
        "Beyond visit length — AI reads what the provider actually documented.",
        "Visit length alone does not tell the full story. A 28-minute visit where the "
        "provider managed three chronic conditions, ordered labs, adjusted medications, "
        "and placed a specialist referral is clinically different from a routine 28-minute "
        "check-in — even though both are the same length.<br><br>"
        "ClarityCode uses AI to read the clinical notes and identify cases where the "
        "documented complexity of care justifies a higher billing code than what was submitted."
    )

    ai_file  = "outputs/step5_soap_ai_results.xlsx"
    nlp_file = "outputs/step6_nlp_mdm_results.xlsx"
    ai_ok    = os.path.exists(ai_file)
    nlp_ok   = os.path.exists(nlp_file)

    if not ai_ok and not nlp_ok:
        st.info("Run `step5_ai_soap_analyzer.py` and `step6_nlp_mdm_extractor.py` "
                "to enable AI analysis.")
        st.code("python step5_ai_soap_analyzer.py\npython step6_nlp_mdm_extractor.py")
    else:
        tabs = st.tabs(["AI note review","Clinical complexity scores","Strongest findings"])

        with tabs[0]:
            if ai_ok:
                ai = pd.read_excel(ai_file, sheet_name="All_AI_Results")
                under_ai = (ai["Coding_Flag"]=="UNDERCODED").sum()
                corr_ai  = (ai["Coding_Flag"]=="CORRECT").sum()
                over_ai  = (ai["Coding_Flag"]=="OVERCODED").sum()
                gap_ai   = ai["Revenue_Gap_$"].sum() if "Revenue_Gap_$" in ai.columns else 0

                a1,a2,a3,a4 = st.columns(4)
                a1.metric("Visits billed too low", str(under_ai), f"{under_ai/len(ai)*100:.0f}% of reviewed visits")
                a2.metric("Correctly billed",      str(corr_ai),  f"{corr_ai/len(ai)*100:.0f}% of reviewed visits")
                a3.metric("Billed too high ⚠️",    str(over_ai),  "May trigger audit")
                a4.metric("AI-identified gap",     f"${gap_ai:,.0f}", "From note analysis")

                if over_ai > 0:
                    st.error(f"⚠️  {over_ai} visits were billed at a level the clinical notes "
                             f"do not fully support. Review before next billing cycle.")

                whatis("What did the AI find in each visit note?",
                       "The AI read each provider's clinical note and determined the appropriate "
                       "billing code based on what was documented — problems addressed, tests reviewed, "
                       "medications changed, and referrals placed.")

                PC = make_plot_cfg(); GR = make_grid()
                fc = ai["Coding_Flag"].value_counts().reset_index()
                fc.columns = ["Finding","Visits"]
                cmap = {"UNDERCODED":RED,"CORRECT":GREEN,"OVERCODED":AMBER,"Non-EM":MUTED,"—":MUTED}
                fig_fc = px.bar(fc, x="Finding", y="Visits", color="Finding",
                                color_discrete_map=cmap, text="Visits")
                fig_fc.update_traces(textposition="outside", marker_opacity=0.88)
                fig_fc.update_layout(showlegend=False, height=300,
                                     xaxis=dict(**GR), yaxis=dict(**GR), **PC)
                st.plotly_chart(fig_fc, use_container_width=True)
                insight("'Billed too high' findings are just as important as 'billed too low' "
                        "— they represent compliance risk, not just missed revenue.")

                whatis("Visit-by-visit AI findings",
                       "The 'AI explanation' column shows exactly why a different billing code "
                       "was recommended — written the way a certified billing specialist would.")
                ff = st.selectbox("Show me", ["All findings","Billed too low",
                                              "Correctly billed","Billed too high"])
                fmap = {"All findings":None,"Billed too low":"UNDERCODED",
                        "Correctly billed":"CORRECT","Billed too high":"OVERCODED"}
                fai  = ai if fmap[ff] is None else ai[ai["Coding_Flag"]==fmap[ff]]
                show = [c for c in ["Visit_ID","Provider_Name","Visit_Type",
                        "CPT_Submitted","CPT_Recommended_AI","Coding_Flag",
                        "Revenue_Gap_$","AI_Reasoning"] if c in fai.columns]
                st.dataframe(fai[show].rename(columns={
                    "CPT_Submitted":"Code submitted","CPT_Recommended_AI":"AI recommendation",
                    "Coding_Flag":"Finding","Revenue_Gap_$":"Gap ($)","AI_Reasoning":"Why it was flagged"
                }).head(25), use_container_width=True, hide_index=True, height=400)
            else:
                st.info("Run `step5_ai_soap_analyzer.py` to enable this tab.")

        with tabs[1]:
            if nlp_ok:
                nlp = pd.read_excel(nlp_file, sheet_name="NLP_Results")
                whatis("How complex were visits — by type?",
                       "ClarityCode scores each visit note 0–100 based on six clinical signals: "
                       "problems addressed, tests reviewed, medications changed, referrals made, "
                       "patient education documented, and time recorded. A score above 70 typically "
                       "warrants a higher billing code.")
                if "MDM_Score_0_100" in nlp.columns:
                    PC = make_plot_cfg(); GR = make_grid()
                    avg = nlp.groupby("Visit_Type")["MDM_Score_0_100"].mean().round(1).sort_values().reset_index()
                    avg.columns = ["Visit type","Avg complexity score"]
                    fig_nlp = px.bar(avg, x="Avg complexity score", y="Visit type",
                                     orientation="h", color="Avg complexity score",
                                     color_continuous_scale=[GREEN, AMBER, RED],
                                     text="Avg complexity score")
                    fig_nlp.update_traces(textposition="outside", marker_opacity=0.88)
                    fig_nlp.update_layout(height=400, showlegend=False, coloraxis_showscale=False,
                                          xaxis=dict(range=[0,110], **GR), yaxis=dict(**GR), **PC)
                    st.plotly_chart(fig_nlp, use_container_width=True)
                    insight("High-scoring visit types billed at a low code level = the clearest "
                            "evidence of a documentation-to-billing disconnect.")

                sig = [c for c in ["Visit_ID","Provider_Name","Problems_Count","Labs_Count",
                       "Referrals_Count","Med_Changes_Count","Time_Documented_Min",
                       "MDM_Score_0_100","CPT_Submitted","CPT_Recommended_NLP"] if c in nlp.columns]
                st.dataframe(nlp[sig].rename(columns={
                    "Problems_Count":"Problems addressed","Labs_Count":"Tests reviewed",
                    "Referrals_Count":"Referrals made","Med_Changes_Count":"Medication changes",
                    "Time_Documented_Min":"Time (min)","MDM_Score_0_100":"Complexity score (0–100)",
                    "CPT_Submitted":"Code submitted","CPT_Recommended_NLP":"Recommended code",
                }), use_container_width=True, hide_index=True)
            else:
                st.info("Run `step6_nlp_mdm_extractor.py` to enable this tab.")

        with tabs[2]:
            whatis("Visits flagged by both AI and clinical scoring",
                   "When two independent methods both flag the same visit as billed too low, "
                   "that is the strongest possible evidence — nearly impossible to dispute "
                   "in a billing review or provider coaching session.")
            if ai_ok and nlp_ok:
                ai2  = pd.read_excel(ai_file,  sheet_name="All_AI_Results")
                nlp2 = pd.read_excel(nlp_file, sheet_name="NLP_Results")
                ai_u  = set(ai2[ai2["Coding_Flag"]=="UNDERCODED"]["Visit_ID"].astype(str))
                nlp_u = set(nlp2[nlp2["Coding_Flag"]=="UNDERCODED"]["Visit_ID"].astype(str)) \
                        if "Coding_Flag" in nlp2.columns else set()
                both  = ai_u & nlp_u
                b1,b2,b3 = st.columns(3)
                b1.metric("AI method only",  len(ai_u-nlp_u), "Single source")
                b2.metric("Scoring only",    len(nlp_u-ai_u), "Single source")
                b3.metric("Both methods ✓",  len(both),       "Highest confidence")
                if both:
                    bdf  = ai2[ai2["Visit_ID"].astype(str).isin(both)]
                    show = [c for c in ["Visit_ID","Provider_Name","Visit_Type",
                            "CPT_Submitted","CPT_Recommended_AI",
                            "Revenue_Gap_$","AI_Reasoning"] if c in bdf.columns]
                    st.dataframe(bdf[show].rename(columns={
                        "CPT_Submitted":"Code submitted","CPT_Recommended_AI":"AI recommendation",
                        "Revenue_Gap_$":"Gap ($)","AI_Reasoning":"Why it was flagged"
                    }), use_container_width=True, hide_index=True)
                    st.success(f"These {len(both)} visits should be prioritized for "
                               f"clinical coder review — both methods agree.")
            else:
                st.info("Run both analysis scripts to unlock this view.")

# ══════════════════════════════════════════════════════════════
# PAGE 4 — MISSING BILLING CODES
# ══════════════════════════════════════════════════════════════
elif page == "Missing Billing Codes":
    st.title("Missing Billing Codes")
    prob_card(
        "Some billing codes are never submitted — even when visits clearly qualify.",
        "Beyond the main visit billing code, certain types of care qualify for "
        "additional reimbursement. These codes are separate billing entries that "
        "attach to the primary visit. Most providers are unaware they exist — "
        "which means qualifying patients are seen, the care is delivered, "
        "but the additional reimbursement is never claimed."
    )

    ccm = pc_f["CCM_Missing"].sum()
    bhi = pc_f["BHI_Missing"].sum()
    g22 = pc_f["G2211_Missing"].sum()
    p90 = psych_f["90833_Missing"].sum()

    a1,a2,a3,a4 = st.columns(4)
    a1.metric("Chronic Care Management",      f"${ccm*62:,.0f}", f"99490 · {ccm} qualifying visits")
    a2.metric("Behavioral Health Integration",f"${bhi*45:,.0f}", f"99484 · {bhi} qualifying visits")
    a3.metric("Complex Care Add-on",          f"${g22*16:,.0f}", f"G2211 · {g22} qualifying visits")
    a4.metric("Therapy Session Add-on",       f"${p90*65:,.0f}", f"90833 · {p90} qualifying visits")

    st.divider()
    whatis("Which missing codes have the biggest impact?",
           "Each of these codes represents care that was delivered but not billed. "
           "They are not duplicate charges — they are separate billable services "
           "with their own reimbursement rates.")

    add_df = pd.DataFrame({
        "Billing code": [
            "Chronic Care Management (99490)",
            "Therapy Session Add-on (90833)",
            "Complex Care Add-on (G2211)",
            "Behavioral Health Integration (99484)",
        ],
        "Qualifying visits": [ccm, p90, g22, bhi],
        "Uncollected ($)":   [ccm*62, p90*65, g22*16, bhi*45],
    }).sort_values("Uncollected ($)", ascending=True)

    PC = make_plot_cfg(); GR = make_grid()
    fig_add = go.Figure(go.Bar(
        x=add_df["Uncollected ($)"], y=add_df["Billing code"],
        orientation="h",
        marker_color=[GREEN, AMBER, AMBER, RED],
        marker_opacity=0.88,
        text=add_df["Uncollected ($)"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside", textfont=dict(size=12, color=FONT_C),
    ))
    fig_add.update_layout(height=300,
                          xaxis=dict(tickprefix="$", tickformat=",", **GR),
                          yaxis=dict(**GR), **PC)
    st.plotly_chart(fig_add, use_container_width=True)
    insight("Chronic Care Management is the biggest opportunity — and unlike a one-time "
            "billing fix, it generates new revenue every single month for every qualifying patient.")

    whatis("Monthly recurring revenue calculator",
           "Chronic Care Management (99490) pays $62 per patient per month for care "
           "coordination of patients with two or more chronic conditions. "
           "If your team is already coordinating this care but not documenting it, "
           "this is a training fix — not extra clinical work.")
    qualifying = st.slider("Patients qualifying for monthly billing", 10, 500, int(ccm), step=1)
    m1,m2,m3 = st.columns(3)
    m1.metric("Monthly additional revenue", f"${qualifying*62:,.0f}")
    m2.metric("Annual additional revenue",  f"${qualifying*62*12:,.0f}")
    m3.metric("3-year revenue potential",   f"${qualifying*62*36:,.0f}")
    st.warning("To bill for Chronic Care Management, 20 minutes of care coordination "
               "must be documented in the patient chart each month. "
               "This is a documentation habit — not extra clinical work.")

# ══════════════════════════════════════════════════════════════
# PAGE 5 — REVIEW QUEUE
# ══════════════════════════════════════════════════════════════
elif page == "Review Queue":
    st.title("Billing Review Queue")
    prob_card(
        "Every visit that needs a second look — in one place.",
        "This queue shows every visit where the submitted billing code may not match "
        "what the visit documentation supports. Use the filters to focus on specific "
        "providers or issue types. Download the list and work through it with your "
        "billing team. Every visit here requires human review before any changes are made — "
        "ClarityCode identifies, your team decides."
    )

    flagged_em = pc_f[pc_f["Coding_Flag"]=="UNDERCODED"][[
        "Visit_ID","Visit_Date","Location","Provider_Name","Visit_Type",
        "CPT_Code_Submitted","Expected_CPT","Visit_Duration_Min",
        "Primary_Diagnosis","Payer","Revenue_Gap"
    ]].copy()
    flagged_em.rename(columns={"Expected_CPT":"Recommended","Revenue_Gap":"Gap_$"}, inplace=True)
    flagged_em["Issue"] = "Billed too low"

    flagged_ccm = pc_f[pc_f["CCM_Missing"]][[
        "Visit_ID","Visit_Date","Location","Provider_Name","Visit_Type",
        "CPT_Code_Submitted","Visit_Duration_Min","Primary_Diagnosis","Payer"
    ]].copy()
    flagged_ccm["Recommended"] = "Add code 99490"
    flagged_ccm["Issue"]       = "Missing monthly billing code"
    flagged_ccm["Gap_$"]       = 62

    flagged_psych = psych_f[psych_f["90833_Missing"]][[
        "Visit_ID","Visit_Date","Location","Provider_Name","Visit_Type",
        "CPT_Code_Submitted","Visit_Duration_Min","Primary_Diagnosis","Payer"
    ]].copy()
    flagged_psych["Recommended"] = "Add code 90833"
    flagged_psych["Issue"]       = "Missing therapy add-on code"
    flagged_psych["Gap_$"]       = 65

    all_flagged = pd.concat([flagged_em, flagged_ccm, flagged_psych],
                            ignore_index=True).sort_values("Gap_$", ascending=False)

    f1,f2,f3 = st.columns(3)
    with f1:
        issue_f = st.selectbox("Issue type", ["All issues","Billed too low",
            "Missing monthly billing code","Missing therapy add-on code"])
    with f2:
        prov_f = st.selectbox("Provider",
            ["All providers"]+sorted(all_flagged["Provider_Name"].unique().tolist()))
    with f3:
        min_gap = st.slider("Minimum gap ($)", 0, 200, 0, step=10)

    filt = all_flagged.copy()
    if issue_f != "All issues":    filt = filt[filt["Issue"]==issue_f]
    if prov_f  != "All providers": filt = filt[filt["Provider_Name"]==prov_f]
    filt = filt[filt["Gap_$"] >= min_gap]

    st.markdown(f"**{len(filt):,} visits** flagged for review · "
                f"Total estimated gap: **${filt['Gap_$'].sum():,.0f}**")

    display = filt[[
        "Visit_ID","Visit_Date","Provider_Name","Location","Visit_Type",
        "CPT_Code_Submitted","Recommended","Visit_Duration_Min","Gap_$","Issue","Payer"
    ]].copy()
    display["Visit_Date"] = pd.to_datetime(display["Visit_Date"]).dt.strftime("%b %d, %Y")
    display["Gap_$"]      = display["Gap_$"].apply(lambda x: f"${x:,.0f}")
    display.columns = ["Visit ID","Date","Provider","Location","Visit type",
                       "Code submitted","Recommended","Duration (min)",
                       "Est. gap","Issue","Insurance"]
    st.dataframe(display, use_container_width=True, hide_index=True, height=480)
    csv = filt.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️  Download review list as CSV", data=csv,
                       file_name="billing_review_queue.csv", mime="text/csv")

