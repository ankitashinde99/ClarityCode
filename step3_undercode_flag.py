import pandas as pd

# ─────────────────────────────────────────────
# STEP 3 — Undercode Flagging
# Compares visit duration against submitted CPT
# using CMS 2021 time-based E&M rules
# ─────────────────────────────────────────────

# Load the file
df = pd.read_excel("ehr_raw_data.xlsx",
                   sheet_name="Raw Visit Data")

print("File loaded —", len(df), "visits\n")


# ─────────────────────────────────────────────
# PART 1: What CPT code SHOULD have been used?
# Based on CMS 2021 time thresholds
# ─────────────────────────────────────────────

def expected_cpt(minutes):
    """Given visit duration, return the correct E&M code."""
    if pd.isna(minutes):
        return None
    m = int(minutes)
    if m <= 9:   return "99211"
    if m <= 19:  return "99212"
    if m <= 29:  return "99213"
    if m <= 39:  return "99214"
    return "99215"  # 40+ minutes


# Apply only to Primary Care — BH and Psych use different code sets
pc = df[df["Service_Line"] == "Primary Care"].copy()
pc["Expected_CPT"] = pc["Visit_Duration_Min"].apply(expected_cpt)


# ─────────────────────────────────────────────
# PART 2: Compare submitted vs expected
# ─────────────────────────────────────────────

em_order = ["99211", "99212", "99213", "99214", "99215"]

def flag_visit(row):
    """Compare what was submitted vs what was expected."""
    submitted = row["CPT_Code_Submitted"]
    expected  = row["Expected_CPT"]

    # Skip visits where submitted code is not a standard E&M code
    if submitted not in em_order:
        return "Non E&M code — skip"

    if expected not in em_order:
        return "Cannot determine"

    submitted_level = em_order.index(submitted)
    expected_level  = em_order.index(expected)

    if submitted_level < expected_level:
        return "UNDERCODED"
    elif submitted_level > expected_level:
        return "OVERCODED"
    else:
        return "CORRECT"


pc["Coding_Flag"] = pc.apply(flag_visit, axis=1)


# ─────────────────────────────────────────────
# PART 3: Calculate the revenue gap per visit
# Using Medicare average reimbursement rates
# ─────────────────────────────────────────────

reimbursement = {
    "99211":  24,
    "99212":  55,
    "99213":  92,
    "99214": 136,
    "99215": 193,
}

def revenue_gap(row):
    """How much money was left on the table for this visit?"""
    if row["Coding_Flag"] != "UNDERCODED":
        return 0.0
    submitted_rate = reimbursement.get(row["CPT_Code_Submitted"], 0)
    expected_rate  = reimbursement.get(row["Expected_CPT"], 0)
    return expected_rate - submitted_rate


pc["Revenue_Gap_$"] = pc.apply(revenue_gap, axis=1)


# ─────────────────────────────────────────────
# PART 4: Print the results
# ─────────────────────────────────────────────

print("=" * 55)
print("  OVERALL CODING FLAG SUMMARY — PRIMARY CARE")
print("=" * 55)
print(pc["Coding_Flag"].value_counts())
print()

total_gap = pc["Revenue_Gap_$"].sum()
undercode_count = (pc["Coding_Flag"] == "UNDERCODED").sum()
total_pc = len(pc)
undercode_rate = undercode_count / total_pc * 100

print("=" * 55)
print("  REVENUE IMPACT")
print("=" * 55)
print(f"  Total Primary Care visits   : {total_pc}")
print(f"  Undercoded visits           : {undercode_count}")
print(f"  Undercode rate              : {undercode_rate:.1f}%")
print(f"  Total estimated revenue gap : ${total_gap:,.0f}")
print(f"  Avg gap per undercoded visit: ${total_gap / undercode_count if undercode_count > 0 else 0:,.0f}")
print()

print("=" * 55)
print("  UNDERCODED VISITS BY PROVIDER")
print("=" * 55)
provider_summary = (
    pc.groupby("Provider_Name")
    .agg(
        Total_Visits     = ("Visit_ID",       "count"),
        Undercoded       = ("Coding_Flag",    lambda x: (x == "UNDERCODED").sum()),
        Revenue_Gap      = ("Revenue_Gap_$",  "sum"),
    )
    .reset_index()
)
provider_summary["Undercode_Rate_%"] = (
    provider_summary["Undercoded"] / provider_summary["Total_Visits"] * 100
).round(1)
provider_summary = provider_summary.sort_values("Revenue_Gap", ascending=False)
print(provider_summary.to_string(index=False))
print()

print("=" * 55)
print("  UNDERCODED VISITS BY VISIT TYPE")
print("=" * 55)
visit_summary = (
    pc.groupby("Visit_Type")
    .agg(
        Total_Visits = ("Visit_ID",       "count"),
        Undercoded   = ("Coding_Flag",    lambda x: (x == "UNDERCODED").sum()),
        Revenue_Gap  = ("Revenue_Gap_$",  "sum"),
        Avg_Duration = ("Visit_Duration_Min", "mean"),
    )
    .reset_index()
)
visit_summary["Undercode_Rate_%"] = (
    visit_summary["Undercoded"] / visit_summary["Total_Visits"] * 100
).round(1)
visit_summary = visit_summary.sort_values("Revenue_Gap", ascending=False)
print(visit_summary.to_string(index=False))
print()

print("=" * 55)
print("  SUBMITTED vs EXPECTED CODE BREAKDOWN")
print("=" * 55)
mismatch = (
    pc[pc["Coding_Flag"] == "UNDERCODED"]
    .groupby(["CPT_Code_Submitted", "Expected_CPT"])
    .agg(Count=("Visit_ID", "count"), Revenue_Gap=("Revenue_Gap_$", "sum"))
    .reset_index()
    .sort_values("Revenue_Gap", ascending=False)
)
print(mismatch.to_string(index=False))
print()


# ─────────────────────────────────────────────
# PART 5: Save results to Excel
# ─────────────────────────────────────────────

output_path = "outputs/step3_undercode_results.xlsx"

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    pc.to_excel(writer, sheet_name="All_PC_Visits_Flagged", index=False)
    provider_summary.to_excel(writer, sheet_name="Provider_Summary", index=False)
    visit_summary.to_excel(writer, sheet_name="Visit_Type_Summary", index=False)
    mismatch.to_excel(writer, sheet_name="Code_Mismatch_Detail", index=False)

print("=" * 55)
print(f"  Results saved to: {output_path}")
print("=" * 55)