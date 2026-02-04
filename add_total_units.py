#!/usr/bin/env python3
"""
Add a 'Total_Units' column to the combined dataset.
Sums: 1-unit units + 2-unit units + 3-4 unit units + 5+ unit units
"""

import pandas as pd
import numpy as np

# Load the combined dataset
print("Loading combined dataset...")
df = pd.read_csv('historical_data/processed/six_metros_2000_2024_combined.csv', low_memory=False)

print(f"Loaded {len(df):,} rows")
print(f"\nCurrent columns ({len(df.columns)} total):")
print(df.columns.tolist()[:20])

# Identify the unit columns
# Looking at the data structure:
# - Column 'Units' = 1-unit units
# - Column 'Units.1' = 2-unit units
# - Column 'Units.2' = 3-4 unit units
# - Column 'Units.3' = 5+ unit units

unit_columns = ['Units', 'Units.1', 'Units.2', 'Units.3']

# Verify columns exist
for col in unit_columns:
    if col not in df.columns:
        print(f"WARNING: Column '{col}' not found!")
    else:
        print(f"Found column: {col}")

# Convert to numeric, handling any non-numeric values
print("\nConverting columns to numeric...")
for col in unit_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Calculate total units
print("\nCalculating Total_Units...")
df['Total_Units'] = df[unit_columns].sum(axis=1, skipna=True)

# Show some statistics
print(f"\nTotal_Units statistics:")
print(f"  Mean: {df['Total_Units'].mean():.1f} units")
print(f"  Median: {df['Total_Units'].median():.1f} units")
print(f"  Max: {df['Total_Units'].max():.0f} units")
print(f"  Rows with 0 units: {(df['Total_Units'] == 0).sum():,} ({(df['Total_Units'] == 0).sum()/len(df)*100:.1f}%)")

# Show a few examples
print("\nSample records with Total_Units:")
sample = df[df['Total_Units'] > 0][['Year', 'Name', 'Units', 'Units.1', 'Units.2', 'Units.3', 'Total_Units']].head(10)
print(sample.to_string())

# Save updated dataset
output_file = 'historical_data/processed/six_metros_2000_2024_combined.csv'
print(f"\nSaving updated dataset to {output_file}...")
df.to_csv(output_file, index=False)

print("✅ Done! Total_Units column added.")
print(f"\nNew column count: {len(df.columns)}")
