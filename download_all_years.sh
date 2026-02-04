#!/bin/bash
# Download all annual building permit data files for 2000-2024
# Total: 25 years × 4 regions = 100 files

set -e  # Exit on error

BASE_URL="https://www2.census.gov/econ/bps/Place"
OUTPUT_DIR="historical_data/raw"

# Function to get region name
get_region() {
    case $1 in
        so) echo "South Region" ;;
        ne) echo "Northeast Region" ;;
        mw) echo "Midwest Region" ;;
        we) echo "West Region" ;;
    esac
}

# Function to get output directory
get_output_dir() {
    case $1 in
        so) echo "south" ;;
        ne) echo "northeast" ;;
        mw) echo "midwest" ;;
        we) echo "west" ;;
    esac
}

echo "========================================================================"
echo "Phase B: Downloading Historical Data (2000-2024)"
echo "========================================================================"
echo ""
echo "Years: 2000-2024 (25 years)"
echo "Regions: 4 (South, Northeast, Midwest, West)"
echo "Total files: 100"
echo ""

total_files=0
success_count=0
failed_files=""

# Loop through years and regions
for year in {2000..2024}; do
    echo "Downloading year $year..."

    for code in so ne mw we; do
        region=$(get_region $code)
        output_subdir=$(get_output_dir $code)
        filename="${code}${year}a.txt"
        url="${BASE_URL}/${region}/${filename}"
        output_path="${OUTPUT_DIR}/${output_subdir}/${filename}"

        # Skip if already exists
        if [ -f "$output_path" ]; then
            echo "  ✓ ${filename} (already exists)"
            ((success_count++))
            ((total_files++))
            continue
        fi

        # Download with retry (encode spaces in URL)
        encoded_url=$(echo "$url" | sed 's/ /%20/g')
        if curl -s -o "$output_path" "$encoded_url" && [ -s "$output_path" ]; then
            file_size=$(ls -lh "$output_path" | awk '{print $5}')
            echo "  ✓ ${filename} (${file_size})"
            ((success_count++))
        else
            echo "  ✗ ${filename} (FAILED)"
            failed_files="${failed_files}\n  - ${filename}"
        fi

        ((total_files++))

        # Small delay to be nice to Census servers
        sleep 0.2
    done

    echo ""
done

echo "========================================================================"
echo "Download Summary"
echo "========================================================================"
echo "Total files: ${total_files}"
echo "Successful: ${success_count}"
echo "Failed: $((total_files - success_count))"

if [ -n "$failed_files" ]; then
    echo ""
    echo "Failed files:"
    echo -e "$failed_files"
    exit 1
else
    echo ""
    echo "✅ All files downloaded successfully!"
    echo ""
    echo "Next step: Run extract_historical.py to process all years"
fi
