import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyreadstat
import os

# Load the DHS Children's Recode Stata file pyreadstat preserves variable labels from the Stata file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data", "raw", "NGKR8BFL.dta")

df, meta = pyreadstat.read_dta(
    data_path,
    apply_value_formats=True
)

print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumns:")
print(df.columns.tolist())

# SELECT RELEVANT COLUMNS
cols_needed = ['hw70', 'hw71', 'hw72', 'v024', 'v025', 
               'v190', 'b4', 'b8', 'v106']

print("\nChecking key variables:")
for col in cols_needed:
    if col in df.columns:
        print(f"  {col}: found - sample values: {df[col].unique()[:5]}")
    else:
        print(f"  {col}: NOT FOUND")

# BUILD WORKING DATASET
# Select only the columns we need
df_work = df[cols_needed].copy()

# Rename columns to readable names
df_work.columns = [
    'stunting_zscore',
    'wasting_zscore', 
    'underweight_zscore',
    'region',
    'residence',
    'wealth_index',
    'child_sex',
    'child_age_years',
    'mother_education'
]

# Z-scores are stored as integers x 100 in DHS
# Convert to actual Z-scores by dividing by 100
# First convert to numeric, flagged cases become NaN
df_work['stunting_zscore'] = pd.to_numeric(
    df_work['stunting_zscore'], errors='coerce'
) / 100

df_work['wasting_zscore'] = pd.to_numeric(
    df_work['wasting_zscore'], errors='coerce'
) / 100

df_work['underweight_zscore'] = pd.to_numeric(
    df_work['underweight_zscore'], errors='coerce'
) / 100

# WHO definition: Z-score below -2 = malnourished
df_work['stunted'] = (df_work['stunting_zscore'] < -2).astype(float)
df_work['wasted'] = (df_work['wasting_zscore'] < -2).astype(float)
df_work['underweight'] = (df_work['underweight_zscore'] < -2).astype(float)

# Set to NaN where Z-score is missing
df_work.loc[df_work['stunting_zscore'].isna(), 'stunted'] = np.nan
df_work.loc[df_work['wasting_zscore'].isna(), 'wasted'] = np.nan
df_work.loc[df_work['underweight_zscore'].isna(), 'underweight'] = np.nan

print("\nWorking dataset shape:", df_work.shape)
print("\nMissing values:")
print(df_work.isnull().sum())
print("\nMalnutrition prevalence (among measured children):")
print(f"  Stunting:     {df_work['stunted'].mean()*100:.1f}%")
print(f"  Wasting:      {df_work['wasted'].mean()*100:.1f}%")
print(f"  Underweight:  {df_work['underweight'].mean()*100:.1f}%")

# UNDERSTAND MISSING Z-SCORES
print("\nAge distribution of all children:")
print(df_work['child_age_years'].value_counts(dropna=False).sort_index())

print("\nChildren with Z-scores available by age:")
print(df_work[df_work['stunting_zscore'].notna()]['child_age_years'].value_counts(dropna=False).sort_index())

# CHECK FOR IMPLAUSIBLE Z-SCORES

# WHO flags Z-scores outside these ranges as implausible
# Stunting (HAZ): -6 to +6
# Wasting (WHZ): -5 to +5
# Underweight (WAZ): -6 to +5

print("\nZ-score ranges before cleaning:")
print(f"  Stunting:    {df_work['stunting_zscore'].min():.2f} to {df_work['stunting_zscore'].max():.2f}")
print(f"  Wasting:     {df_work['wasting_zscore'].min():.2f} to {df_work['wasting_zscore'].max():.2f}")
print(f"  Underweight: {df_work['underweight_zscore'].min():.2f} to {df_work['underweight_zscore'].max():.2f}")

# Apply WHO plausibility flags
df_work.loc[
    (df_work['stunting_zscore'] < -6) | (df_work['stunting_zscore'] > 6),
    ['stunting_zscore', 'stunted']
] = np.nan

