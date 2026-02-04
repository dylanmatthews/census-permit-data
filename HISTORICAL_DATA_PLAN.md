# Historical Data Collection Plan (1980-2024)
## Building Permits for 1,061 Places in Six Major Metro Areas

## Executive Summary
This plan outlines the strategy for collecting 45 years of historical building permit data (1980-2024) for the 1,061 places identified in six major U.S. metropolitan areas.

**Estimated Data Volume:**
- 45 years × 4 regions = 180 files
- ~500-700 KB per file = ~90-125 MB total download
- Processing time: ~2-4 hours (download + processing)

## Phase 1: Data Discovery & Download Strategy

### 1.1 Download All Historical Annual Files (1980-2024)
**For each region (South, Northeast, Midwest, West):**
- Download all annual files: `{region}1980a.txt` through `{region}2024a.txt`
- Total: 180 files (45 years × 4 regions)

**Download Strategy:**
```bash
# Batch download all years for all regions
for region in so ne mw we; do
  for year in {1980..2024}; do
    curl -o ${region}${year}a.txt \
      "https://www2.census.gov/econ/bps/Place/{REGION}%20Region/${region}${year}a.txt"
  done
done
```

**Storage Organization:**
```
historical_data/
├── raw/
│   ├── south/
│   │   ├── so1980a.txt
│   │   ├── so1981a.txt
│   │   └── ... (through so2024a.txt)
│   ├── northeast/
│   ├── midwest/
│   └── west/
└── processed/
    └── six_metros_1980_2024.csv
```

## Phase 2: Data Structure Analysis

### 2.1 Key Structural Changes Over Time

**Era 1: 1980-1999 (Early Format)**
- Columns: Survey Date, State Code, 6-Digit ID, County, MSA/CMSA, PMSA
- MSA/CMSA codes used instead of CBSA codes
- Place names with dots/formatting: "ABBEVILLE. . . . . . . . . . . . ."
- Fewer metadata columns

**Era 2: 2000-2009 (Transition Format)**
- Added: Place Code, Central City indicator, Zip Code
- Still using MSA/CMSA codes (transitioning to CBSA)
- Cleaner place names
- More standardized formatting

**Era 3: 2010-2024 (Modern Format)**
- Added: Census Place Code, FIPS Place Code, FIPS MCD Code, Population
- **CBSA codes introduced** (replaced MSA/CMSA)
- CSA codes added
- Footnote codes added
- Current format we're working with

### 2.2 Critical Challenge: Metro Area Definition Changes

**The MSA/CMSA to CBSA Transition:**
- Pre-2000s: Metropolitan areas identified by MSA (Metropolitan Statistical Area) or CMSA (Consolidated MSA)
- 2003+: OMB transitioned to CBSA (Core Based Statistical Area) system
- **Problem**: A place's metro assignment may have changed between systems

**Our Six Target Metros - Historical Codes:**

1. **New York–Newark–Jersey City**
   - Modern CBSA: 35620
   - Historical: Need to map to MSA/CMSA codes

2. **Los Angeles–Long Beach–Anaheim**
   - Modern CBSA: 31080
   - Historical: MSA 4480 (Los Angeles-Long Beach)

3. **Washington–Arlington–Alexandria**
   - Modern CBSA: 47900
   - Historical: MSA 8840 (Washington DC-MD-VA-WV)

4. **Boston–Cambridge–Newton**
   - Modern CBSA: 14460
   - Historical: CMSA 1120 (Boston-Worcester-Lawrence)

5. **San Francisco–Oakland–Fremont**
   - Modern CBSA: 41860
   - Historical: CMSA 7360 (San Francisco-Oakland-San Jose)

6. **Seattle–Tacoma–Bellevue**
   - Modern CBSA: 42660
   - Historical: CMSA 7600 (Seattle-Tacoma-Bremerton)

## Phase 3: Place Matching Strategy

