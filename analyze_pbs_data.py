#!/usr/bin/env python3
"""
Analyze downloaded PBS data structure and prepare for integration
"""
import pandas as pd
import sys

def analyze_drug_map():
    """Analyze PBS drug mapping file"""
    print("="*80)
    print("PBS Drug Mapping File Analysis")
    print("="*80)
    
    df = pd.read_csv('pbs_data/pbs_item_drug_map.csv')
    
    print(f"\nTotal records: {len(df):,}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nSample records:")
    print(df.head(10))
    
    # Find metformin entries
    metformin = df[df['DRUG_NAME'].str.contains('METFORMIN', case=False, na=False)]
    print(f"\n\nMetformin entries: {len(metformin)}")
    print(metformin)
    
    # ATC code distribution
    print(f"\n\nATC codes (top 10):")
    print(df['ATC5_Code'].value_counts().head(10))
    
    return df

def analyze_prescribing_data():
    """Analyze PBS prescribing data"""
    print("\n" + "="*80)
    print("PBS Prescribing Data Analysis")
    print("="*80)
    
    # Read first 10000 rows to get structure
    df = pd.read_csv('pbs_data/pbs_jul2024_jun2025.csv', nrows=10000)
    
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nSample records:")
    print(df.head())
    
    print(f"\n\nData types:")
    print(df.dtypes)
    
    print(f"\n\nUnique months:")
    print(sorted(df['MONTH_OF_SUPPLY'].unique()))
    
    print(f"\n\nPatient categories:")
    print(df['PATIENT_CAT'].unique())
    
    print(f"\n\nPharmacy types:")
    print(df['PHRMCY_TYPE'].unique())
    
    return df

def find_metformin_data():
    """Find and analyze metformin prescribing data"""
    print("\n" + "="*80)
    print("Metformin Data Analysis")
    print("="*80)
    
    # Get metformin item codes
    drug_map = pd.read_csv('pbs_data/pbs_item_drug_map.csv')
    metformin_items = drug_map[drug_map['DRUG_NAME'].str.contains('METFORMIN', case=False, na=False)]
    metformin_codes = metformin_items['ITEM_CODE'].tolist()
    
    print(f"\nMetformin PBS item codes: {len(metformin_codes)}")
    print(metformin_codes)
    
    # Read full prescribing data (this might take a moment)
    print(f"\nLoading full PBS data...")
    df = pd.read_csv('pbs_data/pbs_jul2024_jun2025.csv')
    
    print(f"Total records: {len(df):,}")
    
    # Filter for metformin
    metformin_data = df[df['ITEM_CODE'].isin(metformin_codes)]
    
    print(f"\nMetformin records: {len(metformin_data):,}")
    
    # Aggregate by month
    monthly = metformin_data.groupby('MONTH_OF_SUPPLY').agg({
        'PRESCRIPTIONS': 'sum',
        'TOTAL_COST': 'sum'
    }).reset_index()
    
    print(f"\n\nMetformin prescriptions by month:")
    print(monthly)
    
    # Total for year
    total_rx = metformin_data['PRESCRIPTIONS'].sum()
    total_cost = metformin_data['TOTAL_COST'].sum()
    
    print(f"\n\nAnnual totals (Jul 2024 - Jun 2025):")
    print(f"  Total prescriptions: {total_rx:,}")
    print(f"  Total cost: ${total_cost:,.2f} AUD")
    print(f"  Average cost per Rx: ${total_cost/total_rx:.2f} AUD")
    
    return metformin_data

def check_state_data():
    """Check if state/territory data exists in this file"""
    print("\n" + "="*80)
    print("State/Territory Data Check")
    print("="*80)
    
    df = pd.read_csv('pbs_data/pbs_jul2024_jun2025.csv', nrows=1000)
    
    # Check if any column contains state information
    print(f"\nColumns: {list(df.columns)}")
    
    # Look for state-like data
    for col in df.columns:
        if 'state' in col.lower() or 'territ' in col.lower():
            print(f"\n✓ Found state column: {col}")
            print(df[col].unique())
            return True
    
    print(f"\n⚠️  No state/territory column found in this file")
    print(f"\nThis appears to be NATIONAL-LEVEL data only")
    print(f"State-level data requires a different PBS dataset")
    
    return False

if __name__ == "__main__":
    try:
        drug_map = analyze_drug_map()
        prescribing_data = analyze_prescribing_data()
        metformin_data = find_metformin_data()
        has_states = check_state_data()
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"✓ Drug mapping file loaded: {len(drug_map):,} items")
        print(f"✓ Prescribing data analyzed")
        print(f"✓ Metformin data found and aggregated")
        
        if has_states:
            print(f"✓ State/territory data available")
        else:
            print(f"⚠️  State/territory data NOT in this file")
            print(f"\nNOTE: This is national-level PBS data.")
            print(f"For state-level analysis, we need:")
            print(f"  1. Download the main 'Date of Supply' report (98MB XLSX)")
            print(f"  2. Or use AIHW monthly data dashboard")
            print(f"  3. Or work with national totals + estimate state distribution")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
