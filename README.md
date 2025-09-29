# Canadian Mortgage Loan Approvals Analytics

A comprehensive data analytics solution for Canadian mortgage loan approvals, featuring automated data processing, quality validation, and Power BI dashboard integration.

## 🎯 Project Overview

This project provides a complete end-to-end solution for analyzing Canadian mortgage loan approval data. It includes data generation, cleaning, validation, and preparation for business intelligence dashboards in Power BI.

### Key Features

- **Automated Data Processing**: Generate realistic Canadian mortgage application datasets
- **Data Quality Validation**: Comprehensive data quality reports and validation
- **Power BI Integration**: Pre-configured data exports optimized for Power BI
- **Multi-dimensional Analysis**: Regional, temporal, and property type analytics
- **Professional Documentation**: Complete data dictionary and implementation guides

## 📊 Dashboard Capabilities

The solution supports four main analytical views:

1. **Overview Dashboard**: KPIs, trends, and executive summary metrics
2. **Regional Analysis**: Provincial performance, heatmaps, and geographic insights
3. **Property Type Analysis**: Comparative analysis across property categories
4. **Insights & Actions**: Anomaly detection and business recommendations

## 🗂️ Project Structure

\`\`\`
├── csv/                          # Generated CSV files for Power BI
│   ├── mortgage_applications.csv # Main dataset
│   ├── dim_date.csv              # Date dimension
│   ├── dim_province.csv          # Province lookup
│   ├── dim_property_type.csv     # Property type lookup
│   └── monthly_summary.csv       # Pre-aggregated monthly data
├── scripts/                      # Data processing scripts
│   ├── mortgage_data_processor.py    # Core data processing
│   ├── data_quality_report.py       # Data validation
│   ├── powerbi_data_export.py       # Power BI export utility
│   └── run_powerbi_export.py        # Main execution script
├── PowerBI_Dashboard_Guide.md    # Power BI implementation guide
├── DATA_DICTIONARY.md           # Complete data documentation
└── README.md                    # This file
\`\`\`

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Required Python packages: `pandas`, `numpy`, `datetime`

### Installation

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd mortgage-analytics
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   pip install pandas numpy
   \`\`\`

3. **Generate the dataset**
   \`\`\`bash
   python scripts/run_powerbi_export.py
   \`\`\`

### Alternative Execution Methods

**Option 1: Direct Script Execution**
\`\`\`bash
python scripts/powerbi_data_export.py
\`\`\`

**Option 2: Individual Components**
\`\`\`bash
python scripts/mortgage_data_processor.py
python scripts/data_quality_report.py
\`\`\`

## 📈 Power BI Integration

### Data Import Process

1. **Open Power BI Desktop**
2. **Import CSV Files**:
   - Go to `Get Data` > `Text/CSV`
   - Import all files from the `csv/` folder
3. **Configure Relationships**:
   - Link tables using the provided relationship guide
   - Set up date table and hierarchies

### Dashboard Implementation

Follow the comprehensive guide in `PowerBI_Dashboard_Guide.md` which includes:

- **Data Model Setup**: Relationships and hierarchies
- **DAX Measures**: 50+ pre-built calculations
- **Visual Specifications**: Detailed layout and formatting
- **Implementation Steps**: Step-by-step dashboard creation

### Key DAX Measures Included

```dax
Total Applications = COUNTROWS(mortgage_applications)
Approval Rate = DIVIDE([Approved Applications], [Total Applications], 0)
Average Mortgage Value = AVERAGE(mortgage_applications[Mortgage_Value])
Applications YoY = [Total Applications] - CALCULATE([Total Applications], SAMEPERIODLASTYEAR(dim_date[Application_Date]))
