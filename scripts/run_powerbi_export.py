#!/usr/bin/env python3
"""
Execute the Power BI data export script
"""

import sys
import os

# Add the scripts directory to the path
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

# Import and run the export script
try:
    print("Starting Power BI data export...")
    
    # Import the export functions
    from powerbi_data_export import *
    
    print("✅ Power BI data export completed successfully!")
    print("\nGenerated files in csv/ folder:")
    print("- mortgage_applications.csv")
    print("- dim_date.csv") 
    print("- dim_province.csv")
    print("- dim_property_type.csv")
    print("- monthly_summary.csv")
    print("\nYou can now download this project and import these CSV files into Power BI Desktop!")
    
except Exception as e:
    print(f"❌ Error during export: {str(e)}")
    sys.exit(1)
