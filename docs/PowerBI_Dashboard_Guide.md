# Canadian Mortgage Approvals Dashboard - Power BI Implementation Guide

## 📊 Dashboard Structure

### Page 1: Overview Dashboard
**Key Visuals:**
- **Card Visuals**: Total Applications, Total Approvals, Approval Rate, Total Value
- **Line Chart**: Monthly trend of applications and approvals (dual axis)
- **Donut Chart**: Approval vs Rejection breakdown
- **Column Chart**: Applications by Quarter
- **Slicer Filters**: Year, Province, Property Type

### Page 2: Regional Analysis
**Key Visuals:**
- **Map Visual**: Mortgage approvals by province (bubble size = volume)
- **Horizontal Bar Chart**: Top 10 provinces by approval volume
- **Table**: Province performance metrics (Applications, Approvals, Rate, Avg Value)
- **Treemap**: Approval value distribution by province
- **Slicer Filters**: Year, Property Type

### Page 3: Property Type Analysis
**Key Visuals:**
- **Stacked Column Chart**: Applications by Property Type over time
- **Clustered Bar Chart**: Approval rates by Property Type
- **Line Chart**: Average LTV ratio trends by Property Type
- **Pie Chart**: Market share by Property Type
- **Slicer Filters**: Year, Province

### Page 4: Insights & Trends
**Key Visuals:**
- **KPI Cards**: YoY growth metrics
- **Waterfall Chart**: Monthly change analysis
- **Scatter Plot**: LTV Ratio vs Approval Rate by Province
- **Table**: Monthly performance with conditional formatting
- **Text Box**: Key insights and recommendations

## 🔗 Data Model Relationships

\`\`\`
dim_date (1) -----> (*) mortgage_applications
dim_province (1) --> (*) mortgage_applications  
dim_property_type (1) -> (*) mortgage_applications
\`\`\`

## 📈 Essential DAX Measures

### Basic Metrics
```dax
Total Applications = COUNTROWS(mortgage_applications)
Total Approvals = SUMX(mortgage_applications, mortgage_applications[Is_Approved])
Approval Rate = DIVIDE([Total Approvals], [Total Applications], 0)
Total Mortgage Value = SUM(mortgage_applications[Mortgage_Value])
Total Approval Value = SUM(mortgage_applications[Approval_Value])
Average LTV = AVERAGE(mortgage_applications[LTV_Ratio])
