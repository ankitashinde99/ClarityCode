import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="ClarityCode",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── APPLE-INSPIRED CSS ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "Helvetica Neue", sans-serif !important;
    letter-spacing: -0.01em;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem !important; max-width: 1200px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(250,250,252,0.95) !important;
    border-right: 1px solid rgba(0,0,0,0.06) !important;
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * { color: #1d1d1f !important; }

/* Metric cards — Apple card style */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 16px;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s ease;
}
[data-testid="metric-container"]:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.06);
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: #86868b !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: #1d1d1f !important;
    letter-spacing: -0.04em;
}
[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

/* Headings */
h1 { font-size: 2.2rem !important; font-weight: 600 !important;
     color: #1d1d1f !important; letter-spacing: -0.04em !important; }
h2 { font-size: 1.4rem !important; font-weight: 600 !important;
     color: #1d1d1f !important; letter-spacing: -0.02em !important; margin-top: 1.5rem !important; }
h3 { font-size: 1.1rem !important; font-weight: 500 !important;
     color: #1d1d1f !important; }

/* Selectbox & slider */
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    background: #ffffff !important;
}
.stSlider > div > div > div > div {
    background: #0071e3 !important;
}

/* Divider */
hr { border: none; border-top: 1px solid rgba(0,0,0,0.06) !important; margin: 1.5rem 0 !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden;
    border: 1px solid rgba(0,0,0,0.06) !important; }

/* Expander */
[data-testid="stExpander"] { border-radius: 12px !important;
    border: 1px solid rgba(0,0,0,0.06) !important; background: #fafafa !important; }

/* Alert boxes */
[data-testid="stAlert"] { border-radius: 12px !important; border: none !important; }

/* Caption */
.stCaption { color: #86868b !important; font-size: 0.82rem !important; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* Problem statement card */
.problem-card {
    background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 100%);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 20px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.5rem;
}
.problem-headline {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1d1d1f;
    letter-spacing: -0.03em;
    line-height: 1.3;
    margin-bottom: 0.8rem;
}
.problem-body {
    font-size: 1rem;
    color: #6e6e73;
    line-height: 1.7;
    max-width: 780px;
}
.story-pill {
    display: inline-block;
    background: rgba(0,113,227,0.08);
    color: #0071e3;
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-size: 0.78rem;
    font-weight: 500;
    margin-top: 1rem;
    letter-spacing: 0.02em;
}
.chart-card {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 16px;
    padding: 1.4rem 1.6rem 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}
.chart-title {
    font-size: 1rem;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 0.25rem;
}
.chart-subtitle {
    font-size: 0.82rem;
    color: #86868b;
    margin-bottom: 1rem;
}
.insight-bar {
    background: rgba(0,113,227,0.06);
    border-left: 3px solid #0071e3;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #1d1d1f;
    margin-top: 0.75rem;
    line-height: 1.5;
}
.help-pill {
    display: inline-block;
    background: #f5f5f7;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    color: #6e6e73;
    margin-bottom: 0.5rem;
    border: 1px solid rgba(0,0,0,0.06);
}
.nav-label {
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #86868b;
    margin: 1rem 0 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────
@st.cache_data(ttl=0)
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
        m=int(m)
        if m<=9:  return "99211"
        if m<=19: return "99212"
        if m<=29: return "99213"
        if m<=39: return "99214"
        return "99215"

    def flag(row):
        s,e = row["CPT_Code_Submitted"], row["Expected_CPT"]
        if s not in EM_ORDER: return "Non E&M"
        if e not in EM_ORDER: return "Unknown"
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
    st.markdown("<div class='nav-label'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio("", [
        "Overview",
        "Provider Insights",
        "AI Analysis",
        "Missing Billing Codes",
        "Review Queue",
        "How It Works",
    ], label_visibility="collapsed")

    st.markdown("<div class='nav-label'>Filters</div>", unsafe_allow_html=True)
    locations = ["All locations"] + sorted(df["Location"].unique().tolist())
    sel_loc   = st.selectbox("Clinic location", locations, label_visibility="collapsed")
    svc_lines = ["All service lines"] + sorted(df["Service_Line"].unique().tolist())
    sel_svc   = st.selectbox("Service line", svc_lines, label_visibility="collapsed")
    payers    = ["All payers"] + sorted(df["Payer"].dropna().unique().tolist())
    sel_payer = st.selectbox("Insurance", payers, label_visibility="collapsed")

    st.markdown("---")
    st.caption("ClarityCode v2.0 · Synthetic data only")

def apply_f(data):
    d = data.copy()
    if sel_loc   != "All locations":    d = d[d["Location"]==sel_loc]
    if sel_svc   != "All service lines":d = d[d["Service_Line"]==sel_svc]
    if sel_payer != "All payers":       d = d[d["Payer"]==sel_payer]
    return d

df_f = apply_f(df); pc_f = apply_f(pc); psych_f = apply_f(psych)

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

# Apple plot defaults
PLOT_CFG = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="-apple-system, BlinkMacSystemFont, 'Helvetica Neue'", color="#1d1d1f"),
    margin=dict(t=20,b=20,l=0,r=0),
)
GRID = dict(gridcolor="rgba(0,0,0,0.05)", zerolinecolor="rgba(0,0,0,0.08)")
BLUE  = "#0071e3"; RED = "#ff3b30"; GREEN = "#34c759"; AMBER = "#ff9500"; GRAY="#86868b"

def card(title, subtitle, content_fn):
    st.markdown(f"""
    <div class='chart-card'>
      <div class='chart-title'>{title}</div>
      <div class='chart-subtitle'>{subtitle}</div>
    </div>""", unsafe_allow_html=True)
    content_fn()

def insight(text):
    st.markdown(f"<div class='insight-bar'>💡 {text}</div>", unsafe_allow_html=True)

def whatis(text):
    st.markdown(f"<div class='help-pill'>ⓘ {text}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "Overview":

    # Problem statement
    st.markdown("""
    <div class='problem-card'>
      <div class='problem-headline'>Your organization may be losing thousands of dollars<br>every month — without knowing it.</div>
      <div class='problem-body'>
        When providers see patients, they submit billing codes to describe the visit.
        If those codes are too low — or qualifying codes are missed entirely —
        insurance pays less than what the visit was worth.
        This happens silently, visit after visit, across every clinic location.
        <br><br>
        <strong>ClarityCode</strong> analyzes your clinical visit data and surfaces exactly where
        billing does not match the care that was delivered — so your team can act on it.
      </div>
      <span class='story-pill'>Analysis based on CMS 2021 clinical billing guidelines</span>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Estimated revenue gap", f"${total_gap:,.0f}",
              "Billing + missing codes combined")
    c2.metric("Visits billed too low",  f"{undercode_rate:.1f}%",
              f"{undercoded} of {len(pc_f)} primary care visits")
    c3.metric("Unclaimed billing codes",f"${total_addon:,.0f}",
              "Codes never submitted")
    c4.metric("Total visits reviewed",  f"{total_visits:,}",
              "Across all service lines")

    st.divider()

    # CPT story chart
    st.markdown("#### Where is the billing problem happening?")
    whatis("Billing codes (called CPT codes) describe how complex a visit was. "
           "Code 99213 is for a 20–29 minute visit. 99215 is for a 40+ minute visit. "
           "When a 45-minute visit gets billed as a 20-minute visit, the difference "
           "in payment goes uncollected.")

    em_codes  = ["99211","99212","99213","99214","99215"]
    em_labels = ["99211\n1–9 min","99212\n10–19 min","99213\n20–29 min",
                 "99214\n30–39 min","99215\n40+ min"]
    EM_RATE   = {"99211":24,"99212":55,"99213":92,"99214":136,"99215":193}

    pc_em = df_f[df_f["Service_Line"]=="Primary Care"].copy()
    submitted = pc_em["CPT_Code_Submitted"].value_counts().reindex(em_codes, fill_value=0)

    def exp(m):
        if pd.isna(m): return None
        m=int(m)
        if m<=9:  return "99211"
        if m<=19: return "99212"
        if m<=29: return "99213"
        if m<=39: return "99214"
        return "99215"

    pc_em["Exp"] = pc_em["Visit_Duration_Min"].apply(exp)
    expected = pc_em["Exp"].value_counts().reindex(em_codes, fill_value=0)

    fig_cpt = go.Figure()
    fig_cpt.add_trace(go.Bar(
        name="What was billed", x=em_labels, y=submitted.values,
        marker_color=BLUE, marker_opacity=0.85,
        text=submitted.values, textposition="outside",
        textfont=dict(size=12, color="#1d1d1f"),
    ))
    fig_cpt.add_trace(go.Bar(
        name="What should have been billed", x=em_labels, y=expected.values,
        marker_color=GREEN, marker_opacity=0.65,
        text=expected.values, textposition="outside",
        textfont=dict(size=12, color="#1d1d1f"),
    ))
    fig_cpt.update_layout(
        barmode="group", height=360,
        xaxis=dict(title="", tickfont=dict(size=11), **GRID),
        yaxis=dict(title="Number of visits", **GRID),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    font=dict(size=12)),
        bargap=0.25, bargroupgap=0.08,
        **PLOT_CFG
    )
    st.plotly_chart(fig_cpt, use_container_width=True)
    insight("The blue bars show what providers billed. The green bars show what "
            "billing should have been based on visit length. Where blue is taller "
            "than green — that code is overused. Where green is taller than blue "
            "— money is being left uncollected.")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Where is the money going?")
        whatis("The gap comes from two sources: visits billed at the wrong level, "
               "and billing codes that qualify for extra reimbursement but are "
               "never submitted at all.")
        fig_donut = px.pie(
            values=[em_gap, total_addon],
            names=["Visits billed too low","Billing codes never submitted"],
            color_discrete_sequence=[RED, AMBER], hole=0.6,
        )
        fig_donut.update_traces(
            textinfo="label+percent",
            textfont=dict(size=12),
            pull=[0.02, 0.02],
        )
        fig_donut.update_layout(
            showlegend=False, height=280, **PLOT_CFG,
            margin=dict(t=10,b=10,l=10,r=10)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        insight("Missing billing codes (amber) are often the bigger problem — "
                "these are legitimate charges that qualify but are simply never submitted.")

    with col2:
        st.markdown("#### Which service line sees the most visits?")
        whatis("Your organization provides care across three service lines. "
               "Billing issues exist in all three — this tool covers each one.")
        sl = df_f["Service_Line"].value_counts().reset_index()
        sl.columns = ["Service Line","Visits"]
        fig_sl = px.pie(sl, values="Visits", names="Service Line",
                        color_discrete_sequence=[BLUE,"#5ac8fa","#34c759"],
                        hole=0.6)
        fig_sl.update_traces(textinfo="label+value", textfont=dict(size=12))
        fig_sl.update_layout(showlegend=False, height=280, **PLOT_CFG,
                              margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_sl, use_container_width=True)
        insight("Behavioral Health and Psychiatry together make up more than half "
                "of all visits — yet most billing audits only look at primary care.")

    st.divider()
    st.markdown("#### If nothing changes, how much is at stake?")
    whatis("Slide to your actual monthly visit volume across all locations "
           "to see how the gap compounds over a full year.")
    monthly = st.slider("Monthly visits across all clinic locations",
                        100, 3000, 500, step=50)
    p_em    = monthly * 0.304 * 50 * 12
    p_addon = monthly * (total_addon/max(total_visits,1)) * 12
    p1,p2,p3 = st.columns(3)
    p1.metric("Annual gap — billing level",   f"${p_em:,.0f}")
    p2.metric("Annual gap — missing codes",   f"${p_addon:,.0f}")
    p3.metric("Total projected annual gap",   f"${p_em+p_addon:,.0f}",
              f"Based on {monthly:,} visits/month")

# ══════════════════════════════════════════════════════════════
# PAGE 2 — PROVIDER INSIGHTS
# ══════════════════════════════════════════════════════════════
elif page == "Provider Insights":
    st.title("Provider Insights")
    st.markdown("""
    <div class='problem-card'>
      <div class='problem-headline' style='font-size:1.1rem'>
        Billing gaps are not random — they follow provider-specific patterns.
      </div>
      <div class='problem-body' style='font-size:0.92rem'>
        This page shows which providers have the highest rate of visits billed
        below what the visit length supports. The goal is not to evaluate clinical
        performance — it is to identify who would benefit most from a billing
        education session. Every provider's patients deserve to have the full
        value of their visit captured.
      </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("#### Which providers have the largest billing gap?")
    whatis("Each bar shows the estimated dollar gap between what was billed and "
           "what should have been billed based on visit length. This is money "
           "the organization is entitled to collect but currently is not.")

    bar_colors = prov["Rate_%"].apply(
        lambda r: RED if r>40 else (AMBER if r>20 else GREEN)).tolist()

    fig_bar = go.Figure(go.Bar(
        x=prov["Provider_Name"],
        y=prov["Revenue_Gap"],
        marker_color=bar_colors,
        marker_opacity=0.88,
        text=prov.apply(lambda r: f"${r['Revenue_Gap']:,.0f}", axis=1),
        textposition="outside",
        textfont=dict(size=12, color="#1d1d1f"),
        customdata=prov[["Rate_%","Visits","Avg_Duration"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Estimated gap: $%{y:,.0f}<br>"
            "Billing error rate: %{customdata[0]:.1f}%<br>"
            "Total visits: %{customdata[1]}<br>"
            "Avg visit length: %{customdata[2]:.0f} min"
            "<extra></extra>"
        ),
    ))
    fig_bar.add_hline(y=0, line_color="rgba(0,0,0,0.1)", line_width=1)
    fig_bar.update_layout(
        height=380, xaxis=dict(tickangle=-15, **GRID),
        yaxis=dict(title="Estimated billing gap ($)",
                   tickprefix="$", tickformat=",", **GRID),
        **PLOT_CFG
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    best = prov.loc[prov["Rate_%"].idxmin(), "Provider_Name"]
    insight(f"{best} has the lowest billing error rate and serves as the "
            f"benchmark. In a coaching session, show other providers "
            f"specific visits where billing did not match visit length — "
            f"with real examples from their own charts.")

    st.markdown("#### Provider scorecard")
    whatis("Billing error rate = the percentage of primary care visits where "
           "the billed code was lower than the visit length supports. "
           "A rate above 40% is a consistent pattern that billing education can fix.")

    display = prov[["Provider_Name","Visits","Undercoded","Rate_%",
                     "Revenue_Gap","Avg_Duration","Status"]].copy()
    display["Revenue_Gap"]   = display["Revenue_Gap"].apply(lambda x: f"${x:,.0f}")
    display["Avg_Duration"]  = display["Avg_Duration"].apply(lambda x: f"{x:.0f} min")
    display["Rate_%"]        = display["Rate_%"].apply(lambda x: f"{x}%")
    display.columns = ["Provider","Visits","Billed too low",
                       "Error rate","Est. gap","Avg visit length","Status"]
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.markdown("#### How does visit length compare to what was billed?")
    whatis("Each dot is one visit. The horizontal position shows the billing "
           "code submitted. The vertical position shows how long the visit "
           "actually was. Dots above the shaded band for their code mean "
           "the visit was longer than what was billed.")

    pc_em2 = pc_f[pc_f["CPT_Code_Submitted"].isin(
        ["99211","99212","99213","99214","99215"])].copy()
    pc_em2["Coding_Flag2"] = pc_em2["Coding_Flag"].apply(
        lambda x: "Billed too low" if x=="UNDERCODED"
                  else ("Billed too high" if x=="OVERCODED" else "Correctly billed"))
    color_map = {"Billed too low":RED,"Correctly billed":GREEN,"Billed too high":AMBER}

    fig_sc = px.strip(pc_em2, x="CPT_Code_Submitted", y="Visit_Duration_Min",
                      color="Coding_Flag2", color_discrete_map=color_map,
                      hover_data=["Provider_Name","Visit_Type","Visit_Duration_Min"],
                      labels={"CPT_Code_Submitted":"Billing code submitted",
                              "Visit_Duration_Min":"Actual visit length (minutes)",
                              "Coding_Flag2":"Billing status"})
    # Add CMS threshold bands
    bands = [(0,9,"99211"),(10,19,"99212"),(20,29,"99213"),(30,39,"99214"),(40,54,"99215")]
    for lo,hi,code in bands:
        fig_sc.add_hrect(y0=lo, y1=hi, fillcolor="rgba(0,113,227,0.04)",
                         line_width=0, annotation_text=f"Correct range for {code}",
                         annotation_font_size=10, annotation_font_color=GRAY)
    fig_sc.update_layout(height=380, **PLOT_CFG,
                         xaxis=dict(**GRID), yaxis=dict(**GRID),
                         legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig_sc, use_container_width=True)
    insight("Red dots sitting above the shaded band for their code are the "
            "clearest evidence of underbilling — the visit was longer than "
            "what the billing code suggests.")

# ══════════════════════════════════════════════════════════════
# PAGE 3 — AI ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "AI Analysis":
    st.title("AI Analysis")
    st.markdown("""
    <div class='problem-card'>
      <div class='problem-headline' style='font-size:1.1rem'>
        Beyond visit length — AI reads what the provider actually documented.
      </div>
      <div class='problem-body' style='font-size:0.92rem'>
        Visit length alone does not tell the full story. A 28-minute visit where the
        provider managed three chronic conditions, ordered labs, adjusted medications,
        and placed a specialist referral is more complex than a 28-minute routine check.
        <br><br>
        ClarityCode uses Claude AI to read the clinical notes — the same notes a
        certified billing coder would review — and identify cases where the documented
        complexity of care justifies a higher billing code than what was submitted.
      </div>
    </div>
    """, unsafe_allow_html=True)

    import os
    ai_file  = "outputs/step5_soap_ai_results.xlsx"
    nlp_file = "outputs/step6_nlp_mdm_results.xlsx"
    ai_ok    = os.path.exists(ai_file)
    nlp_ok   = os.path.exists(nlp_file)

    if not ai_ok and not nlp_ok:
        st.info("To enable AI analysis, run the following scripts and push "
                "the output files to your repository:")
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
                a1.metric("Visits billed too low", f"{under_ai}",
                          f"{under_ai/len(ai)*100:.0f}% of reviewed visits")
                a2.metric("Correctly billed",      f"{corr_ai}",
                          f"{corr_ai/len(ai)*100:.0f}% of reviewed visits")
                a3.metric("Billed too high ⚠️",    f"{over_ai}",
                          "May trigger insurance audit")
                a4.metric("AI-identified gap",     f"${gap_ai:,.0f}",
                          "From clinical note analysis")

                if over_ai > 0:
                    st.error(f"⚠️ {over_ai} visits were billed at a level the clinical "
                             f"notes do not fully support. These should be reviewed "
                             f"before the next billing cycle to avoid audit risk.")

                st.markdown("#### What did the AI find in each visit note?")
                whatis("The AI read each provider's clinical note and determined "
                       "the appropriate billing code based on what was documented — "
                       "number of health problems addressed, tests reviewed, "
                       "medications changed, and referrals placed.")

                fc = ai["Coding_Flag"].value_counts().reset_index()
                fc.columns = ["Finding","Visits"]
                cmap = {"UNDERCODED":RED,"CORRECT":GREEN,
                        "OVERCODED":AMBER,"Non-EM":GRAY,"—":GRAY}
                fig_fc = px.bar(fc, x="Finding", y="Visits",
                                color="Finding", color_discrete_map=cmap,
                                text="Visits")
                fig_fc.update_traces(textposition="outside", marker_opacity=0.88)
                fig_fc.update_layout(showlegend=False, height=320,
                                     xaxis=dict(**GRID), yaxis=dict(**GRID),
                                     **PLOT_CFG)
                st.plotly_chart(fig_fc, use_container_width=True)
                insight("'Billed too high' findings are just as important as "
                        "'billed too low' — they represent compliance risk, "
                        "not just revenue opportunity.")

                st.markdown("#### Visit-by-visit AI findings")
                whatis("The 'AI explanation' column shows exactly why the AI "
                       "recommended a different billing code — written in the same "
                       "language a certified billing specialist would use.")
                ff = st.selectbox("Show me", ["All findings","Billed too low",
                                              "Correctly billed","Billed too high"])
                fmap = {"All findings":None,"Billed too low":"UNDERCODED",
                        "Correctly billed":"CORRECT","Billed too high":"OVERCODED"}
                fai = ai if fmap[ff] is None else ai[ai["Coding_Flag"]==fmap[ff]]
                show = ["Visit_ID","Provider_Name","Visit_Type",
                        "CPT_Submitted","CPT_Recommended_AI",
                        "Coding_Flag","Revenue_Gap_$","AI_Reasoning"]
                show = [c for c in show if c in fai.columns]
                rename = {"CPT_Submitted":"Code submitted",
                          "CPT_Recommended_AI":"AI recommendation",
                          "Coding_Flag":"Finding",
                          "Revenue_Gap_$":"Gap ($)",
                          "AI_Reasoning":"AI explanation"}
                st.dataframe(fai[show].rename(columns=rename).head(25),
                             use_container_width=True, hide_index=True, height=400)
            else:
                st.info("Run step5_ai_soap_analyzer.py to enable this tab.")

        with tabs[1]:
            if nlp_ok:
                nlp = pd.read_excel(nlp_file, sheet_name="NLP_Results")
                st.markdown("#### How complex were the visits — by visit type?")
                whatis("ClarityCode scores each visit note on a scale of 0–100 "
                       "based on six clinical signals: how many health problems "
                       "were addressed, which tests were reviewed, whether "
                       "medications were changed, whether a referral was placed, "
                       "whether patient education was documented, and how long "
                       "the visit was. A score above 70 typically warrants a "
                       "higher billing code.")

                if "MDM_Score_0_100" in nlp.columns:
                    avg = (nlp.groupby("Visit_Type")["MDM_Score_0_100"]
                           .mean().round(1).sort_values().reset_index())
                    avg.columns = ["Visit type","Avg complexity score"]
                    fig_nlp = px.bar(avg, x="Avg complexity score", y="Visit type",
                                     orientation="h",
                                     color="Avg complexity score",
                                     color_continuous_scale=[GREEN, AMBER, RED],
                                     text="Avg complexity score")
                    fig_nlp.update_traces(textposition="outside", marker_opacity=0.88)
                    fig_nlp.update_layout(
                        height=400, showlegend=False,
                        coloraxis_showscale=False,
                        xaxis=dict(range=[0,105], **GRID),
                        yaxis=dict(**GRID),
                        **PLOT_CFG
                    )
                    st.plotly_chart(fig_nlp, use_container_width=True)
                    insight("Heart failure and multi-chronic condition visits score "
                            "highest — meaning providers are documenting complex care. "
                            "If those visits are being billed at a low level, there is "
                            "a direct documentation-to-billing disconnect.")

                st.markdown("#### Signal breakdown per visit")
                whatis("This table shows exactly what clinical signals were found "
                       "in each note and how they contributed to the complexity score.")
                sig = ["Visit_ID","Provider_Name","Problems_Count","Labs_Count",
                       "Referrals_Count","Med_Changes_Count","Time_Documented_Min",
                       "MDM_Score_0_100","CPT_Submitted","CPT_Recommended_NLP"]
                sig = [c for c in sig if c in nlp.columns]
                rename_nlp = {
                    "Problems_Count":"Problems addressed",
                    "Labs_Count":"Tests reviewed",
                    "Referrals_Count":"Referrals made",
                    "Med_Changes_Count":"Medication changes",
                    "Time_Documented_Min":"Time documented (min)",
                    "MDM_Score_0_100":"Complexity score (0–100)",
                    "CPT_Submitted":"Code submitted",
                    "CPT_Recommended_NLP":"Recommended code",
                }
                st.dataframe(nlp[sig].rename(columns=rename_nlp),
                             use_container_width=True, hide_index=True)
            else:
                st.info("Run step6_nlp_mdm_extractor.py to enable this tab.")

        with tabs[2]:
            st.markdown("#### Visits flagged by both AI and clinical scoring")
            whatis("When the AI note review AND the clinical complexity score "
                   "both flag the same visit as billed too low, that is the "
                   "strongest possible evidence. These cases are nearly "
                   "impossible to dispute in a billing review or provider "
                   "coaching session.")
            if ai_ok and nlp_ok:
                ai2  = pd.read_excel(ai_file,  sheet_name="All_AI_Results")
                nlp2 = pd.read_excel(nlp_file, sheet_name="NLP_Results")
                ai_u  = set(ai2[ai2["Coding_Flag"]=="UNDERCODED"]["Visit_ID"].astype(str))
                nlp_u = set(nlp2[nlp2["Coding_Flag"]=="UNDERCODED"]["Visit_ID"].astype(str)) if "Coding_Flag" in nlp2.columns else set()
                both  = ai_u & nlp_u

                b1,b2,b3 = st.columns(3)
                b1.metric("AI only",         len(ai_u - nlp_u),  "Single method")
                b2.metric("Scoring only",    len(nlp_u - ai_u),  "Single method")
                b3.metric("Both methods ✓",  len(both),          "Highest confidence")

                if both:
                    both_df = ai2[ai2["Visit_ID"].astype(str).isin(both)]
                    show = ["Visit_ID","Provider_Name","Visit_Type",
                            "CPT_Submitted","CPT_Recommended_AI",
                            "Revenue_Gap_$","AI_Reasoning"]
                    show = [c for c in show if c in both_df.columns]
                    st.dataframe(both_df[show].rename(columns={
                        "CPT_Submitted":"Code submitted",
                        "CPT_Recommended_AI":"AI recommendation",
                        "Revenue_Gap_$":"Gap ($)",
                        "AI_Reasoning":"Why it was flagged",
                    }), use_container_width=True, hide_index=True)
                    st.success(f"These {len(both)} visits have the strongest evidence "
                               f"of underbilling and should be prioritized for "
                               f"clinical coder review.")
            else:
                st.info("Run both analysis scripts to unlock this view.")

# ══════════════════════════════════════════════════════════════
# PAGE 4 — MISSING BILLING CODES
# ══════════════════════════════════════════════════════════════
elif page == "Missing Billing Codes":
    st.title("Missing Billing Codes")
    st.markdown("""
    <div class='problem-card'>
      <div class='problem-headline' style='font-size:1.1rem'>
        Some billing codes are never submitted — even when visits clearly qualify.
      </div>
      <div class='problem-body' style='font-size:0.92rem'>
        Beyond the main visit billing code, certain types of care qualify for
        additional reimbursement. These "add-on codes" are separate billing entries
        that attach to the primary visit. Most providers are unaware they exist —
        which means qualifying patients are seen, the care is delivered,
        but the additional reimbursement is never claimed.
      </div>
    </div>
    """, unsafe_allow_html=True)

    ccm = pc_f["CCM_Missing"].sum()
    bhi = pc_f["BHI_Missing"].sum()
    g22 = pc_f["G2211_Missing"].sum()
    p90 = psych_f["90833_Missing"].sum()

    a1,a2,a3,a4 = st.columns(4)
    a1.metric("Chronic Care Management", f"${ccm*62:,.0f}",
              f"99490 · {ccm} qualifying visits")
    a2.metric("Behavioral Health Integration", f"${bhi*45:,.0f}",
              f"99484 · {bhi} qualifying visits")
    a3.metric("Complex Care Add-on",    f"${g22*16:,.0f}",
              f"G2211 · {g22} qualifying visits")
    a4.metric("Therapy Session Add-on", f"${p90*65:,.0f}",
              f"90833 · {p90} qualifying visits")

    st.divider()
    st.markdown("#### Which missing codes have the biggest impact?")
    whatis("Each of these codes represents a type of care that was delivered "
           "but not billed. They are not duplicate charges — they are separate "
           "billable services with their own reimbursement rates.")

    add_df = pd.DataFrame({
        "Billing code": [
            "Chronic Care Management (99490)",
            "Therapy Session Add-on (90833)",
            "Complex Care Add-on (G2211)",
            "Behavioral Health Integration (99484)",
        ],
        "Plain English": [
            "Monthly care coordination for patients with 2+ chronic conditions",
            "Combined medication review + therapy in one psychiatry visit",
            "Extra complexity billing for primary care visits with 3+ diagnoses",
            "Behavioral health support delivered alongside primary care",
        ],
        "Qualifying visits": [ccm, p90, g22, bhi],
        "Uncollected ($)":   [ccm*62, p90*65, g22*16, bhi*45],
        "Rate per visit":    ["$62/month","$65/visit","$16/visit","$45/visit"],
    }).sort_values("Uncollected ($)", ascending=True)

    fig_add = go.Figure(go.Bar(
        x=add_df["Uncollected ($)"],
        y=add_df["Billing code"],
        orientation="h",
        marker_color=[AMBER, RED, AMBER, RED][::-1],
        marker_opacity=0.88,
        text=add_df["Uncollected ($)"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside",
        textfont=dict(size=12),
        customdata=add_df[["Plain English","Qualifying visits","Rate per visit"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "%{customdata[0]}<br>"
            "Qualifying visits: %{customdata[1]}<br>"
            "Rate: %{customdata[2]}"
            "<extra></extra>"
        ),
    ))
    fig_add.update_layout(height=320, xaxis=dict(tickprefix="$",tickformat=",",**GRID),
                          yaxis=dict(**GRID), **PLOT_CFG)
    st.plotly_chart(fig_add, use_container_width=True)
    insight("Chronic Care Management is the biggest opportunity — and unlike "
            "a one-time billing fix, it generates new revenue every month "
            "for every qualifying patient.")

    st.markdown("#### Chronic Care Management — monthly recurring revenue")
    whatis("Chronic Care Management (billing code 99490) pays $62 per patient "
           "per month for care coordination of patients with two or more chronic "
           "conditions like diabetes and hypertension. This requires documenting "
           "20 minutes of care coordination per month. If your team is already "
           "doing this coordination but not documenting it, this is a training fix.")
    qualifying = st.slider("Patients qualifying for monthly billing",
                           10, 500, int(ccm), step=1)
    m1,m2,m3 = st.columns(3)
    m1.metric("Monthly additional revenue", f"${qualifying*62:,.0f}")
    m2.metric("Annual additional revenue",  f"${qualifying*62*12:,.0f}")
    m3.metric("3-year revenue potential",   f"${qualifying*62*36:,.0f}")
    st.warning("To bill for Chronic Care Management, the care coordination "
               "time must be documented in the patient chart each month. "
               "This is a documentation habit — not extra clinical work.")

# ══════════════════════════════════════════════════════════════
# PAGE 5 — REVIEW QUEUE
# ══════════════════════════════════════════════════════════════
elif page == "Review Queue":
    st.title("Billing Review Queue")
    st.markdown("""
    <div class='problem-card'>
      <div class='problem-headline' style='font-size:1.1rem'>
        Every visit that needs a second look — in one place.
      </div>
      <div class='problem-body' style='font-size:0.92rem'>
        This queue shows every visit where the submitted billing code may not
        match what the visit documentation supports. Use the filters to focus
        on specific providers or flag types. Download the list and work through
        it with your billing team. Every visit here requires human review
        before any changes are made — ClarityCode identifies, your team decides.
      </div>
    </div>
    """, unsafe_allow_html=True)

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
        issue_f = st.selectbox("Issue type",
            ["All issues","Billed too low",
             "Missing monthly billing code","Missing therapy add-on code"])
    with f2:
        prov_f = st.selectbox("Provider",
            ["All providers"]+sorted(all_flagged["Provider_Name"].unique().tolist()))
    with f3:
        min_gap = st.slider("Minimum gap ($)", 0, 200, 0, step=10)

    filt = all_flagged.copy()
    if issue_f != "All issues":     filt = filt[filt["Issue"]==issue_f]
    if prov_f  != "All providers":  filt = filt[filt["Provider_Name"]==prov_f]
    filt = filt[filt["Gap_$"] >= min_gap]

    st.markdown(f"**{len(filt):,} visits** need review · "
                f"Total estimated gap: **${filt['Gap_$'].sum():,.0f}**")

    display = filt[[
        "Visit_ID","Visit_Date","Provider_Name","Location","Visit_Type",
        "CPT_Code_Submitted","Recommended","Visit_Duration_Min","Gap_$","Issue","Payer"
    ]].copy()
    display["Visit_Date"] = pd.to_datetime(display["Visit_Date"]).dt.strftime("%b %d, %Y")
    display["Gap_$"]      = display["Gap_$"].apply(lambda x: f"${x:,.0f}")
    display.columns = ["Visit ID","Date","Provider","Location","Visit type",
                       "Code submitted","Recommended","Visit length (min)",
                       "Est. gap","Issue","Insurance"]
    st.dataframe(display, use_container_width=True, hide_index=True, height=480)

    csv = filt.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download review list as CSV",
                       data=csv, file_name="billing_review_queue.csv",
                       mime="text/csv")

# ══════════════════════════════════════════════════════════════
# PAGE 6 — HOW IT WORKS
# ══════════════════════════════════════════════════════════════
elif page == "How It Works":
    st.title("How ClarityCode works")
    st.markdown("""
    <div class='problem-card'>
      <div class='problem-headline' style='font-size:1.1rem'>
        Transparent analysis. Every finding has a documented reason.
      </div>
      <div class='problem-body' style='font-size:0.92rem'>
        ClarityCode does not make changes to any billing records. It analyzes
        visit data, surfaces potential discrepancies, and presents them for
        human review. The methodology is based entirely on publicly available
        federal billing guidelines — not proprietary algorithms.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### The problem ClarityCode solves")
    st.markdown("""
Healthcare organizations bill insurance companies using standardized codes
that describe what happened during a visit. A code like **99213** means a
20-29 minute visit with low medical complexity. A **99215** means a 40+ minute
visit with high complexity.

When providers submit codes that are lower than what the visit documentation
supports, the insurance company pays less — and the organization absorbs the
difference silently. This is called **underbilling** or **undercoding**.

Similarly, certain types of care qualify for **additional billing codes**
on top of the primary visit code. Chronic disease coordination, behavioral
health integration, and therapy sessions all have dedicated codes worth
$16–$65 per visit. Most organizations never submit these.
""")

    st.markdown("#### How the analysis works")
    steps = {
        "Step 1 — Load visit data": (
            "ClarityCode reads your EHR visit extract — provider, patient demographics, "
            "visit type, billing codes submitted, visit duration, and diagnoses."
        ),
        "Step 2 — Apply billing rules": (
            "Federal CMS 2021 guidelines specify exactly how long a visit must be "
            "to justify each billing code. ClarityCode compares every primary care "
            "visit's duration against these thresholds and flags mismatches."
        ),
        "Step 3 — Check for missing codes": (
            "ClarityCode checks each visit against known qualifying criteria for "
            "add-on billing codes — chronic conditions, behavioral health diagnoses, "
            "combined psychiatry and therapy visits."
        ),
        "Step 4 — AI reads the clinical notes": (
            "For visits with full clinical notes (SOAP format), ClarityCode uses "
            "Claude AI to read the note and determine what billing code the "
            "documented complexity of care supports — independent of duration."
        ),
        "Step 5 — Score clinical complexity": (
            "A natural language processing (NLP) model extracts six clinical signals "
            "from each note and produces a complexity score from 0 to 100. "
            "This score is used alongside the AI analysis to identify the "
            "highest-confidence findings."
        ),
    }
    for title, body in steps.items():
        with st.expander(title, expanded=False):
            st.write(body)

    st.markdown("#### Important limitations")
    st.warning("""
**Before acting on any finding in this dashboard:**

- This analysis identifies **potential** billing discrepancies — it does not confirm them
- Every flagged visit must be reviewed by a **certified medical coder** before any claim is modified
- Reimbursement estimates use **Medicare average rates** — your actual contracted rates with each insurer will differ
- Patients on **self-pay** should be excluded from Chronic Care Management and G2211 recommendations
- This dashboard currently runs on **synthetic (non-real) patient data** for demonstration purposes
""")

    st.markdown("#### Official sources")
    refs = {
        "CMS 2021 E&M Office Visit Guidelines": "https://www.cms.gov/medicare/physician-fee-schedule/2021-office-outpatient-evaluation-and-management",
        "Medicare Physician Fee Schedule": "https://www.cms.gov/medicare/payment/fee-schedules/physician",
        "Chronic Care Management billing guide": "https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/mlnproducts/downloads/chroniccaremanagement.pdf",
        "AAPC CPT code reference": "https://www.aapc.com/codes/",
        "ICD-10 diagnosis code browser": "https://icd.cdc.gov/icd10cm/",
        "OIG compliance guidance": "https://oig.hhs.gov/reports-and-publications/workplan/",
    }
    for name, url in refs.items():
        st.markdown(f"- [{name}]({url})")

    st.markdown("---")
    st.caption("Built by Ankita Shinde · Health Systems Product Manager · "
               "ClarityCode v2.0 · Synthetic data only · "
               "github.com/ankitashinde99/coding-intelligence")
