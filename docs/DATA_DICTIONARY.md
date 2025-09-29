# 📊 Canadian Mortgage Approvals - Data Dictionary

## Overview
This data dictionary describes the structure and content of the Canadian Mortgage Approvals dataset used for Power BI dashboard analytics. The dataset consists of 5 related tables designed for dimensional modeling and business intelligence reporting.

## 📋 Table of Contents
- [Fact Tables](#fact-tables)
  - [mortgage_applications](#mortgage_applications)
  - [monthly_summary](#monthly_summary)
- [Dimension Tables](#dimension-tables)
  - [dim_date](#dim_date)
  - [dim_province](#dim_province)
  - [dim_property_type](#dim_property_type)
- [Data Relationships](#data-relationships)
- [Business Rules](#business-rules)

---

## Fact Tables

### mortgage_applications
**Purpose**: Main transactional table containing individual mortgage application records.

| Column Name | Data Type | Format | Description | Business Rules |
|-------------|-----------|--------|-------------|----------------|
| Application_ID | Integer | 1-50000 | Unique identifier for each mortgage application | Primary Key, Auto-increment |
| Application_Date | Date | YYYY-MM-DD | Date when mortgage application was submitted | Range: 2020-01-01 to 2024-12-31 |
| Province | String | 2-3 chars | Canadian province/territory code | Foreign Key to dim_province |
| Property_Type | String | Text | Type of property being mortgaged | Foreign Key to dim_property_type |
| Mortgage_Value | Decimal | Currency | Total mortgage amount requested (CAD) | Range: $100,000 - $2,000,000 |
| Property_Value | Decimal | Currency | Assessed value of the property (CAD) | Range: $150,000 - $3,000,000 |
| LTV_Ratio | Decimal | Percentage | Loan-to-Value ratio (Mortgage/Property * 100) | Calculated field, Range: 50-95% |
| Applicant_Income | Decimal | Currency | Annual gross income of primary applicant (CAD) | Range: $40,000 - $300,000 |
| Credit_Score | Integer | Score | Credit score of primary applicant | Range: 500-850 |
| Employment_Type | String | Text | Type of employment | Values: Full-time, Part-time, Self-employed, Contract |
| Down_Payment | Decimal | Currency | Down payment amount (CAD) | Calculated: Property_Value - Mortgage_Value |
| Approval_Status | String | Text | Final decision on mortgage application | Values: Approved, Rejected |
| Interest_Rate | Decimal | Percentage | Approved interest rate (if approved) | Range: 2.5-7.5%, NULL if rejected |
| Amortization_Years | Integer | Years | Mortgage amortization period | Values: 15, 20, 25, 30, NULL if rejected |

**Record Count**: ~50,000 applications  
**Time Period**: January 2020 - December 2024  
**Granularity**: One record per mortgage application

---

### monthly_summary
**Purpose**: Pre-aggregated monthly statistics for performance optimization in Power BI.

| Column Name | Data Type | Format | Description | Business Rules |
|-------------|-----------|--------|-------------|----------------|
| Year_Month | String | YYYY-MM | Year and month identifier | Format: "2024-01" |
| Province | String | 2-3 chars | Canadian province/territory code | Foreign Key to dim_province |
| Property_Type | String | Text | Type of property | Foreign Key to dim_property_type |
| Total_Applications | Integer | Count | Number of applications in the period | Aggregated from mortgage_applications |
| Approved_Applications | Integer | Count | Number of approved applications | Subset of Total_Applications |
| Approval_Rate | Decimal | Percentage | Approval rate for the period | Calculated: Approved/Total * 100 |
| Avg_Mortgage_Value | Decimal | Currency | Average mortgage amount (CAD) | Mean of approved applications |
| Avg_LTV_Ratio | Decimal | Percentage | Average loan-to-value ratio | Mean of all applications |
| Avg_Credit_Score | Integer | Score | Average credit score | Mean of all applications |

**Record Count**: ~3,000 monthly summaries  
**Time Period**: January 2020 - December 2024  
**Granularity**: One record per month/province/property type combination

---

## Dimension Tables

### dim_date
**Purpose**: Date dimension table for time-based analysis and filtering.

| Column Name | Data Type | Format | Description | Business Rules |
|-------------|-----------|--------|-------------|----------------|
| Application_Date | Date | YYYY-MM-DD | Calendar date | Primary Key, Range: 2020-2024 |
| Year | Integer | YYYY | Calendar year | Extracted from Application_Date |
| Month | Integer | 1-12 | Calendar month number | Extracted from Application_Date |
| Month_Name | String | Text | Full month name | Values: January, February, etc. |
| Quarter | Integer | 1-4 | Calendar quarter | Calculated from month |
| Quarter_Name | String | Text | Quarter label | Values: Q1, Q2, Q3, Q4 |
| Day_of_Week | Integer | 1-7 | Day of week number | 1=Sunday, 7=Saturday |
| Day_Name | String | Text | Full day name | Values: Sunday, Monday, etc. |
| Is_Weekend | Boolean | True/False | Weekend indicator | True for Saturday/Sunday |
| Is_Month_End | Boolean | True/False | Month end indicator | True for last day of month |
| Is_Quarter_End | Boolean | True/False | Quarter end indicator | True for last day of quarter |
| Is_Year_End | Boolean | True/False | Year end indicator | True for December 31st |

**Record Count**: ~1,826 dates (5 years)  
**Time Period**: January 1, 2020 - December 31, 2024  
**Granularity**: One record per calendar date

---

### dim_province
**Purpose**: Canadian provinces and territories lookup table.

| Column Name | Data Type | Format | Description | Business Rules |
|-------------|-----------|--------|-------------|----------------|
| Province | String | 2-3 chars | Province/territory code | Primary Key |
| Province_Name | String | Text | Full province/territory name | Official Canadian names |
| Region | String | Text | Geographic region | Values: Western, Central, Atlantic, Northern |
| Population | Integer | Count | Provincial population (2023 est.) | Statistics Canada data |
| Major_City | String | Text | Largest city in province | Primary economic center |

**Record Count**: 13 provinces/territories  
**Coverage**: All Canadian provinces and territories

**Province Codes**:
- ON (Ontario), QC (Quebec), BC (British Columbia)
- AB (Alberta), MB (Manitoba), SK (Saskatchewan)
- NS (Nova Scotia), NB (New Brunswick), NL (Newfoundland and Labrador)
- PE (Prince Edward Island), YT (Yukon), NT (Northwest Territories), NU (Nunavut)

---

### dim_property_type
**Purpose**: Property type classification lookup table.

| Column Name | Data Type | Format | Description | Business Rules |
|-------------|-----------|--------|-------------|----------------|
| Property_Type | String | Text | Property type identifier | Primary Key |
| Category | String | Text | High-level property category | Values: Residential, Commercial |
| Description | String | Text | Detailed property type description | Business definition |
| Typical_LTV_Max | Decimal | Percentage | Maximum typical LTV for property type | Industry standard |
| Risk_Level | String | Text | Risk assessment category | Values: Low, Medium, High |

**Record Count**: 3 property types  

**Property Types**:
- **Existing**: Previously owned residential properties
- **New**: Newly constructed residential properties  
- **New Residential Construction**: Properties under construction/pre-construction

---

## Data Relationships

### Primary Relationships
\`\`\`
mortgage_applications.Application_Date → dim_date.Application_Date (Many-to-One)
mortgage_applications.Province → dim_province.Province (Many-to-One)
mortgage_applications.Property_Type → dim_property_type.Property_Type (Many-to-One)

monthly_summary.Province → dim_province.Province (Many-to-One)
monthly_summary.Property_Type → dim_property_type.Property_Type (Many-to-One)
\`\`\`

### Relationship Cardinality
- **One-to-Many**: Each dimension record can relate to multiple fact records
- **Referential Integrity**: All foreign keys have corresponding dimension records
- **No Orphaned Records**: All fact table foreign keys are valid

---

## Business Rules

### Data Quality Standards
- **Completeness**: No NULL values in required fields
- **Accuracy**: All calculated fields verified against source formulas
- **Consistency**: Standardized formats across all tables
- **Timeliness**: Data represents applications from 2020-2024

### Calculation Rules
\`\`\`sql
LTV_Ratio = (Mortgage_Value / Property_Value) * 100
Down_Payment = Property_Value - Mortgage_Value
Approval_Rate = (Approved_Applications / Total_Applications) * 100
\`\`\`

### Business Constraints
- **LTV Ratio**: Maximum 95% (Canadian mortgage regulations)
- **Minimum Down Payment**: 5% for properties under $500K, 10% for $500K+
- **Credit Score**: Minimum 600 for approval consideration
- **Debt Service Ratios**: Implicit in approval decisions

### Data Validation Rules
- Property_Value > Mortgage_Value (positive down payment)
- LTV_Ratio between 50% and 95%
- Credit_Score between 500 and 850
- Interest_Rate only populated for approved applications
- Application_Date within valid business date range

---

## Usage Notes

### Power BI Implementation
- Use dim_date as the primary date table
- Create relationships in Power BI model view
- Mark dim_date as date table for time intelligence
- Use monthly_summary for performance-optimized visuals

### Performance Considerations
- Index on Application_Date for time-based queries
- Use monthly_summary for aggregate visualizations
- Implement proper star schema relationships
- Consider partitioning by year for large datasets

### Data Refresh Strategy
- Full refresh recommended for dimension tables
- Incremental refresh possible for fact tables by Application_Date
- Monthly_summary should be recalculated after fact table updates

---

## Contact & Support
For questions about this data dictionary or the underlying dataset, please refer to the project documentation or create an issue in the repository.

**Last Updated**: December 2024  
**Version**: 1.0  
**Data Source**: Synthetic Canadian mortgage application data for analytics purposes
