# Census Building Permits Survey - Place-Level Data Analysis

## Project Overview
Download and analyze place-level housing permit data from the Census Bureau's Building Permits Survey to enable lookup of annual housing permits issued by individual US towns/cities.

## Data Source
- **URL**: https://www2.census.gov/econ/bps/Place/
- **Format**: Appears to be FTP-accessible directory structure
- **Scope**: Place-level (city/town) building permit data

## Implementation Plan

### Phase 1: Data Discovery & Download
1. **Explore the directory structure**
   - Access the Census FTP directory to understand the organization
   - Identify the most recent data files available
   - Document file naming conventions and formats
   - Determine what years of data are available

2. **Download the data**
   - Fetch the most recent place-level permit data files
   - Store locally for analysis
   - Document data vintage and update frequency

### Phase 2: Data Processing
1. **Parse and structure the data**
   - Load data into analyzable format (likely CSV or similar)
   - Understand the schema and fields available
   - Identify key columns: place name, state, year, permit counts
   - Handle any data quality issues (missing values, formatting)

2. **Create lookup capability**
   - Build an index or search function by place name
   - Handle ambiguous place names (multiple cities with same name in different states)
   - Aggregate data by year for annual totals

### Phase 3: Analysis & Reporting
1. **Build query interface**
   - Create function to lookup permits by place name (and optionally state)
   - Return annual permit counts
   - Format results for easy interpretation

2. **Add analytical features** (optional enhancements)
   - Historical trends for a given place
   - Comparison across multiple places
   - Summary statistics (totals, averages, etc.)

## Expected Deliverables
- Downloaded Census permit data files
- Data processing scripts/code
- Lookup function to query permits by place name
- Documentation of data structure and any limitations

## Technical Considerations
- Handle FTP/HTTP access to Census servers
- Parse potentially large datasets efficiently
- Account for place name variations and duplicates across states
- Consider data update schedule for future refreshes