df_work.loc[
    (df_work['wasting_zscore'] < -5) | (df_work['wasting_zscore'] > 5),
    ['wasting_zscore', 'wasted']
] = np.nan

df_work.loc[
    (df_work['underweight_zscore'] < -6) | (df_work['underweight_zscore'] > 5),
    ['underweight_zscore', 'underweight']
] = np.nan

print("\nZ-score ranges after cleaning:")
print(f"  Stunting:    {df_work['stunting_zscore'].min():.2f} to {df_work['stunting_zscore'].max():.2f}")
print(f"  Wasting:     {df_work['wasting_zscore'].min():.2f} to {df_work['wasting_zscore'].max():.2f}")
print(f"  Underweight: {df_work['underweight_zscore'].min():.2f} to {df_work['underweight_zscore'].max():.2f}")

print("\nMalnutrition prevalence after removing implausible values:")
print(f"  Stunting:     {df_work['stunted'].mean()*100:.1f}%")
print(f"  Wasting:      {df_work['wasted'].mean()*100:.1f}%")
print(f"  Underweight:  {df_work['underweight'].mean()*100:.1f}%")

# CREATE ANALYSIS SUBSET
# Keep only children with at least one Z-score measurement
df_measured = df_work[
    df_work['stunting_zscore'].notna() |
    df_work['wasting_zscore'].notna() |
    df_work['underweight_zscore'].notna()
].copy()

print("\nAnalysis subset shape:", df_measured.shape)
print("\nSample breakdown:")
print(f"  By region:\n{df_measured['region'].value_counts()}")
print(f"\n  By residence:\n{df_measured['residence'].value_counts()}")
print(f"\n  By wealth index:\n{df_measured['wealth_index'].value_counts()}")
print(f"\n  By mother's education:\n{df_measured['mother_education'].value_counts()}")

# ANALYSIS AND VISUALISATIONS
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
visuals_dir = os.path.join(base_dir, "visuals")
os.makedirs(visuals_dir, exist_ok=True)

# Colour palette
colors = ['#c0392b', '#e67e22', '#f1c40f']
indicators = ['stunted', 'wasted', 'underweight']
labels = ['Stunting', 'Wasting', 'Underweight']

# ── Chart 1: National prevalence overview ──
national = [df_measured[i].mean() * 100 for i in indicators]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, national, color=colors, width=0.5)
ax.set_ylabel("Prevalence (%)")
ax.set_title("Child Malnutrition Prevalence in Nigeria (2024 DHS)")
ax.set_ylim(0, 50)
for bar, val in zip(bars, national):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha='center', va='bottom', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(visuals_dir, "national_prevalence.png"), dpi=150)
plt.close()
print("Chart 1 saved: national_prevalence.png")

# ── Chart 2: Prevalence by region ──
region_prev = df_measured.groupby('region')[indicators].mean() * 100
region_prev.columns = labels
region_prev = region_prev.sort_values('Stunting', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(region_prev))
width = 0.25
for i, (col, color) in enumerate(zip(labels, colors)):
    ax.bar([p + i*width for p in x], region_prev[col],
           width=width, label=col, color=color)
ax.set_xticks([p + width for p in x])
ax.set_xticklabels(region_prev.index, rotation=15, ha='right')
ax.set_ylabel("Prevalence (%)")
ax.set_title("Child Malnutrition by Region (2024 DHS)")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(visuals_dir, "prevalence_by_region.png"), dpi=150)
plt.close()
print("Chart 2 saved: prevalence_by_region.png")

# ── Chart 3: Prevalence by residence ──
residence_prev = df_measured.groupby('residence')[indicators].mean() * 100
residence_prev.columns = labels

fig, ax = plt.subplots(figsize=(7, 5))
x = range(len(residence_prev))
for i, (col, color) in enumerate(zip(labels, colors)):
    ax.bar([p + i*width for p in x], residence_prev[col],
           width=width, label=col, color=color)
