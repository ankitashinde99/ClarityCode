import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Load data ──────────────────────────────────────────────────────────────
df = pd.read_excel("ehr_raw_data.xlsx", sheet_name="Raw Visit Data")
os.makedirs("outputs", exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "font.size": 11})

# ── Chart 1: Visits by Service Line ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
counts = df["Service_Line"].value_counts()
bars = ax.bar(counts.index, counts.values, color=["#4C72B0", "#DD8452", "#55A868"])
ax.bar_label(bars, padding=4)
ax.set_title("Visits by Service Line", fontweight="bold")
ax.set_ylabel("Number of Visits")
ax.set_ylim(0, counts.max() * 1.15)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/chart1_visits_by_service_line.png")
plt.close()
print("Saved: chart1_visits_by_service_line.png")

# ── Chart 2: Top 10 CPT Codes ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
top_cpt = df["CPT_Code_Submitted"].value_counts().head(10)
bars = ax.barh(top_cpt.index.astype(str)[::-1], top_cpt.values[::-1], color="#4C72B0")
ax.bar_label(bars, padding=4)
ax.set_title("Top 10 CPT Codes Submitted", fontweight="bold")
ax.set_xlabel("Number of Visits")
ax.set_xlim(0, top_cpt.max() * 1.15)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/chart2_top_cpt_codes.png")
plt.close()
print("Saved: chart2_top_cpt_codes.png")

# ── Chart 3: Average Visit Duration by Visit Type ──────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
avg_dur = (df.groupby("Visit_Type")["Visit_Duration_Min"]
             .mean().round(1).sort_values())
bars = ax.barh(avg_dur.index, avg_dur.values, color="#55A868")
ax.bar_label(bars, fmt="%.1f min", padding=4)
ax.set_title("Average Visit Duration by Visit Type", fontweight="bold")
ax.set_xlabel("Duration (minutes)")
ax.set_xlim(0, avg_dur.max() * 1.2)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/chart3_avg_duration_by_visit_type.png")
plt.close()
print("Saved: chart3_avg_duration_by_visit_type.png")

# ── Chart 4: Visits by Payer ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
payer_counts = df["Payer"].value_counts()
bars = ax.barh(payer_counts.index[::-1], payer_counts.values[::-1], color="#DD8452")
ax.bar_label(bars, padding=4)
ax.set_title("Visits by Payer", fontweight="bold")
ax.set_xlabel("Number of Visits")
ax.set_xlim(0, payer_counts.max() * 1.15)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/chart4_visits_by_payer.png")
plt.close()
print("Saved: chart4_visits_by_payer.png")

# ── Chart 5: Visits by Modality ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4))
mod_counts = df["Modality"].value_counts()
wedges, texts, autotexts = ax.pie(
    mod_counts.values,
    labels=mod_counts.index,
    autopct="%1.1f%%",
    colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52"],
    startangle=140,
)
for at in autotexts:
    at.set_fontsize(9)
ax.set_title("Visits by Modality", fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/chart5_visits_by_modality.png")
plt.close()
print("Saved: chart5_visits_by_modality.png")

# ── Chart 6: Claim Status Breakdown ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
claim_counts = df["Claim_Status"].value_counts()
colors = ["#55A868" if s == "Clean" else "#DD8452" if s == "Pending" else "#C44E52"
          for s in claim_counts.index]
bars = ax.bar(claim_counts.index, claim_counts.values, color=colors)
ax.bar_label(bars, padding=4)
ax.set_title("Claim Status Breakdown", fontweight="bold")
ax.set_ylabel("Number of Claims")
ax.set_ylim(0, claim_counts.max() * 1.15)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("outputs/chart6_claim_status.png")
plt.close()
print("Saved: chart6_claim_status.png")

print("\nAll 6 charts saved to outputs/")
