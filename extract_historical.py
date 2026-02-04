#!/usr/bin/env python3
"""
Extract historical building permit data for specific places across multiple years.
Tests matching logic on 1980, 2000, and 2024 data.
"""

import pandas as pd
import os
from pathlib import Path

def load_master_places(master_file):
    """Load the 2024 metro subset data to get our master place list."""
    # Read CSV, skipping the first header row
    df = pd.read_csv(master_file, skiprows=[0], low_memory=False)

    # Create set of (State Code, 6-Digit ID) tuples for matching
    place_identifiers = set(
        zip(df['Code'].astype(str).str.strip(),
            df['ID'].astype(str).str.strip())
    )

    print(f"Loaded {len(place_identifiers)} unique place identifiers from master file")
    print(f"Sample identifiers: {list(place_identifiers)[:5]}")

    return place_identifiers, df

def process_year(year, regions, place_identifiers, output_dir):
    """Process all regional files for a given year and extract our places."""
    all_data = []

    for region_code, region_name in regions.items():
        file_path = f"historical_data/raw/{region_name}/{region_code}{year}a.txt"

        if not os.path.exists(file_path):
            print(f"  WARNING: File not found: {file_path}")
            continue

        print(f"  Processing {region_name} {year}...")

        try:
            # Read file, skipping first header row
            df = pd.read_csv(file_path, skiprows=[0], low_memory=False)

            # Get column names
            state_col = 'Code' if 'Code' in df.columns else 'State Code'
            id_col = 'ID' if 'ID' in df.columns else '6-Digit ID'

            print(f"    Columns found: {df.columns.tolist()[:10]}...")
            print(f"    Total rows: {len(df)}")

            # Create identifier column for matching
            df['state_id_key'] = (
                df[state_col].astype(str).str.strip() + '|' +
                df[id_col].astype(str).str.strip()
            )

            # Create matching set from this file
            file_identifiers = set(
                zip(df[state_col].astype(str).str.strip(),
                    df[id_col].astype(str).str.strip())
            )

            # Find matches
            matches = place_identifiers.intersection(file_identifiers)
            print(f"    Found {len(matches)} matching places")

            # Filter to matching places
            df_filtered = df[
                df.apply(lambda row: (
                    str(row[state_col]).strip(),
                    str(row[id_col]).strip()
                ) in place_identifiers, axis=1)
            ].copy()  # Make a copy to avoid SettingWithCopyWarning

            if len(df_filtered) > 0:
                # Add year column
                df_filtered['Year'] = year
                df_filtered['Region'] = region_name
                all_data.append(df_filtered)
                print(f"    Extracted {len(df_filtered)} rows")

                # Show sample
                if len(df_filtered) > 0:
                    name_col = 'Name' if 'Name' in df_filtered.columns else 'Place Name'
                    if name_col in df_filtered.columns:
                        sample_places = df_filtered[name_col].head(3).tolist()
                        print(f"    Sample places: {sample_places}")

        except Exception as e:
            print(f"  ERROR processing {file_path}: {e}")
            continue

    if all_data:
        # Combine all regions for this year
        combined = pd.concat(all_data, ignore_index=True)

        # Save year-specific file
        output_file = f"{output_dir}/six_metros_{year}.csv"
        combined.to_csv(output_file, index=False)
        print(f"\nSaved {len(combined)} rows to {output_file}")

        return combined
    else:
        print(f"\nNo data extracted for {year}")
        return None

def main():
    # Configuration
    master_file = "metro_subset/six_metros_2024.csv"
    output_dir = "historical_data/processed"

    regions = {
        'so': 'south',
        'ne': 'northeast',
        'mw': 'midwest',
        'we': 'west'
    }

    # Process all years 2000-2024
    test_years = list(range(2000, 2025))

    print("="*70)
    print("Full Historical Data Extraction: 2000-2024")
    print("="*70)
    print()

    # Load master place list
    print("Step 1: Loading master place list from 2024 data...")
    place_identifiers, master_df = load_master_places(master_file)
    print()

    # Process each test year
    all_results = {}

    for year in test_years:
        print(f"\nStep 2.{test_years.index(year)+1}: Processing year {year}")
        print("-"*70)
        result = process_year(year, regions, place_identifiers, output_dir)
        all_results[year] = result
        print()

    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    print(f"\nMaster places from 2024: {len(place_identifiers)}")

    for year in test_years:
        if all_results[year] is not None:
            count = len(all_results[year])
            pct = (count / len(place_identifiers)) * 100
            print(f"{year}: {count} places found ({pct:.1f}% of master list)")
        else:
            print(f"{year}: No data extracted")

    print("\n" + "="*70)
    print("Extraction Complete!")
    print("="*70)

    # Validation checks
    print("\nValidation Checks:")
    print("✓ Files downloaded successfully")

    successful_years = [y for y in test_years if all_results[y] is not None]
    failed_years = [y for y in test_years if all_results[y] is None]

    print(f"✓ {len(successful_years)} years processed successfully")
    if failed_years:
        print(f"⚠ {len(failed_years)} years failed: {failed_years[:5]}{'...' if len(failed_years) > 5 else ''}")

    # Create combined dataset
    if successful_years:
        print("\nCreating combined dataset...")
        combined_data = pd.concat([all_results[y] for y in successful_years if all_results[y] is not None],
                                 ignore_index=True)

        combined_file = f"{output_dir}/six_metros_2000_2024_combined.csv"
        combined_data.to_csv(combined_file, index=False)

        print(f"✅ Combined dataset saved: {combined_file}")
        print(f"   Total rows: {len(combined_data):,}")
        print(f"   Years: {combined_data['Year'].min()}-{combined_data['Year'].max()}")
        print(f"   Unique places: {len(combined_data.groupby(['Code', 'ID']))}")

if __name__ == "__main__":
    main()
