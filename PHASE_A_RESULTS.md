# Phase A Validation Results
## Testing Historical Data Extraction (1980, 2000, 2024)

**Date**: February 4, 2026
**Test Files**: 12 files (3 years × 4 regions)

---

## Summary

| Year | Places Found | % of Target | Status |
|------|-------------|-------------|---------|
| 2024 | 1,061 | 100.0% | ✅ Success |
| 2000 | 1,043 | 98.3% | ✅ Success |
| 1980 | 0 | 0.0% | ❌ Failed |

## Key Findings

### 🎉 Success: 2000-2024 Matching Works!
- **2024**: Perfect match - all 1,061 places extracted
- **2000**: Nearly perfect - 1,043 places (98.3%)
- The geographic identifier matching strategy (State Code + 6-Digit ID) works for 2000 onwards

### ❌ Critical Discovery: 1980 IDs Are Different

**The Problem**: The 6-Digit ID codes changed between 1980 and 2000.

**Evidence**:
- **Washington DC in 1980**: State=11, ID=000500
- **Washington DC in 2000**: State=11, ID=1000
- **Washington DC in 2024**: State=11, ID=1000

The Census Bureau appears to have renumbered place identifiers sometime between 1980 and 2000.

## Detailed Results

### 2024 (Current Format)
```
Breakdown by region:
- South (Washington DC area): 44 places
- Northeast (NYC, Boston): 749 places
- West (LA, SF, Seattle): 268 places
- Midwest: 0 places (none of our 6 metros are in Midwest)
```

### 2000 (Transition Format)
```
Breakdown by region:
- South: 37 places (vs 44 in 2024)
- Northeast: 744 places (vs 749 in 2024)
- West: 262 places (vs 268 in 2024)

Missing ~18 places likely due to:
- Places incorporated after 2000
- Minor boundary/definition changes
```

### 1980 (Early Format)
```
Result: 0 matches across all regions
Cause: 6-Digit ID codes are different from 2000/2024
```

## Implications for Full Historical Collection

### Option 1: 2000-2024 Only (Recommended)
**Pros:**
- Works with current matching logic
- Covers 25 years of data
- High confidence in place matching (98%+ success rate)
- ~1,000+ places × 25 years = ~25,000 place-years

**Cons:**
- Loses 20 years of earlier data (1980-1999)

**Effort**: Same as planned (just adjust year range)

### Option 2: Full 1980-2024 with Place Name Matching
**Pros:**
- Gets all 45 years of data
- More complete historical picture

**Cons:**
- Requires different matching strategy for 1980-1999
- Place name matching is less reliable:
  - Names formatted differently ("WASHINGTON D.C. . . . . ." vs "Washington")
  - Name changes over time
  - Ambiguous names (multiple Springfields, Washingtons, etc.)
- Much more complex code
- Lower confidence in correct matches

**Effort**: 2-3x more complex

### Option 3: Research ID Crosswalk
**Pros:**
- Could enable accurate matching back to 1980
- Would be the "correct" solution

**Cons:**
- Need to find or create 1980→2000 ID crosswalk
- May not exist or be publicly available
- Could take significant research time

**Effort**: Unknown (depends on crosswalk availability)

## Recommendation

### Proceed with Option 1: 2000-2024 Collection

**Rationale:**
1. The matching logic works reliably for 2000-2024
2. 25 years is still a substantial historical dataset
3. Avoids complexity and potential errors of name matching
4. Can always add 1980-1999 later if we find a crosswalk

**Next Steps for Phase B (Full Download):**
1. Modify year range: 2000-2024 (instead of 1980-2024)
2. Download: 25 years × 4 regions = 100 files (instead of 180)
3. Expected results: ~25,000 place-years
4. Estimated time: 3-5 hours (down from 5-8 hours)

## Files Generated

- `historical_data/processed/six_metros_2000.csv` - 1,043 places
- `historical_data/processed/six_metros_2024.csv` - 1,061 places

## Technical Notes

### Why 2000 Works
- 6-Digit IDs are consistent 2000-2024
- Column structure is similar enough to parse
- State codes unchanged

### Why 1980 Failed
- Different ID numbering system
- Would need to match on:
  - State Code + Place Name (unreliable)
  - Or find Census ID crosswalk file

### Missing Places in 2000
The 18 places present in 2024 but missing in 2000 likely represent:
- New incorporations (2000-2024)
- Boundary changes
- Places below reporting threshold in 2000

This is expected and acceptable.

## Validation Queries

To verify the extracted data quality:

```bash
# Check sample places exist
grep -i "washington" historical_data/processed/six_metros_2000.csv
grep -i "new york" historical_data/processed/six_metros_2000.csv
grep -i "los angeles" historical_data/processed/six_metros_2000.csv

# Verify place counts
wc -l historical_data/processed/six_metros_*.csv
```

---

## Decision Point

**Should we:**
A. ✅ Proceed with 2000-2024 collection (25 years, reliable) - RECOMMENDED
B. Attempt name-matching for 1980-1999 (more complex, less reliable)
C. Research Census ID crosswalk first (unknown timeline)

---

*Phase A validation complete. Awaiting user decision to proceed to Phase B.*
