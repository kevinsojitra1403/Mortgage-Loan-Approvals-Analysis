# Canadian Mortgage Dashboard - Script Instructions

## Prerequisites
- Python 3.7 or higher
- Install required packages:
\`\`\`bash
pip install pandas numpy datetime
\`\`\`

## Running the Scripts

### Generate Power BI Data (Recommended)
\`\`\`bash
python scripts/run_powerbi_export.py
\`\`\`

This creates 5 CSV files in the `csv/` folder:
- `mortgage_applications.csv` - Main dataset (~10,000 records)
- `dim_date.csv` - Date dimension table
- `dim_province.csv` - Province lookup table  
- `dim_property_type.csv` - Property type lookup table
- `monthly_summary.csv` - Monthly aggregated data

### Alternative: Full Processing Pipeline
\`\`\`bash
python scripts/mortgage_pipeline_simple.py
\`\`\`

### Individual Scripts (Optional)
\`\`\`bash
python scripts/mortgage_data_processor.py
python scripts/data_quality_report.py
python scripts/powerbi_data_export.py
\`\`\`

## Next Steps
1. Run the script above
2. Import the CSV files from `csv/` folder into Power BI Desktop
3. Follow the `PowerBI_Dashboard_Guide.md` for dashboard creation
