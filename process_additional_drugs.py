#!/usr/bin/env python3
"""
Process Additional Drugs from PBS Data
Extracts atorvastatin and rosuvastatin from PBS CSV and creates state-distributed data
"""
import csv
import json
from collections import defaultdict

# State distribution model (same as metformin)
STATE_MODEL = {
    'NSW': {
        'name': 'New South Wales',
        'population': 8_166_000,
        'demographic_factor': 1.05,
        'weighted_share': 0.3214
    },
    'VIC': {
        'name': 'Victoria',
        'population': 6_613_000,
        'demographic_factor': 1.02,
        'weighted_share': 0.2528
    },
    'QLD': {
        'name': 'Queensland',
        'population': 5_185_000,
        'demographic_factor': 1.10,
        'weighted_share': 0.2138
    },
    'WA': {
        'name': 'Western Australia',
        'population': 2_667_000,
        'demographic_factor': 0.95,
        'weighted_share': 0.0950
    },
    'SA': {
        'name': 'South Australia',
        'population': 1_771_000,
        'demographic_factor': 1.08,
        'weighted_share': 0.0717
    },
    'TAS': {
        'name': 'Tasmania',
        'population': 541_000,
        'demographic_factor': 1.15,
        'weighted_share': 0.0233
    },
    'ACT': {
        'name': 'Australian Capital Territory',
        'population': 431_000,
        'demographic_factor': 0.85,
        'weighted_share': 0.0137
    },
    'NT': {
        'name': 'Northern Territory',
        'population': 246_000,
        'demographic_factor': 0.90,
        'weighted_share': 0.0083
    }
}

def get_drug_item_codes(drug_name):
    """Get all PBS item codes for a drug"""
    print(f"\nFinding PBS item codes for {drug_name}...")
    codes = set()
    
    with open('pbs_data/pbs_item_drug_map.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if drug_name.upper() in row['DRUG_NAME'].upper():
                # Only include pure drug, not combinations
                if '&' not in row['DRUG_NAME'] and '+' not in row['DRUG_NAME']:
                    codes.add(row['ITEM_CODE'])
    
    print(f"  ✓ Found {len(codes)} PBS item codes")
    return codes

def load_national_data(drug_name, item_codes):
    """Load national PBS data for a drug"""
    print(f"\nLoading national PBS data for {drug_name}...")
    monthly_data = defaultdict(lambda: {'prescriptions': 0, 'cost': 0.0})
    
    with open('pbs_data/pbs_jul2024_jun2025.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row['ITEM_CODE'] in item_codes:
                month = row['MONTH_OF_SUPPLY']
                rx = int(row['PRESCRIPTIONS'])
                cost = float(row['TOTAL_COST'])
                
                monthly_data[month]['prescriptions'] += rx
                monthly_data[month]['cost'] += cost
    
    # Calculate totals
    total_rx = sum(d['prescriptions'] for d in monthly_data.values())
    total_cost = sum(d['cost'] for d in monthly_data.values())
    
    print(f"  ✓ Loaded data for {len(monthly_data)} months")
    print(f"  Total prescriptions: {total_rx:,}")
    print(f"  Total cost: ${total_cost:,.2f} AUD")
    
    return dict(monthly_data)

def distribute_to_states(monthly_national_data):
    """Apply state distribution to national data"""
    print(f"\nApplying state distribution...")
    state_monthly_data = {}
    
    for state_code, state_info in STATE_MODEL.items():
        state_monthly_data[state_code] = {}
        
        for month, nat_data in monthly_national_data.items():
            state_rx = int(nat_data['prescriptions'] * state_info['weighted_share'])
            state_cost = nat_data['cost'] * state_info['weighted_share']
            
            state_monthly_data[state_code][month] = {
                'prescriptions': state_rx,
                'cost': state_cost
            }
    
    print(f"  ✓ Distributed to {len(STATE_MODEL)} states")
    return state_monthly_data

def export_drug_data(drug_name, atc_code, state_monthly_data, monthly_national_data):
    """Export drug data to JSON"""
    print(f"\nExporting {drug_name} data...")
    
    export_data = {
        'metadata': {
            'source': 'PBS (Pharmaceutical Benefits Scheme)',
            'source_url': 'https://www.pbs.gov.au/statistics/dos-and-dop/',
            'data_type': 'Real national data with demographic state distribution',
            'drug': drug_name,
            'atc_code': atc_code,
            'period_start': '2024-07',
            'period_end': '2025-06',
            'update_frequency': 'Monthly',
            'created': '2026-02-04'
        },
        'state_model': STATE_MODEL,
        'monthly_data': state_monthly_data
    }
    
    filename = f"pbs_data/pbs_{drug_name.lower()}_real_data.json"
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"  ✓ Saved to {filename}")
    print(f"  File size: {len(json.dumps(export_data)) / 1024:.1f} KB")
    
    return filename

def process_drug(drug_name, atc_code):
    """Process a single drug"""
    print("="*80)
    print(f"Processing {drug_name} (ATC: {atc_code})")
    print("="*80)
    
    # Get item codes
    item_codes = get_drug_item_codes(drug_name)
    
    if not item_codes:
        print(f"  ❌ No PBS item codes found for {drug_name}")
        return None
    
    # Load national data
    monthly_national_data = load_national_data(drug_name, item_codes)
    
    if not monthly_national_data:
        print(f"  ❌ No prescribing data found for {drug_name}")
        return None
    
    # Distribute to states
    state_monthly_data = distribute_to_states(monthly_national_data)
    
    # Export
    filename = export_drug_data(drug_name, atc_code, state_monthly_data, monthly_national_data)
    
    # Show sample month
    sample_month = '202410'
    if sample_month in monthly_national_data:
        print(f"\nSample: October 2024")
        print(f"  National: {monthly_national_data[sample_month]['prescriptions']:,} Rx")
        print(f"  NSW: {state_monthly_data['NSW'][sample_month]['prescriptions']:,} Rx")
        print(f"  VIC: {state_monthly_data['VIC'][sample_month]['prescriptions']:,} Rx")
    
    return filename

def main():
    """Process multiple drugs"""
    drugs = [
        ('Atorvastatin', 'C10AA05'),
        ('Rosuvastatin', 'C10AA07'),
    ]
    
    results = []
    
    for drug_name, atc_code in drugs:
        result = process_drug(drug_name, atc_code)
        if result:
            results.append((drug_name, result))
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    for drug_name, filename in results:
        print(f"✓ {drug_name}: {filename}")
    
    print(f"\nTotal drugs processed: {len(results)}")
    print(f"\nData files ready for integration with data_sources_au.py")

if __name__ == "__main__":
    main()
