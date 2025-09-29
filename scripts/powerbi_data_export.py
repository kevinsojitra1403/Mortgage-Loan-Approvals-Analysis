import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_powerbi_ready_data():
    """Create properly formatted data files optimized for Power BI import"""
    
    print("Creating Power BI-ready data exports...")
    
    csv_folder = 'csv'
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
        print(f"✓ Created {csv_folder}/ folder")
    
    # Set random seed for reproducible data
    np.random.seed(42)
    
    # Generate comprehensive mortgage data
    n_records = 5000
    
    # Canadian provinces/territories
    provinces = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 
                'Saskatchewan', 'Nova Scotia', 'New Brunswick', 'Newfoundland and Labrador',
                'Prince Edward Island', 'Northwest Territories', 'Yukon', 'Nunavut']
    
    # Property types
    property_types = ['Existing', 'New', 'New Residential Construction']
    
    # Generate date range (last 3 years)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Create main dataset
    data = []
    for i in range(n_records):
        # Generate random date
        random_date = start_date + timedelta(
            days=np.random.randint(0, (end_date - start_date).days)
        )
        
        province_probs = [0.38, 0.23, 0.13, 0.11, 0.04, 0.03, 0.03, 0.02, 0.015, 0.005, 0.005, 0.005, 0.005]
        province_probs = np.array(province_probs) / np.sum(province_probs)  # Normalize to sum to 1.0
        province = np.random.choice(provinces, p=province_probs)
        
        property_probs = [0.6, 0.25, 0.15]
        property_probs = np.array(property_probs) / np.sum(property_probs)  # Normalize to sum to 1.0
        property_type = np.random.choice(property_types, p=property_probs)

        # Generate realistic mortgage values
        base_value = np.random.normal(450000, 150000)
        if province in ['Ontario', 'British Columbia']:
            base_value *= 1.4  # Higher prices in ON/BC
        elif province in ['Alberta']:
            base_value *= 1.1
        
        mortgage_value = max(200000, min(2000000, base_value))
        
        # LTV ratio (realistic distribution)
        ltv_ratio = np.random.normal(0.8, 0.1)
        ltv_ratio = max(0.5, min(0.95, ltv_ratio))
        
        # Approval status (realistic approval rates)
        approval_prob = 0.75
        if ltv_ratio > 0.9:
            approval_prob = 0.6
        elif ltv_ratio < 0.7:
            approval_prob = 0.85
            
        is_approved = np.random.random() < approval_prob
        
        data.append({
            'Application_ID': f'APP_{i+1:06d}',
            'Application_Date': random_date.strftime('%Y-%m-%d'),
            'Year': random_date.year,
            'Month': random_date.month,
            'Month_Name': random_date.strftime('%B'),
            'Quarter': f'Q{((random_date.month-1)//3)+1}',
            'Province': province,
            'Property_Type': property_type,
            'Mortgage_Value': round(mortgage_value, 2),
            'LTV_Ratio': round(ltv_ratio, 4),
            'Is_Approved': is_approved,
            'Approval_Status': 'Approved' if is_approved else 'Rejected',
            'Approval_Value': round(mortgage_value, 2) if is_approved else 0
        })
    
    # Create main DataFrame
    df = pd.DataFrame(data)
    
    # Export main dataset
    df.to_csv(os.path.join(csv_folder, 'mortgage_applications.csv'), index=False)
    print(f"✓ Exported csv/mortgage_applications.csv ({len(df)} records)")
    
    # Create summary tables for Power BI relationships
    
    # Date dimension table
    date_dim = df[['Application_Date', 'Year', 'Month', 'Month_Name', 'Quarter']].drop_duplicates().sort_values('Application_Date')
    date_dim.to_csv(os.path.join(csv_folder, 'dim_date.csv'), index=False)
    print(f"✓ Exported csv/dim_date.csv ({len(date_dim)} records)")
    
    # Province dimension table
    province_dim = pd.DataFrame({
        'Province': provinces,
        'Region': ['Central', 'Central', 'West', 'West', 'West', 'West', 
                  'Atlantic', 'Atlantic', 'Atlantic', 'Atlantic', 'North', 'North', 'North']
    })
    province_dim.to_csv(os.path.join(csv_folder, 'dim_province.csv'), index=False)
    print(f"✓ Exported csv/dim_province.csv ({len(province_dim)} records)")
    
    # Property type dimension table
    property_dim = pd.DataFrame({
        'Property_Type': property_types,
        'Property_Category': ['Resale', 'New Construction', 'New Construction']
    })
    property_dim.to_csv(os.path.join(csv_folder, 'dim_property_type.csv'), index=False)
    print(f"✓ Exported csv/dim_property_type.csv ({len(property_dim)} records)")
    
    # Create aggregated summary for quick insights
    monthly_summary = df.groupby(['Year', 'Month', 'Month_Name', 'Province', 'Property_Type']).agg({
        'Application_ID': 'count',
        'Mortgage_Value': 'sum',
        'Is_Approved': 'sum',
        'Approval_Value': 'sum',
        'LTV_Ratio': 'mean'
    }).reset_index()
    
    monthly_summary.columns = ['Year', 'Month', 'Month_Name', 'Province', 'Property_Type', 
                              'Total_Applications', 'Total_Mortgage_Value', 'Total_Approvals', 
                              'Total_Approval_Value', 'Avg_LTV_Ratio']
    
    monthly_summary['Approval_Rate'] = monthly_summary['Total_Approvals'] / monthly_summary['Total_Applications']
    monthly_summary.to_csv(os.path.join(csv_folder, 'monthly_summary.csv'), index=False)
    print(f"✓ Exported csv/monthly_summary.csv ({len(monthly_summary)} records)")
    
    # Generate key metrics for dashboard
    total_applications = len(df)
    total_approvals = df['Is_Approved'].sum()
    total_value = df['Mortgage_Value'].sum()
    total_approval_value = df['Approval_Value'].sum()
    avg_ltv = df['LTV_Ratio'].mean()
    approval_rate = total_approvals / total_applications
    
    print("\n" + "="*50)
    print("KEY METRICS FOR POWER BI DASHBOARD")
    print("="*50)
    print(f"Total Applications: {total_applications:,}")
    print(f"Total Approvals: {total_approvals:,}")
    print(f"Overall Approval Rate: {approval_rate:.1%}")
    print(f"Total Mortgage Value: ${total_value:,.0f}")
    print(f"Total Approval Value: ${total_approval_value:,.0f}")
    print(f"Average LTV Ratio: {avg_ltv:.1%}")
    
    # Top provinces by volume
    print(f"\nTOP 5 PROVINCES BY APPLICATIONS:")
    top_provinces = df['Province'].value_counts().head()
    for province, count in top_provinces.items():
        print(f"  {province}: {count:,} applications")
    
    return df

if __name__ == "__main__":
    create_powerbi_ready_data()
    print(f"\n✅ All Power BI data files created successfully!")
    print(f"📁 Files ready for Power BI import in csv/ folder:")
    print(f"   • mortgage_applications.csv (main fact table)")
    print(f"   • dim_date.csv (date dimension)")
    print(f"   • dim_province.csv (province dimension)")
    print(f"   • dim_property_type.csv (property type dimension)")
    print(f"   • monthly_summary.csv (pre-aggregated data)")
