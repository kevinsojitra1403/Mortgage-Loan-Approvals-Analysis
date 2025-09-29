import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("🏠 Canadian Mortgage Loan Approvals Dashboard - Data Processing")
print("=" * 60)

# Set random seed for reproducible results
np.random.seed(42)

try:
    # Generate sample mortgage data
    print("📊 Generating sample mortgage data...")
    
    provinces = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan']
    property_types = ['Single Family', 'Condo', 'Townhouse', 'Multi-Family']
    
    # Generate 5000 records for faster processing
    n_records = 5000
    data = []
    
    for i in range(n_records):
        loan_amount = np.random.uniform(200000, 800000)
        property_value = loan_amount / np.random.uniform(0.7, 0.9)
        
        record = {
            'Application_ID': f'APP{i+1:06d}',
            'Application_Date': (datetime.now() - timedelta(days=np.random.randint(0, 730))).strftime('%Y-%m-%d'),
            'Province': np.random.choice(provinces),
            'Property_Type': np.random.choice(property_types),
            'Loan_Amount': round(loan_amount, 2),
            'Property_Value': round(property_value, 2),
            'Credit_Score': int(np.random.uniform(600, 850)),
            'Interest_Rate': round(np.random.uniform(3.0, 6.0), 2),
            'Approval_Status': np.random.choice(['Approved', 'Denied'], p=[0.75, 0.25])
        }
        data.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    df['Application_Date'] = pd.to_datetime(df['Application_Date'])
    df['Year'] = df['Application_Date'].dt.year
    df['Month'] = df['Application_Date'].dt.month
    df['LTV_Ratio'] = (df['Loan_Amount'] / df['Property_Value']).round(3)
    
    print(f"✅ Generated {len(df)} mortgage records")
    
    # Create summaries
    print("📈 Creating summaries...")
    
    # Yearly summary
    yearly_summary = df.groupby('Year').agg({
        'Application_ID': 'count',
        'Loan_Amount': ['sum', 'mean'],
        'Property_Value': 'mean',
        'LTV_Ratio': 'mean',
        'Interest_Rate': 'mean'
    }).round(2)
    yearly_summary.columns = ['Total_Applications', 'Total_Loan_Amount', 'Avg_Loan_Amount', 
                             'Avg_Property_Value', 'Avg_LTV_Ratio', 'Avg_Interest_Rate']
    yearly_summary = yearly_summary.reset_index()
    
    # Provincial summary
    province_summary = df.groupby('Province').agg({
        'Application_ID': 'count',
        'Loan_Amount': ['sum', 'mean'],
        'Property_Value': 'mean'
    }).round(2)
    province_summary.columns = ['Total_Applications', 'Total_Loan_Amount', 'Avg_Loan_Amount', 'Avg_Property_Value']
    province_summary = province_summary.reset_index()
    
    # Property type summary
    property_summary = df.groupby('Property_Type').agg({
        'Application_ID': 'count',
        'Loan_Amount': 'mean',
        'Property_Value': 'mean'
    }).round(2)
    property_summary.columns = ['Total_Applications', 'Avg_Loan_Amount', 'Avg_Property_Value']
    property_summary = property_summary.reset_index()
    
    print("✅ Created all summaries")
    
    # Display results
    print("\n📊 YEARLY SUMMARY:")
    print(yearly_summary.to_string(index=False))
    
    print("\n🗺️ PROVINCIAL SUMMARY:")
    print(province_summary.to_string(index=False))
    
    print("\n🏠 PROPERTY TYPE SUMMARY:")
    print(property_summary.to_string(index=False))
    
    # Key metrics
    print("\n📋 KEY METRICS:")
    print(f"Total Applications: {len(df):,}")
    print(f"Average Loan Amount: ${df['Loan_Amount'].mean():,.2f}")
    print(f"Average Property Value: ${df['Property_Value'].mean():,.2f}")
    print(f"Average LTV Ratio: {df['LTV_Ratio'].mean():.3f}")
    print(f"Approval Rate: {(df['Approval_Status'] == 'Approved').mean()*100:.1f}%")
    
    # Top provinces
    print(f"\nTop Province by Volume: {df['Province'].value_counts().index[0]}")
    print(f"Most Common Property Type: {df['Property_Type'].value_counts().index[0]}")
    
    print("\n🎉 PROCESSING COMPLETED SUCCESSFULLY!")
    print("Data is ready for Power BI dashboard creation.")
    
except Exception as e:
    print(f"❌ Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()
