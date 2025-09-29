import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mortgage_data_processor import MortgageDataProcessor

def generate_quality_report(processor):
    """Generate a data quality report for the mortgage data"""
    if processor.cleaned_data is None:
        print("No cleaned data available for quality report")
        return
    
    df = processor.cleaned_data
    
    print("=== DATA QUALITY REPORT ===\n")
    
    # Basic statistics
    print("1. DATASET OVERVIEW")
    print(f"   Total Records: {len(df):,}")
    print(f"   Date Range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"   Columns: {len(df.columns)}")
    print()
    
    # Missing values
    print("2. MISSING VALUES")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✓ No missing values found")
    else:
        for col, count in missing[missing > 0].items():
            print(f"   ⚠ {col}: {count} missing ({count/len(df)*100:.1f}%)")
    print()
    
    # Data completeness by dimension
    print("3. DATA COMPLETENESS")
    print(f"   Regions: {df['Region'].nunique()} unique")
    for region in df['Region'].value_counts().head().items():
        print(f"     - {region[0]}: {region[1]:,} records")
    
    print(f"   Property Types: {df['PropertyType'].nunique()} unique")
    for prop_type in df['PropertyType'].value_counts().items():
        print(f"     - {prop_type[0]}: {prop_type[1]:,} records")
    print()
    
    # Time series completeness
    print("4. TIME SERIES ANALYSIS")
    if 'Date' in df.columns:
        date_counts = df.groupby('Date').size()
        expected_records_per_month = df['Region'].nunique() * df['PropertyType'].nunique()
        
        incomplete_months = date_counts[date_counts < expected_records_per_month]
        if len(incomplete_months) > 0:
            print(f"   ⚠ {len(incomplete_months)} months with incomplete data")
            print(f"   Expected {expected_records_per_month} records per month")
        else:
            print("   ✓ Complete time series data")
    print()
    
    # Value ranges and outliers
    print("5. VALUE ANALYSIS")
    print(f"   Total Approvals Range: {df['TotalApprovals'].min():,} - {df['TotalApprovals'].max():,}")
    print(f"   Total Value Range: ${df['TotalValue'].min():,.0f} - ${df['TotalValue'].max():,.0f}")
    
    # Calculate outliers
    for col in ['TotalApprovals', 'TotalValue']:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        outliers = df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)]
        print(f"   {col} outliers: {len(outliers)} records ({len(outliers)/len(df)*100:.1f}%)")
    print()
    
    # Business logic checks
    print("6. BUSINESS LOGIC VALIDATION")
    
    # Check for negative values
    negative_approvals = df[df['TotalApprovals'] < 0]
    negative_values = df[df['TotalValue'] < 0]
    
    if len(negative_approvals) > 0:
        print(f"   ⚠ {len(negative_approvals)} records with negative approvals")
    else:
        print("   ✓ No negative approval counts")
        
    if len(negative_values) > 0:
        print(f"   ⚠ {len(negative_values)} records with negative values")
    else:
        print("   ✓ No negative approval values")
    
    # Check average value per approval
    df['AvgValuePerApproval'] = df['TotalValue'] / df['TotalApprovals']
    avg_range = df['AvgValuePerApproval'].describe()
    
    print(f"   Average Value per Approval:")
    print(f"     - Mean: ${avg_range['mean']:,.0f}")
    print(f"     - Range: ${avg_range['min']:,.0f} - ${avg_range['max']:,.0f}")
    
    # Flag unrealistic values
    unrealistic = df[(df['AvgValuePerApproval'] < 100000) | (df['AvgValuePerApproval'] > 2000000)]
    if len(unrealistic) > 0:
        print(f"   ⚠ {len(unrealistic)} records with unrealistic average values")
    else:
        print("   ✓ All average values appear realistic")
    
    print("\n=== REPORT COMPLETE ===")
    print("Review any warnings (⚠) before proceeding to Power BI")

def create_visualizations(processor):
    """Create basic visualizations for data exploration"""
    if processor.cleaned_data is None:
        print("No data available for visualizations")
        return
    
    df = processor.cleaned_data
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Canadian Mortgage Approvals - Data Overview', fontsize=16)
    
    # 1. Approvals by Region
    region_totals = df.groupby('Region')['TotalApprovals'].sum().sort_values(ascending=True)
    axes[0,0].barh(region_totals.index, region_totals.values)
    axes[0,0].set_title('Total Approvals by Region')
    axes[0,0].set_xlabel('Total Approvals')
    
    # 2. Approvals by Property Type
    prop_totals = df.groupby('PropertyType')['TotalApprovals'].sum()
    axes[0,1].pie(prop_totals.values, labels=prop_totals.index, autopct='%1.1f%%')
    axes[0,1].set_title('Approvals by Property Type')
    
    # 3. Monthly trend
    monthly_trend = df.groupby(['Year', 'Month'])['TotalApprovals'].sum().reset_index()
    monthly_trend['Date'] = pd.to_datetime(monthly_trend[['Year', 'Month']].assign(day=1))
    axes[1,0].plot(monthly_trend['Date'], monthly_trend['TotalApprovals'])
    axes[1,0].set_title('Monthly Approval Trends')
    axes[1,0].set_xlabel('Date')
    axes[1,0].set_ylabel('Total Approvals')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # 4. Value vs Approvals scatter
    sample_data = df.sample(min(1000, len(df)))  # Sample for performance
    axes[1,1].scatter(sample_data['TotalApprovals'], sample_data['TotalValue'], alpha=0.6)
    axes[1,1].set_title('Value vs Approvals Relationship')
    axes[1,1].set_xlabel('Total Approvals')
    axes[1,1].set_ylabel('Total Value ($)')
    
    plt.tight_layout()
    plt.savefig('output/mortgage_data_overview.png', dpi=300, bbox_inches='tight')
    print("Visualization saved to: output/mortgage_data_overview.png")

if __name__ == "__main__":
    # Run quality report on processed data
    processor = MortgageDataProcessor()
    
    # Load and process data (using sample data for demo)
    from run_processing import create_sample_data
    create_sample_data()
    
    processor.load_data('sample_mortgage_data.csv')
    processor.clean_data()
    processor.create_summary_data()
    
    # Generate quality report
    generate_quality_report(processor)
    
    # Create visualizations
    create_visualizations(processor)
