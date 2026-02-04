# Census Building Permits Survey - Data Documentation

## Data Source
- **Organization**: U.S. Census Bureau
- **Survey**: Building Permits Survey (BPS)
- **URL**: https://www2.census.gov/econ/bps/Place/
- **Data Level**: Place-level (cities/towns)
- **Latest Year Downloaded**: 2024

## Files Downloaded
- `so2024a.txt` - South Region (673 KB, 4,433 places)
- `ne2024a.txt` - Northeast Region (827 KB, 5,582 places)
- `mw2024a.txt` - Midwest Region (1.1 MB, 7,968 places)
- `we2024a.txt` - West Region (315 KB, 2,013 places)
- **Total**: ~19,993 places across the United States

## File Structure

### Header Format
The files use a two-row header:
- Row 1: Primary column names
- Row 2: Sub-column descriptions
- Row 3: Blank separator
- Rows 4+: Data

### Key Columns

#### Identification Columns
- `Survey Date` - Year of survey (e.g., 2024)
- `State Code` - 2-digit FIPS state code
- `6-Digit ID` - Unique place identifier
- `County Code` - County FIPS code
- `Census Place Code` - Census place code
- `FIPS Place Code` - FIPS place code
- `FIPS MCD Code` - FIPS Minor Civil Division code
- `Place Name` - Name of the city/town
- `Pop` - Population estimate
- `CSA Code` - Combined Statistical Area code
- `CBSA Code` - Core Based Statistical Area code
- `Central City` - Central city indicator
- `Zip Code` - Primary ZIP code
- `Region Code` - Census region (3=South, 1=Northeast, 2=Midwest, 4=West)
- `Division Code` - Census division code
- `Number of Months Rep` - Number of months reporting data

#### Permit Data Columns (repeated for each housing type)

For each category, there are 3 sub-columns: Buildings, Units, Value

**Categories:**
1. **1-unit** - Single-family homes
   - `Bldgs` - Number of buildings
   - `Units` - Number of units (same as buildings for 1-unit)
   - `Value` - Total construction value in dollars

2. **2-units** - Duplexes
   - Same structure as above

3. **3-4 units** - Small multi-family
   - Same structure as above

4. **5+ units** - Larger multi-family/apartments
   - Same structure as above

5. **1-unit rep** - Single-family (reported only)
   - Same structure, subset of 1-unit data

6. **2-units rep** - Duplexes (reported only)
   - Same structure, subset of 2-units data

7. **3-4 units rep** - Small multi-family (reported only)
   - Same structure, subset of 3-4 units data

8. **5+ units rep** - Larger multi-family (reported only)
   - Same structure, subset of 5+ units data

### Data Format
- **Delimiter**: Comma-separated values (CSV)
- **Encoding**: Text/ASCII
- **Missing Values**: Represented as 0 or blank
- **Numbers**: No thousands separators

## Data Quality Notes

### Reporting Coverage
- The `Number of Months Rep` column indicates how many months of data were reported
- 0 months = No permits or no reporting
- 12 months = Full year of data
- Values 1-11 = Partial year reporting

### Special Entries
- Some entries are "Unincorporated Area" for county-level aggregations
- Places with zero permits may indicate no construction or no reporting
- The "rep" columns show permits that were actively reported vs. estimated

## Example Data Row

```
2024,01,028000,081,0110,03076,00000,68343,194,12220,,1,36830,3,6,12,Auburn,863,863,234656234,24,48,4997483,0,0,0,1,113,14474191,863,863,234656234,24,48,4997483,0,0,0,1,113,14474191
```

This represents:
- **Place**: Auburn, Alabama
- **State Code**: 01 (Alabama)
- **Year**: 2024
- **Months Reported**: 12 (full year)
- **Total Permits**: 888 buildings, 1,024 units
  - 863 single-family homes ($234.7M)
  - 24 duplexes (48 units, $5.0M)
  - 0 3-4 unit buildings
  - 1 5+ unit building (113 units, $14.5M)

## Regional Coverage

### South Region (Region Code: 3)
- States: AL, AR, DE, DC, FL, GA, KY, LA, MD, MS, NC, OK, SC, TN, TX, VA, WV
- 4,433 places

### Northeast Region (Region Code: 1)
- States: CT, ME, MA, NH, NJ, NY, PA, RI, VT
- 5,582 places

### Midwest Region (Region Code: 2)
- States: IL, IN, IA, KS, MI, MN, MO, NE, ND, OH, SD, WI
- 7,968 places

### West Region (Region Code: 4)
- States: AK, AZ, CA, CO, HI, ID, MT, NV, NM, OR, UT, WA, WY
- 2,013 places

## Historical Data Availability
- Annual files available back to 1980 (so1980a.txt format)
- Monthly files available for more recent years
- Files updated annually (typically in April-May for previous year)

## Next Steps
See CLAUDE.MD for the analysis plan.
