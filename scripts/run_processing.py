import sys
import os
sys.path.append(os.getcwd())

from mortgage_data_processor import MortgageDataProcessor
import pandas as pd
import numpy as np

def create_sample_data():
    """Create sample mortgage data for testing"""
    print("Creating sample mortgage data for testing...")
    
    # Sample data structure
    regions = ['Ontario', 'British Columbia', 'Alberta', 'Quebec', 'Manitoba']
    property_types = ['Existing', 'New', 'New Residential Construction']
    
    data = []
    np.random.seed(42)  # For reproducible results
    
    for year in range(2020, 2024):
        for month in range(1, 13):
            for region in regions:
                for prop_type in property_types:
                    # Generate realistic sample data
                    base_approvals = {
                        'Ontario': 5000,
                        'British Columbia': 3000,
                        'Alberta': 2000,
                        'Quebec': 2500,
                        'Manitoba': 800
                    }
                    
                    # Add some seasonal variation
                    seasonal_factor = 1.2 if month in [4, 5, 6, 7, 8] else 0.9
                    
                    approvals = int(base_approvals[region] * seasonal_factor * (0.8 + 0.4 * np.random.rand()))
                    avg_value = 450000 if prop_type == 'New' else 380000
                    total_value = approvals * avg_value * (0.9 + 0.2 * np.random.rand())
                    
                    data.append({
                        'region': region,
                        'property_type': prop_type,
                        'number_of_approvals': approvals,
                        'value_of_approvals': total_value,
                        'year': year,
                        'month': month
                    })
    
    df = pd.DataFrame(data)
    df.to_csv('sample_mortgage_data.csv', index=False)
    print(f"Sample data created: {len(df)} records saved to 'sample_mortgage_data.csv'")
    return df

def main():
    """Main processing function"""
    print("=== Canadian Mortgage Loan Approvals - Dashboard Prep ===\n")
    
    try:
        # Initialize processor
        processor = MortgageDataProcessor()
        
        # For demonstration, create sample data
        # In real use, replace this with your actual data files
        sample_data = create_sample_data()
        
        # Load the data
        success = processor.load_data('sample_mortgage_data.csv')
        
        if not success:
            print("Failed to load data. Please check your file paths.")
            return
        
        # Clean the data
        cleaned_df = processor.clean_data()
        
        if cleaned_df is None:
            print("Data cleaning failed.")
            return
        
        # Create summary data
        summary_df = processor.create_summary_data()
        
        # Export all processed data
        processor.export_data()
        
        # Print summary statistics
        print("\n=== Processing Summary ===")
        print(f"Total records processed: {len(cleaned_df)}")
        print(f"Date range: {cleaned_df['Year'].min()} - {cleaned_df['Year'].max()}")
        print(f"Regions: {', '.join(cleaned_df['Region'].unique())}")
        print(f"Property types: {', '.join(cleaned_df['PropertyType'].unique())}")
        print(f"Total approvals: {cleaned_df['TotalApprovals'].sum():,}")
        print(f"Total value: ${cleaned_df['TotalValue'].sum():,.0f}")
        
        print("\n=== Files Ready for Power BI ===")
        print("✓ mortgage_approvals_cleaned.csv - Main dataset")
        print("✓ mortgage_approvals_summary.csv - Aggregated data")
        print("✓ mortgage_approvals_trends.csv - Trend calculations")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
