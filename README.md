# Census Building Permits Data - Six Major Metro Areas

Historical building permit data (2000-2024) for 1,061 places across six major U.S. metropolitan areas.

## Quick Start

### Main Dataset
```
historical_data/processed/six_metros_2000_2024_combined.csv
```
- 26,301 rows (place-years)
- 25 years (2000-2024)
- 1,061 unique places

### Metro Areas Covered
1. New York–Newark–Jersey City (552 places)
2. Los Angeles–Long Beach–Anaheim (124 places)
3. Washington–Arlington–Alexandria (44 places)
4. Boston–Cambridge–Newton (197 places)
5. San Francisco–Oakland–Fremont (64 places)
6. Seattle–Tacoma–Bellevue (80 places)

## Key Files

### Documentation
- **FINAL_RESULTS.md** - Complete project summary
- **DATA_DOCUMENTATION.md** - Data structure and field definitions
- **HISTORICAL_DATA_PLAN.md** - Collection methodology
- **PHASE_A_RESULTS.md** - Validation testing results

### Data
- `metro_subset/six_metros_2024.csv` - 2024 data only
- `historical_data/processed/six_metros_2000_2024_combined.csv` - Full 25-year dataset
- `historical_data/processed/six_metros_YYYY.csv` - Individual year files

### Scripts
- `download_all_years.sh` - Download Census data
- `extract_historical.py` - Extract and combine data
- `analyze_historical.py` - Generate summary statistics

## Data Fields

**Identifiers:**
- State Code, 6-Digit ID, Place Name, Year

**Permit Data (for each housing type):**
- 1-unit (single-family homes)
- 2-units (duplexes)
- 3-4 units (small multi-family)
- 5+ units (apartments)

**For each type:**
- Buildings, Units, Value (construction value in $)

## Quick Examples

### Find a specific town
```python
import pandas as pd
df = pd.read_csv('historical_data/processed/six_metros_2000_2024_combined.csv')

# Example: Find all records for a place
place_data = df[df['Name'].str.contains('Cambridge', case=False)]
print(place_data[['Year', 'Name', 'Units']])
```

### Annual permits by metro
```python
# Group by CBSA code and year
metro_totals = df.groupby(['Code.6', 'Year'])['Units'].sum()
```

## Data Quality

- **97.7%** of places have complete 25-year coverage
- **100%** place coverage from 2017-2024
- **98%+** place coverage for 2000-2016

## Source

U.S. Census Bureau, Building Permits Survey
- URL: https://www2.census.gov/econ/bps/Place/
- Collected: February 2026

## Project Status

✅ Complete - Ready for analysis!

See **FINAL_RESULTS.md** for detailed documentation.