### 3.1 Two-Pronged Matching Approach

**Approach A: Geographic Identifier Matching (Most Reliable)**
Use consistent place identifiers that span the entire time period:
- **State Code** (column 2) - Unchanged since 1980
- **6-Digit ID** (column 3) - Appears to be consistent across years
- **County Code** (column 4) - Generally stable

**Matching Logic:**
1. Create master list from 2024 data: State Code + 6-Digit ID for all 1,061 places
2. For each historical year, extract rows matching these identifiers
3. This should capture places regardless of metro definition changes

**Approach B: Metro Area Code Matching (Fallback/Verification)**
For years 2010+:
- Filter by CBSA codes (35620, 31080, 47900, 14460, 41860, 42660)

For years 2000-2009:
- Research MSA/CMSA codes for our six metros
- Filter by those codes

For years 1980-1999:
- Research MSA codes for our six metros
- Filter by those codes
- May need to handle place name matching due to formatting differences

### 3.2 Recommended Approach: Hybrid

**Step 1: Use 2024 as Master Reference**
- Extract unique (State Code, 6-Digit ID, Place Name) combinations from `six_metros_2024.csv`
- This gives us 1,061 places with known identifiers

**Step 2: Match Across All Years**
- For each historical file (1980-2023), extract rows where:
  - State Code AND 6-Digit ID match our master list
- This ensures we track the same places over time, regardless of metro definition changes

**Step 3: Verify with Metro Codes (Where Available)**
- Cross-check 2010-2024 matches against CBSA codes
- Research and verify 1980-2009 matches against MSA/CMSA codes

## Phase 4: Data Processing Pipeline

### 4.1 Extraction Script

```python
import pandas as pd
import glob

# Load master place list from 2024 data
master_places = pd.read_csv('metro_subset/six_metros_2024.csv',
                            skiprows=[0], # Skip first header row
                            low_memory=False)

# Create identifier set: (State Code, 6-Digit ID)
place_identifiers = set(
    zip(master_places['State Code'], master_places['6-Digit ID'])
)

# Process each historical file
all_years_data = []

for year in range(1980, 2025):
    for region in ['so', 'ne', 'mw', 'we']:
        file = f'historical_data/raw/{region}/{region}{year}a.txt'

        # Read with appropriate header handling
        if year < 2000:
            # Handle older format
            df = pd.read_csv(file, skiprows=[0], low_memory=False)
        else:
            df = pd.read_csv(file, skiprows=[0], low_memory=False)

        # Filter to our places
        df_filtered = df[
            df.apply(lambda row: (row['State Code'], row['6-Digit ID'])
                    in place_identifiers, axis=1)
        ]

        # Add year column
        df_filtered['Year'] = year

        all_years_data.append(df_filtered)

# Combine all years
historical_data = pd.concat(all_years_data, ignore_index=True)

# Save combined dataset
historical_data.to_csv('historical_data/processed/six_metros_1980_2024.csv',
                       index=False)
```

### 4.2 Data Quality Checks

**After Processing:**
1. Verify place counts per year (should be ≤1,061 for each year)
2. Check for missing years for each place
3. Identify places that may not have existed in earlier years
4. Flag places with 0 months reporting

## Phase 5: Expected Challenges & Solutions

### Challenge 1: Places That Didn't Exist in 1980
**Issue**: Some places may have been incorporated after 1980
**Solution**: Accept that some places will have incomplete time series
**Action**: Document first appearance year for each place

### Challenge 2: Column Structure Variations
**Issue**: Different column names/orders across eras
**Solution**: Standardize columns after loading each file
**Action**: Create column mapping dictionary for each era

### Challenge 3: Metro Boundary Changes
**Issue**: Places may have been added/removed from metro definitions over time
**Solution**: Use geographic identifiers rather than metro codes
**Action**: Document which approach was used for which years