ax.set_xticks([p + width for p in x])
ax.set_xticklabels(residence_prev.index)
ax.set_ylabel("Prevalence (%)")
ax.set_title("Child Malnutrition by Residence Type (2024 DHS)")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(visuals_dir, "prevalence_by_residence.png"), dpi=150)
plt.close()
print("Chart 3 saved: prevalence_by_residence.png")

# ── Chart 4: Prevalence by wealth index ──
wealth_order = ['poorest', 'poorer', 'middle', 'richer', 'richest']
wealth_prev = df_measured.groupby('wealth_index')[indicators].mean() * 100
wealth_prev.columns = labels
wealth_prev = wealth_prev.reindex(wealth_order)

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(wealth_prev))
for i, (col, color) in enumerate(zip(labels, colors)):
    ax.bar([p + i*width for p in x], wealth_prev[col],
           width=width, label=col, color=color)
ax.set_xticks([p + width for p in x])
ax.set_xticklabels(wealth_prev.index)
ax.set_ylabel("Prevalence (%)")
ax.set_title("Child Malnutrition by Household Wealth (2024 DHS)")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(visuals_dir, "prevalence_by_wealth.png"), dpi=150)
plt.close()
print("Chart 4 saved: prevalence_by_wealth.png")

# ── Chart 5: Prevalence by mother's education ──
edu_order = ['no education', 'primary', 'secondary', 'higher']
edu_prev = df_measured.groupby('mother_education')[indicators].mean() * 100
edu_prev.columns = labels
edu_prev = edu_prev.reindex(edu_order)

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(edu_prev))
for i, (col, color) in enumerate(zip(labels, colors)):
    ax.bar([p + i*width for p in x], edu_prev[col],
           width=width, label=col, color=color)
ax.set_xticks([p + width for p in x])
ax.set_xticklabels(edu_prev.index)
ax.set_ylabel("Prevalence (%)")
ax.set_title("Child Malnutrition by Mother's Education Level (2024 DHS)")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(visuals_dir, "prevalence_by_education.png"), dpi=150)
plt.close()
print("Chart 5 saved: prevalence_by_education.png")

# ── Chart 6: Prevalence by child age ──
age_prev = df_measured.groupby('child_age_years')[indicators].mean() * 100
age_prev.columns = labels

fig, ax = plt.subplots(figsize=(9, 5))
for col, color in zip(labels, colors):
    ax.plot(age_prev.index, age_prev[col], marker='o', label=col, color=color)
ax.set_xlabel("Child Age (years)")
ax.set_ylabel("Prevalence (%)")
ax.set_title("Child Malnutrition by Age Group (2024 DHS)")
ax.legend()
ax.set_xticks([0, 1, 2, 3, 4])
plt.tight_layout()
plt.savefig(os.path.join(visuals_dir, "prevalence_by_age.png"), dpi=150)
plt.close()
print("Chart 6 saved: prevalence_by_age.png")

print("\nAll charts saved successfully.")

# SUMMARY STATISTICS FOR DOCUMENTATION
print("\n" + "="*55)
print("SUMMARY STATISTICS")
print("="*55)

print(f"\nTotal children measured: {len(df_measured):,}")

print("\nNational Prevalence:")
for ind, lab in zip(indicators, labels):
    n = df_measured[ind].notna().sum()
    prev = df_measured[ind].mean() * 100
    print(f"  {lab}: {prev:.1f}% (n={n:,})")

print("\nPrevalence by Region:")
print(region_prev.round(1).to_string())

print("\nPrevalence by Residence:")
print(residence_prev.round(1).to_string())

print("\nPrevalence by Wealth Index:")
print(wealth_prev.round(1).to_string())

print("\nPrevalence by Mother's Education:")
print(edu_prev.round(1).to_string())

print("\nPrevalence by Age:")
print(age_prev.round(1).to_string())