# Six Major Metro Areas - Building Permits Data

## Overview
This directory contains filtered Census Building Permits Survey data for six major U.S. metropolitan areas for the year 2024.

## File
- `six_metros_2024.csv` - Combined data for all six metro areas (1,063 rows including 2-row header)

## Metro Areas Included

### 1. New York–Newark–Jersey City, NY-NJ MSA
- **CBSA Code**: 35620
- **Places Included**: 552
- **States**: NY, NJ

### 2. Los Angeles–Long Beach–Anaheim, CA MSA
- **CBSA Code**: 31080
- **Places Included**: 124
- **State**: CA

### 3. Washington–Arlington–Alexandria, DC-VA-MD-WV MSA
- **CBSA Code**: 47900
- **Places Included**: 44
- **States**: DC, VA, MD, WV

### 4. Boston–Cambridge–Newton, MA-NH MSA
- **CBSA Code**: 14460
- **Places Included**: 197
- **States**: MA, NH

### 5. San Francisco–Oakland–Fremont, CA MSA
- **CBSA Code**: 41860
- **Places Included**: 64
- **State**: CA

### 6. Seattle–Tacoma–Bellevue, WA MSA
- **CBSA Code**: 42660
- **Places Included**: 80
- **State**: WA

## Total Coverage
- **Total Places**: 1,061 places
- **Year**: 2024
- **Data Source**: Census Building Permits Survey

## File Structure
The CSV file maintains the same structure as the original regional files:
- 2-row header (primary columns + sub-columns)
- All original columns preserved
- Data rows for places within the six metro areas only

### Key Columns
- `Place Name` - Name of city/town
- `State Code` - 2-digit FIPS state code
- `CBSA Code` - Core Based Statistical Area code (used to filter metros)
- `1-unit Bldgs/Units/Value` - Single-family home permits
- `2-units Bldgs/Units/Value` - Duplex permits
- `3-4 units Bldgs/Units/Value` - Small multi-family permits
- `5+ units Bldgs/Units/Value` - Large multi-family/apartment permits
- `Number of Months Rep` - Months of data reported (0-12)

See `../DATA_DOCUMENTATION.md` for complete field descriptions.

## Usage Example
To look up permits for a specific place, search by place name. Note that some place names may appear in multiple metros (e.g., "Washington" appears in multiple states).

## Data Quality Notes
- Places with 0 in "Number of Months Rep" may not have reported data for 2024
- Some entries are "Unincorporated Area" representing county-level aggregations
- All permit counts and values are for calendar year 2024
