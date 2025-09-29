import pandas as pd
import numpy as np
from datetime import datetime
import os

class MortgageDataProcessor:
    def __init__(self):
        self.cleaned_data = None
        self.summary_data = None
        
    def load_data(self, mortgage_csv_path, metadata_csv_path=None):
        """Load the mortgage approvals dataset and optional metadata"""
        try:
            self.raw_data = pd.read_csv(mortgage_csv_path)
            print(f"Loaded mortgage data: {len(self.raw_data)} rows")
            
            if metadata_csv_path and os.path.exists(metadata_csv_path):
                self.metadata = pd.read_csv(metadata_csv_path)
                print(f"Loaded metadata: {len(self.metadata)} rows")
            else:
                self.metadata = None
                print("No metadata file provided or found")
                
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def clean_data(self):
        """Clean and standardize the mortgage data"""
        print("Starting data cleaning...")
        df = self.raw_data.copy()
        
        # Define expected columns and their clean names
        column_mapping = {
            'region': 'Region',
            'property_type': 'PropertyType', 
            'number_of_approvals': 'TotalApprovals',
            'value_of_approvals': 'TotalValue',
            'year': 'Year',
            'month': 'Month'
        }
        
        # Handle different possible column names (case insensitive)
        actual_columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
        df.columns = actual_columns
        
        # Rename columns to business-friendly names
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Check for missing key columns
        required_columns = ['Region', 'PropertyType', 'TotalApprovals', 'TotalValue', 'Year', 'Month']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Warning: Missing required columns: {missing_columns}")
            # Try to create missing columns if possible
            if 'Year' not in df.columns and 'date' in df.columns:
                df['Year'] = pd.to_datetime(df['date']).dt.year
            if 'Month' not in df.columns and 'date' in df.columns:
                df['Month'] = pd.to_datetime(df['date']).dt.month
        
        # Clean and standardize data
        # 1. Remove rows with missing values in key columns
        initial_rows = len(df)
        key_columns = [col for col in required_columns if col in df.columns]
        df = df.dropna(subset=key_columns)
        print(f"Removed {initial_rows - len(df)} rows with missing key values")
        
        # 2. Standardize region names
        if 'Region' in df.columns:
            df['Region'] = df['Region'].str.strip().str.title()
            # Common standardizations
            region_mapping = {
                'Bc': 'British Columbia',
                'B.C.': 'British Columbia', 
                'Alta': 'Alberta',
                'Sask': 'Saskatchewan',
                'Man': 'Manitoba',
                'Ont': 'Ontario',
                'Que': 'Quebec',
                'N.B.': 'New Brunswick',
                'N.S.': 'Nova Scotia',
                'P.E.I.': 'Prince Edward Island',
                'Nfld': 'Newfoundland and Labrador',
                'N.W.T.': 'Northwest Territories',
                'Nvt': 'Nunavut'
            }
            df['Region'] = df['Region'].replace(region_mapping)
        
        # 3. Standardize property types
        if 'PropertyType' in df.columns:
            df['PropertyType'] = df['PropertyType'].str.strip().str.title()
            property_mapping = {
                'Existing': 'Existing',
                'New': 'New',
                'New Residential Construction': 'New Residential Construction',
                'New Construction': 'New Residential Construction',
                'Resale': 'Existing'
            }
            df['PropertyType'] = df['PropertyType'].replace(property_mapping)
        
        # 4. Convert numeric fields
        numeric_columns = ['TotalApprovals', 'TotalValue', 'Year', 'Month']
        for col in numeric_columns:
            if col in df.columns:
                # Remove any currency symbols or commas
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.replace('[$,]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 5. Create date column for easier processing
        if 'Year' in df.columns and 'Month' in df.columns:
            df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
        
        # 6. Check for anomalies
        self.detect_anomalies(df)
        
        self.cleaned_data = df
        print(f"Data cleaning completed. Final dataset: {len(df)} rows")
        return df
    
    def detect_anomalies(self, df):
        """Detect and report data anomalies"""
        print("\nChecking for anomalies...")
        
        # Check for missing months in time series
        if 'Date' in df.columns:
            date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='MS')
            missing_dates = set(date_range) - set(df['Date'].unique())
            if missing_dates:
                print(f"Missing months detected: {len(missing_dates)} gaps")
                for date in sorted(missing_dates)[:5]:  # Show first 5
                    print(f"  - {date.strftime('%Y-%m')}")
        
        # Check for outliers in approvals
        if 'TotalApprovals' in df.columns:
            q1 = df['TotalApprovals'].quantile(0.25)
            q3 = df['TotalApprovals'].quantile(0.75)
            iqr = q3 - q1
            outliers = df[(df['TotalApprovals'] < q1 - 1.5*iqr) | (df['TotalApprovals'] > q3 + 1.5*iqr)]
            if len(outliers) > 0:
                print(f"Approval outliers detected: {len(outliers)} records")
    
    def create_summary_data(self):
        """Create aggregated summary data for dashboard"""
        if self.cleaned_data is None:
            print("Error: No cleaned data available. Run clean_data() first.")
            return None
            
        print("Creating summary data...")
        df = self.cleaned_data.copy()
        
        # Aggregate by different dimensions
        summaries = []
        
        # 1. By Year
        yearly = df.groupby('Year').agg({
            'TotalApprovals': 'sum',
            'TotalValue': 'sum'
        }).reset_index()
        yearly['Dimension'] = 'Year'
        yearly['DimensionValue'] = yearly['Year'].astype(str)
        summaries.append(yearly[['Dimension', 'DimensionValue', 'TotalApprovals', 'TotalValue']])
        
        # 2. By Month (across all years)
        monthly = df.groupby('Month').agg({
            'TotalApprovals': 'sum',
            'TotalValue': 'sum'
        }).reset_index()
        monthly['Dimension'] = 'Month'
        monthly['DimensionValue'] = monthly['Month'].astype(str)
        summaries.append(monthly[['Dimension', 'DimensionValue', 'TotalApprovals', 'TotalValue']])
        
        # 3. By Region
        regional = df.groupby('Region').agg({
            'TotalApprovals': 'sum',
            'TotalValue': 'sum'
        }).reset_index()
        regional['Dimension'] = 'Region'
        regional['DimensionValue'] = regional['Region']
        summaries.append(regional[['Dimension', 'DimensionValue', 'TotalApprovals', 'TotalValue']])
        
        # 4. By Property Type
        property_type = df.groupby('PropertyType').agg({
            'TotalApprovals': 'sum',
            'TotalValue': 'sum'
        }).reset_index()
        property_type['Dimension'] = 'PropertyType'
        property_type['DimensionValue'] = property_type['PropertyType']
        summaries.append(property_type[['Dimension', 'DimensionValue', 'TotalApprovals', 'TotalValue']])
        
        # Combine all summaries
        self.summary_data = pd.concat(summaries, ignore_index=True)
        
        print(f"Summary data created: {len(self.summary_data)} summary records")
        return self.summary_data
    
    def calculate_trends(self):
        """Calculate month-over-month and year-over-year trends"""
        if self.cleaned_data is None:
            print("Error: No cleaned data available.")
            return None
            
        print("Calculating trends...")
        df = self.cleaned_data.copy()
        
        # Sort by date
        df = df.sort_values('Date')
        
        # Calculate trends by region and property type
        trend_data = []
        
        for region in df['Region'].unique():
            for prop_type in df['PropertyType'].unique():
                subset = df[(df['Region'] == region) & (df['PropertyType'] == prop_type)].copy()
                
                if len(subset) < 2:
                    continue
                    
                # Calculate month-over-month change
                subset['MoM_Approvals_Change'] = subset['TotalApprovals'].pct_change() * 100
                subset['MoM_Value_Change'] = subset['TotalValue'].pct_change() * 100
                
                # Calculate year-over-year change
                subset = subset.set_index('Date')
                subset['YoY_Approvals_Change'] = subset['TotalApprovals'].pct_change(periods=12) * 100
                subset['YoY_Value_Change'] = subset['TotalValue'].pct_change(periods=12) * 100
                subset = subset.reset_index()
                
                trend_data.append(subset)
        
        if trend_data:
            trends_df = pd.concat(trend_data, ignore_index=True)
            print(f"Trends calculated for {len(trends_df)} records")
            return trends_df
        else:
            print("No trend data could be calculated")
            return None
    
    def export_data(self, output_dir='output'):
        """Export cleaned and summary data to CSV files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Export cleaned data
        if self.cleaned_data is not None:
            cleaned_path = os.path.join(output_dir, 'mortgage_approvals_cleaned.csv')
            self.cleaned_data.to_csv(cleaned_path, index=False)
            print(f"Cleaned data exported to: {cleaned_path}")
        
        # Export summary data
        if self.summary_data is not None:
            summary_path = os.path.join(output_dir, 'mortgage_approvals_summary.csv')
            self.summary_data.to_csv(summary_path, index=False)
            print(f"Summary data exported to: {summary_path}")
        
        # Export trends data
        trends_df = self.calculate_trends()
        if trends_df is not None:
            trends_path = os.path.join(output_dir, 'mortgage_approvals_trends.csv')
            trends_df.to_csv(trends_path, index=False)
            print(f"Trends data exported to: {trends_path}")
        
        print(f"\nAll files exported to '{output_dir}' directory")

# Example usage
if __name__ == "__main__":
    processor = MortgageDataProcessor()
    
    # Load your data files here
    # processor.load_data('mortgage_approvals_dataset.csv', 'metadata.csv')
    # processor.clean_data()
    # processor.create_summary_data()
    # processor.export_data()
    
    print("Mortgage Data Processor ready!")
    print("To use:")
    print("1. processor.load_data('your_mortgage_file.csv', 'your_metadata_file.csv')")
    print("2. processor.clean_data()")
    print("3. processor.create_summary_data()")
    print("4. processor.export_data()")
