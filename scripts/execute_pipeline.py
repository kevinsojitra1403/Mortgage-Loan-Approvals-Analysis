import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("🏠 Canadian Mortgage Loan Approvals Dashboard - Data Processing Pipeline")
print("=" * 70)

# Set random seed for reproducible results
np.random.seed(42)

class MortgageDataProcessor:
    def __init__(self):
        self.cleaned_data = None
        self.metadata = None
        
    def generate_sample_data(self, n_records=10000):
        """Generate realistic Canadian mortgage data for testing"""
        print("📊 Generating sample mortgage data...")
        
        # Canadian provinces and territories
        provinces = ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'YT', 'NT', 'NU']
        property_types = ['Single Family', 'Condo', 'Townhouse', 'Multi-Family', 'Mobile Home']
        loan_purposes = ['Purchase', 'Refinance', 'Home Improvement', 'Debt Consolidation']
        
        # Generate date range (last 3 years)
        start_date = datetime.now() - timedelta(days=3*365)
        dates = [start_date + timedelta(days=x) for x in range(0, 3*365, 3)]
        
        data = []
        for i in range(n_records):
            # Generate realistic mortgage data
            loan_amount = np.random.normal(400000, 150000)  # Average Canadian mortgage
            loan_amount = max(100000, min(2000000, loan_amount))  # Reasonable bounds
            
            property_value = loan_amount / np.random.uniform(0.6, 0.95)  # LTV ratio
            
            record = {
                'Application_ID': f'APP{i+1:06d}',
                'Application_Date': np.random.choice(dates).strftime('%Y-%m-%d'),
                'Province': np.random.choice(provinces),
                'Property_Type': np.random.choice(property_types),
                'Loan_Amount': round(loan_amount, 2),
                'Property_Value': round(property_value, 2),
                'Loan_Purpose': np.random.choice(loan_purposes),
                'Credit_Score': int(np.random.normal(720, 80)),
                'Income': round(np.random.normal(85000, 30000), 2),
                'Debt_to_Income': round(np.random.uniform(0.1, 0.45), 3),
                'Interest_Rate': round(np.random.uniform(2.5, 6.5), 3),
                'Approval_Status': np.random.choice(['Approved', 'Denied', 'Pending'], p=[0.7, 0.2, 0.1])
            }
            
            # Add some missing values randomly (5% chance)
            if np.random.random() < 0.05:
                missing_field = np.random.choice(['Credit_Score', 'Income', 'Debt_to_Income'])
                record[missing_field] = None
                
            data.append(record)
        
        df = pd.DataFrame(data)
        print(f"✅ Generated {len(df)} mortgage records")
        return df
    
    def clean_data(self, df):
        """Clean and standardize the mortgage data"""
        print("🧹 Cleaning and standardizing data...")
        
        cleaned_df = df.copy()
        
        # Convert date columns
        cleaned_df['Application_Date'] = pd.to_datetime(cleaned_df['Application_Date'])
        
        # Handle missing values
        if 'Credit_Score' in cleaned_df.columns:
            cleaned_df['Credit_Score'].fillna(cleaned_df['Credit_Score'].median(), inplace=True)
        if 'Income' in cleaned_df.columns:
            cleaned_df['Income'].fillna(cleaned_df['Income'].median(), inplace=True)
        if 'Debt_to_Income' in cleaned_df.columns:
            cleaned_df['Debt_to_Income'].fillna(cleaned_df['Debt_to_Income'].median(), inplace=True)
        
        # Standardize province names
        province_mapping = {
            'ON': 'Ontario', 'QC': 'Quebec', 'BC': 'British Columbia', 
            'AB': 'Alberta', 'MB': 'Manitoba', 'SK': 'Saskatchewan',
            'NS': 'Nova Scotia', 'NB': 'New Brunswick', 'NL': 'Newfoundland and Labrador',
            'PE': 'Prince Edward Island', 'YT': 'Yukon', 'NT': 'Northwest Territories', 
            'NU': 'Nunavut'
        }
        cleaned_df['Province_Full'] = cleaned_df['Province'].map(province_mapping)
        
        # Add derived columns
        cleaned_df['Year'] = cleaned_df['Application_Date'].dt.year
        cleaned_df['Month'] = cleaned_df['Application_Date'].dt.month
        cleaned_df['Quarter'] = cleaned_df['Application_Date'].dt.quarter
        cleaned_df['LTV_Ratio'] = (cleaned_df['Loan_Amount'] / cleaned_df['Property_Value']).round(3)
        
        # Data validation
        cleaned_df = cleaned_df[cleaned_df['Loan_Amount'] > 0]
        cleaned_df = cleaned_df[cleaned_df['Property_Value'] > 0]
        cleaned_df = cleaned_df[cleaned_df['LTV_Ratio'] <= 1.0]
        
        print(f"✅ Cleaned data: {len(cleaned_df)} valid records")
        self.cleaned_data = cleaned_df
        return cleaned_df
    
    def create_summaries(self, df):
        """Create aggregated summaries for dashboard"""
        print("📈 Creating aggregated summaries...")
        
        summaries = {}
        
        # Summary by Year
        yearly_summary = df.groupby('Year').agg({
            'Application_ID': 'count',
            'Loan_Amount': ['sum', 'mean', 'median'],
            'Property_Value': ['mean', 'median'],
            'LTV_Ratio': 'mean',
            'Interest_Rate': 'mean'
        }).round(2)
        yearly_summary.columns = ['Total_Applications', 'Total_Loan_Amount', 'Avg_Loan_Amount', 
                                'Median_Loan_Amount', 'Avg_Property_Value', 'Median_Property_Value',
                                'Avg_LTV_Ratio', 'Avg_Interest_Rate']
        yearly_summary = yearly_summary.reset_index()
        summaries['yearly'] = yearly_summary
        
        # Summary by Month
        monthly_summary = df.groupby(['Year', 'Month']).agg({
            'Application_ID': 'count',
            'Loan_Amount': ['sum', 'mean'],
            'Property_Value': 'mean',
            'LTV_Ratio': 'mean'
        }).round(2)
        monthly_summary.columns = ['Total_Applications', 'Total_Loan_Amount', 'Avg_Loan_Amount', 
                                 'Avg_Property_Value', 'Avg_LTV_Ratio']
        monthly_summary = monthly_summary.reset_index()
        summaries['monthly'] = monthly_summary
        
        # Summary by Province
        province_summary = df.groupby('Province_Full').agg({
            'Application_ID': 'count',
            'Loan_Amount': ['sum', 'mean'],
            'Property_Value': 'mean',
            'LTV_Ratio': 'mean'
        }).round(2)
        province_summary.columns = ['Total_Applications', 'Total_Loan_Amount', 'Avg_Loan_Amount', 
                                  'Avg_Property_Value', 'Avg_LTV_Ratio']
        province_summary = province_summary.reset_index()
        summaries['province'] = province_summary
        
        # Summary by Property Type
        property_summary = df.groupby('Property_Type').agg({
            'Application_ID': 'count',
            'Loan_Amount': ['sum', 'mean'],
            'Property_Value': 'mean',
            'LTV_Ratio': 'mean'
        }).round(2)
        property_summary.columns = ['Total_Applications', 'Total_Loan_Amount', 'Avg_Loan_Amount', 
                                  'Avg_Property_Value', 'Avg_LTV_Ratio']
        property_summary = property_summary.reset_index()
        summaries['property_type'] = property_summary
        
        print("✅ Created all summary tables")
        return summaries
    
    def calculate_trends(self, df):
        """Calculate month-over-month and year-over-year trends"""
        print("📊 Calculating trends...")
        
        # Monthly trends
        monthly_data = df.groupby(['Year', 'Month']).agg({
            'Application_ID': 'count',
            'Loan_Amount': 'sum'
        }).reset_index()
        
        monthly_data = monthly_data.sort_values(['Year', 'Month'])
        monthly_data['MoM_Applications'] = monthly_data['Application_ID'].pct_change() * 100
        monthly_data['MoM_Loan_Volume'] = monthly_data['Loan_Amount'].pct_change() * 100
        
        # Year-over-year trends
        yearly_data = df.groupby('Year').agg({
            'Application_ID': 'count',
            'Loan_Amount': 'sum'
        }).reset_index()
        
        yearly_data = yearly_data.sort_values('Year')
        yearly_data['YoY_Applications'] = yearly_data['Application_ID'].pct_change() * 100
        yearly_data['YoY_Loan_Volume'] = yearly_data['Loan_Amount'].pct_change() * 100
        
        trends = {
            'monthly': monthly_data.round(2),
            'yearly': yearly_data.round(2)
        }
        
        print("✅ Calculated trend analysis")
        return trends
    
    def export_data(self, df, summaries, trends):
        """Export all processed data to CSV files"""
        print("💾 Exporting processed data...")
        
        try:
            # Export cleaned data
            df.to_csv('cleaned_mortgage_data.csv', index=False)
            print("✅ Exported: cleaned_mortgage_data.csv")
            
            # Export summaries
            summaries['yearly'].to_csv('mortgage_summary_by_year.csv', index=False)
            print("✅ Exported: mortgage_summary_by_year.csv")
            
            summaries['monthly'].to_csv('mortgage_summary_by_month.csv', index=False)
            print("✅ Exported: mortgage_summary_by_month.csv")
            
            summaries['province'].to_csv('mortgage_summary_by_province.csv', index=False)
            print("✅ Exported: mortgage_summary_by_province.csv")
            
            summaries['property_type'].to_csv('mortgage_summary_by_property_type.csv', index=False)
            print("✅ Exported: mortgage_summary_by_property_type.csv")
            
            # Export trends
            trends['monthly'].to_csv('mortgage_monthly_trends.csv', index=False)
            print("✅ Exported: mortgage_monthly_trends.csv")
            
            trends['yearly'].to_csv('mortgage_yearly_trends.csv', index=False)
            print("✅ Exported: mortgage_yearly_trends.csv")
            
        except Exception as e:
            print(f"❌ Error exporting data: {str(e)}")
    
    def generate_quality_report(self, df):
        """Generate data quality report"""
        print("📋 Generating data quality report...")
        
        report = []
        report.append("CANADIAN MORTGAGE DATA QUALITY REPORT")
        report.append("=" * 50)
        report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Basic statistics
        report.append("DATASET OVERVIEW:")
        report.append(f"Total Records: {len(df):,}")
        report.append(f"Date Range: {df['Application_Date'].min()} to {df['Application_Date'].max()}")
        report.append(f"Provinces Covered: {df['Province_Full'].nunique()}")
        report.append(f"Property Types: {df['Property_Type'].nunique()}")
        report.append("")
        
        # Data completeness
        report.append("DATA COMPLETENESS:")
        for col in df.columns:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100
            report.append(f"{col}: {100-missing_pct:.1f}% complete")
        report.append("")
        
        # Business metrics
        report.append("KEY BUSINESS METRICS:")
        report.append(f"Average Loan Amount: ${df['Loan_Amount'].mean():,.2f}")
        report.append(f"Average Property Value: ${df['Property_Value'].mean():,.2f}")
        report.append(f"Average LTV Ratio: {df['LTV_Ratio'].mean():.3f}")
        report.append(f"Average Interest Rate: {df['Interest_Rate'].mean():.2f}%")
        report.append(f"Approval Rate: {(df['Approval_Status'] == 'Approved').mean()*100:.1f}%")
        report.append("")
        
        # Top provinces by volume
        report.append("TOP PROVINCES BY APPLICATION VOLUME:")
        top_provinces = df['Province_Full'].value_counts().head(5)
        for province, count in top_provinces.items():
            report.append(f"{province}: {count:,} applications")
        report.append("")
        
        report_text = "\n".join(report)
        
        # Save report
        with open('mortgage_data_quality_report.txt', 'w') as f:
            f.write(report_text)
        
        print("✅ Generated: mortgage_data_quality_report.txt")
        print("\n" + report_text)
        
        return report_text

# Execute the pipeline
def main():
    try:
        processor = MortgageDataProcessor()
        
        # Step 1: Generate sample data
        raw_data = processor.generate_sample_data(10000)
        
        # Step 2: Clean the data
        cleaned_data = processor.clean_data(raw_data)
        
        # Step 3: Create summaries
        summaries = processor.create_summaries(cleaned_data)
        
        # Step 4: Calculate trends
        trends = processor.calculate_trends(cleaned_data)
        
        # Step 5: Export all data
        processor.export_data(cleaned_data, summaries, trends)
        
        # Step 6: Generate quality report
        processor.generate_quality_report(cleaned_data)
        
        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("Files generated for Power BI dashboard:")
        print("• cleaned_mortgage_data.csv")
        print("• mortgage_summary_by_year.csv")
        print("• mortgage_summary_by_month.csv")
        print("• mortgage_summary_by_province.csv")
        print("• mortgage_summary_by_property_type.csv")
        print("• mortgage_monthly_trends.csv")
        print("• mortgage_yearly_trends.csv")
        print("• mortgage_data_quality_report.txt")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
