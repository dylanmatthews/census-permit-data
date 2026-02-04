#!/usr/bin/env python3
"""
Analyze the combined historical building permit dataset.
Generate summary statistics and validate data quality.
"""

import pandas as pd
import numpy as np

# Load the combined dataset
print("Loading combined dataset...")
df = pd.read_csv('historical_data/processed/six_metros_2000_2024_combined.csv', low_memory=False)

print(f"\n{'='*70}")
print("DATASET OVERVIEW")
print(f"{'='*70}")
print(f"Total rows: {len(df):,}")
print(f"Years: {df['Year'].min()}-{df['Year'].max()} ({df['Year'].nunique()} years)")
print(f"Unique places: {len(df.groupby(['Code', 'ID']))}")
print(f"Columns: {len(df.columns)}")

# Get place name column (varies by year)
name_col = 'Name' if 'Name' in df.columns else 'Place Name'

print(f"\n{'='*70}")
print("DATA BY YEAR")
print(f"{'='*70}")
year_summary = df.groupby('Year').agg({
    'Code': 'count',  # Number of places
}).rename(columns={'Code': 'Places'})

for year, row in year_summary.iterrows():
    pct = (row['Places'] / 1061) * 100
    print(f"{year}: {row['Places']:4d} places ({pct:5.1f}%)")

print(f"\n{'='*70}")
print("DATA BY METRO AREA (2024 snapshot)")
print(f"{'='*70}")

# Map CBSA codes to metro names
metro_names = {
    '35620': 'New York-Newark-Jersey City',
    '31080': 'Los Angeles-Long Beach-Anaheim',
    '47900': 'Washington-Arlington-Alexandria',
    '14460': 'Boston-Cambridge-Newton',
    '41860': 'San Francisco-Oakland-Fremont',
    '42660': 'Seattle-Tacoma-Bellevue'
}

# Get 2024 data
df_2024 = df[df['Year'] == 2024].copy()

# Try to find CBSA column
cbsa_cols = [col for col in df_2024.columns if 'CBSA' in col or 'Code.6' in col]
if cbsa_cols:
    cbsa_col = cbsa_cols[0]
    df_2024['CBSA_clean'] = df_2024[cbsa_col].astype(str).str.strip()

    for cbsa, name in metro_names.items():
        count = len(df_2024[df_2024['CBSA_clean'] == cbsa])
        print(f"{name:40s}: {count:4d} places")

# Sample places
print(f"\n{'='*70}")
print("SAMPLE PLACES (2024)")
print(f"{'='*70}")

sample_places = [
    ('Washington', '11', '1000'),
    ('New York', '36', '51000'),
    ('Los Angeles', '6', '44000'),
    ('Boston', '25', '7000'),
    ('San Francisco', '6', '67000'),
    ('Seattle', '53', '63000')
]

for place_name, state, place_id in sample_places:
    matches = df_2024[(df_2024['Code'].astype(str) == state) &
                       (df_2024['ID'].astype(str) == place_id)]
    if len(matches) > 0:
        print(f"✓ Found: {place_name}")
    else:
        print(f"✗ Missing: {place_name} (state={state}, id={place_id})")

# Data completeness
print(f"\n{'='*70}")
print("DATA COMPLETENESS")
print(f"{'='*70}")

# Count places with data for all 25 years
place_year_counts = df.groupby(['Code', 'ID']).size()
complete_places = (place_year_counts == 25).sum()
print(f"Places with all 25 years: {complete_places} ({(complete_places/1061)*100:.1f}%)")

# Years with missing data
incomplete_places = place_year_counts[place_year_counts < 25]
if len(incomplete_places) > 0:
    print(f"Places with incomplete data: {len(incomplete_places)}")
    print(f"Average years present: {place_year_counts.mean():.1f}")

print(f"\n{'='*70}")
print("SUMMARY SAVED")
print(f"{'='*70}")
print("Files created:")
print("  - historical_data/processed/six_metros_2000_2024_combined.csv")
print(f"  - Individual year files: six_metros_YYYY.csv (2000-2024)")
