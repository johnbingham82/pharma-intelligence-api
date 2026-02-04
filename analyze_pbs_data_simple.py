#!/usr/bin/env python3
"""
Analyze downloaded PBS data structure (without pandas)
"""
import csv
from collections import defaultdict

def analyze_drug_map():
    """Analyze PBS drug mapping file"""
    print("="*80)
    print("PBS Drug Mapping File Analysis")
    print("="*80)
    
    with open('pbs_data/pbs_item_drug_map.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"\nTotal records: {len(rows):,}")
    print(f"\nColumns: {list(rows[0].keys())}")
    
    # Find metformin entries
    metformin_items = [row for row in rows if 'METFORMIN' in row['DRUG_NAME'].upper()]
    
    print(f"\n\nMetformin entries: {len(metformin_items)}")
    for item in metformin_items[:10]:
        print(f"  {item['ITEM_CODE']}: {item['DRUG_NAME']} (ATC: {item['ATC5_Code']})")
    
    return rows, metformin_items

def analyze_prescribing_data(metformin_item_codes):
    """Analyze PBS prescribing data"""
    print("\n" + "="*80)
    print("PBS Prescribing Data Analysis")
    print("="*80)
    
    with open('pbs_data/pbs_jul2024_jun2025.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        
        # Get first row to see structure
        first_row = next(reader)
        
        print(f"\nColumns: {list(first_row.keys())}")
        print(f"\nSample record:")
        for key, value in first_row.items():
            print(f"  {key}: {value}")
        
        # Check for state data
        has_state = any('state' in col.lower() or 'territ' in col.lower() 
                       for col in first_row.keys())
        
        if has_state:
            print(f"\n✓ State/territory column found!")
        else:
            print(f"\n⚠️  No state/territory column found - this is NATIONAL data only")
        
        # Reset to beginning
        f.seek(0)
        next(reader)  # Skip header
        
        # Analyze metformin data
        print(f"\n\nAnalyzing metformin prescriptions...")
        monthly_totals = defaultdict(lambda: {'rx': 0, 'cost': 0.0})
        total_rx = 0
        total_cost = 0.0
        
        for row in reader:
            if row['ITEM_CODE'] in metformin_item_codes:
                month = row['MONTH_OF_SUPPLY']
                rx = int(row['PRESCRIPTIONS'])
                cost = float(row['TOTAL_COST'])
                
                monthly_totals[month]['rx'] += rx
                monthly_totals[month]['cost'] += cost
                total_rx += rx
                total_cost += cost
        
        print(f"\n\nMetformin prescriptions by month:")
        for month in sorted(monthly_totals.keys()):
            data = monthly_totals[month]
            print(f"  {month}: {data['rx']:,} prescriptions, ${data['cost']:,.2f} AUD")
        
        print(f"\n\nAnnual totals (Jul 2024 - Jun 2025):")
        print(f"  Total prescriptions: {total_rx:,}")
        print(f"  Total cost: ${total_cost:,.2f} AUD")
        if total_rx > 0:
            print(f"  Average cost per Rx: ${total_cost/total_rx:.2f} AUD")
        
        return has_state, total_rx, total_cost

if __name__ == "__main__":
    try:
        # Analyze drug map
        all_drugs, metformin_items = analyze_drug_map()
        metformin_codes = {item['ITEM_CODE'] for item in metformin_items}
        
        # Analyze prescribing data
        has_states, total_rx, total_cost = analyze_prescribing_data(metformin_codes)
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"✓ Drug mapping: {len(all_drugs):,} PBS items")
        print(f"✓ Metformin items: {len(metformin_codes)}")
        print(f"✓ Annual metformin prescriptions: {total_rx:,}")
        print(f"✓ Annual metformin cost: ${total_cost:,.2f} AUD")
        
        if has_states:
            print(f"✓ State/territory data available")
            print(f"\n✅ Ready to integrate with data_sources_au.py")
        else:
            print(f"\n⚠️  State/territory breakdown NOT in this file")
            print(f"\nOPTIONS:")
            print(f"1. Use national totals and distribute by state population")
            print(f"2. Download larger PBS file with state data (98MB XLSX)")
            print(f"3. Query AIHW dashboard API for state breakdowns")
            print(f"\nRECOMMENDATION: Option 1 (population-based distribution)")
            print(f"  - Quick to implement")
            print(f"  - Reasonably accurate for most drugs")
            print(f"  - Can refine with real state data later")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