### Challenge 4: Missing Data
**Issue**: Some places may not have reported in certain years
**Solution**: Keep rows with 0 permits to distinguish from non-reporting
**Action**: Flag rows where "Number of Months Rep" = 0

### Challenge 5: File Download Failures
**Issue**: Network errors, missing files, server issues
**Solution**: Implement retry logic and progress tracking
**Action**: Log successful/failed downloads, resume capability

## Phase 6: Output Format

### 6.1 Final Dataset Structure

**Columns (Standardized Across All Years):**
- Year
- State Code
- 6-Digit ID
- County Code
- Place Name
- Metro Area (CBSA/MSA/CMSA as available)
- Number of Months Reported
- 1-unit Buildings, Units, Value
- 2-units Buildings, Units, Value
- 3-4 units Buildings, Units, Value
- 5+ units Buildings, Units, Value
- Total Buildings, Total Units, Total Value (calculated)

**Additional Metadata Columns (where available):**
- Population
- ZIP Code
- FIPS Place Code
- Central City indicator

### 6.2 Summary Tables

**Create supporting files:**
1. `place_summary.csv` - One row per place with:
   - Place identifiers
   - First year of data
   - Last year of data
   - Years with data
   - Total permits 1980-2024

2. `annual_summary.csv` - One row per year with:
   - Year
   - Total places reporting
   - Total permits issued
   - Breakdown by housing type

## Phase 7: Implementation Timeline

### Estimated Effort
1. **Download all files** (~180 files): 30-60 minutes
2. **Write extraction script**: 2-3 hours
3. **Process all files**: 1-2 hours
4. **Quality checks & validation**: 1-2 hours
5. **Documentation**: 1 hour

**Total: 5-8 hours of work**

### Phased Rollout
**Phase A (Quick Validation):**
- Download 3 sample years: 1980, 2000, 2024
- Test matching logic
- Verify approach works
- Estimated: 1 hour

**Phase B (Full Download):**
- Download all 180 files
- Organize into directory structure
- Estimated: 1 hour

**Phase C (Processing):**
- Run extraction script
- Generate combined dataset
- Estimated: 3-4 hours

**Phase D (Validation & Documentation):**
- Quality checks
- Create summary tables
- Document findings
- Estimated: 2-3 hours

## Phase 8: Success Metrics

### How We'll Know It Worked
1. **Completeness**: ~1,061 places × 45 years = ~47,745 place-years (allowing for missing data)
2. **Consistency**: Each place appears with consistent identifiers across years
3. **Accuracy**: Spot-check known cities show expected permit trends
4. **Quality**: < 5% of rows with data quality flags

### Validation Tests
1. Check that major cities (NYC, LA, DC, Boston, SF, Seattle) appear in all 45 years
2. Verify permit counts match known historical patterns (e.g., housing boom/bust cycles)
3. Ensure total permits across six metros show expected trends
4. Confirm no duplicate place-year combinations

## Phase 9: Alternative Approaches

### If Geographic Matching Fails
**Fallback Option**: Download ALL places for all years, then filter
- More data to process (~20,000 places × 45 years)
- But guarantees we don't miss places due to identifier changes
- Can always subset later

### If Historical Metro Codes Are Unknown
**Research Plan**:
1. Check Census documentation for MSA/CMSA to CBSA crosswalks
2. Use NBER data files (they maintain historical metro code mappings)
3. Contact Census Bureau for guidance
4. Worst case: Accept 2010-2024 data only (15 years instead of 45)

## Next Steps

1. **Immediate**: Run Phase A validation with 3 sample years
2. **If successful**: Proceed with full download (Phase B)
3. **Then**: Implement processing pipeline (Phase C)
4. **Finally**: Generate final datasets and documentation (Phase D)

## Notes
- This plan assumes geographic identifiers (State + 6-Digit ID) are stable over time
- Validation with sample years will confirm this assumption
- Flexibility to adjust approach based on what we learn
- Focus on getting "good enough" historical data rather than perfect completeness
