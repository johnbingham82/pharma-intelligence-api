#!/usr/bin/env python3
"""
Prepare PBS real data for integration
Loads national PBS data and creates state distribution model
"""
import csv
import json
from collections import defaultdict

def load_metformin_national_data():
    """Load real metformin national data from PBS CSV"""
    print("="*80)
    print("Loading Real PBS National Data")
    print("="*80)
    
    # Get metformin item codes
    print("\n1. Loading metformin PBS item codes...")
    metformin_codes = set()
    with open('pbs_data/pbs_item_drug_map.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'METFORMIN' in row['DRUG_NAME'].upper():
                metformin_codes.add(row['ITEM_CODE'])
    
    print(f"   ✓ Found {len(metformin_codes)} metformin item codes")
    
    # Load prescribing data
    print(f"\n2. Loading PBS prescribing data (this may take a minute)...")
    monthly_data = defaultdict(lambda: {'prescriptions': 0, 'cost': 0.0})
    
    with open('pbs_data/pbs_jul2024_jun2025.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row['ITEM_CODE'] in metformin_codes:
                month = row['MONTH_OF_SUPPLY']
                rx = int(row['PRESCRIPTIONS'])
                cost = float(row['TOTAL_COST'])
                
                monthly_data[month]['prescriptions'] += rx
                monthly_data[month]['cost'] += cost
    
    print(f"   ✓ Loaded data for {len(monthly_data)} months")
    
    # Display summary
    print(f"\n3. National Monthly Data:")
    total_rx = 0
    total_cost = 0.0
    
    for month in sorted(monthly_data.keys()):
        data = monthly_data[month]
        total_rx += data['prescriptions']
        total_cost += data['cost']
        
        # Convert month to readable format
        year = month[:4]
        mon = month[4:6]
        print(f"   {year}-{mon}: {data['prescriptions']:>9,} Rx, ${data['cost']:>12,.2f} AUD")
    
    print(f"\n   TOTAL:    {total_rx:>9,} Rx, ${total_cost:>12,.2f} AUD")
    print(f"   Average:  {total_rx//12:>9,} Rx/month, ${total_cost/12:>12,.2f} AUD/month")
    
    return dict(monthly_data)

def create_state_distribution_model():
    """
    Create intelligent state distribution model
    Based on population + demographic factors
    """
    print("\n" + "="*80)
    print("Creating State Distribution Model")
    print("="*80)
    
    # State demographics and health factors
    states = {
        'NSW': {
            'name': 'New South Wales',
            'population': 8_166_000,
            'demographic_factor': 1.05,  # Slightly higher (urban + aging population)
            'rationale': 'Largest population, Sydney urban factors'
        },
        'VIC': {
            'name': 'Victoria',
            'population': 6_613_000,
            'demographic_factor': 1.02,  # Slightly higher (Melbourne urban)
            'rationale': 'Large urban population, Melbourne'
        },
        'QLD': {
            'name': 'Queensland',
            'population': 5_185_000,
            'demographic_factor': 1.10,  # Higher (older population, warm climate)
            'rationale': 'Older population, retirement destination, high diabetes rates'
        },
        'WA': {
            'name': 'Western Australia',
            'population': 2_667_000,
            'demographic_factor': 0.95,  # Lower (younger population)
            'rationale': 'Younger demographic, mining industry'
        },
        'SA': {
            'name': 'South Australia',
            'population': 1_771_000,
            'demographic_factor': 1.08,  # Higher (older population)
            'rationale': 'Older population, higher chronic disease rates'
        },
        'TAS': {
            'name': 'Tasmania',
            'population': 541_000,
            'demographic_factor': 1.15,  # Highest (oldest population)
            'rationale': 'Oldest population in Australia, high prescribing rates'
        },
        'ACT': {
            'name': 'Australian Capital Territory',
            'population': 431_000,
            'demographic_factor': 0.85,  # Lowest (youngest, health-conscious)
            'rationale': 'Youngest population, high education, health-conscious'
        },
        'NT': {
            'name': 'Northern Territory',
            'population': 246_000,
            'demographic_factor': 0.90,  # Lower (young, remote)
            'rationale': 'Young population, remote, different health access patterns'
        }
    }
    
    # Calculate weighted shares
    total_pop = sum(s['population'] for s in states.values())
    total_weighted = sum(s['population'] * s['demographic_factor'] for s in states.values())
    
    for state_code, state_data in states.items():
        # Population share
        pop_share = state_data['population'] / total_pop
        
        # Weighted share (includes demographic factors)
        weighted_share = (state_data['population'] * state_data['demographic_factor']) / total_weighted
        
        state_data['pop_share'] = pop_share
        state_data['weighted_share'] = weighted_share
    
    # Display model
    print(f"\nState Distribution Factors:")
    print(f"\n{'State':<6} {'Population':>12} {'Pop %':>7} {'Demo Factor':>12} {'Weighted %':>11} {'Rationale':<50}")
    print("-" * 110)
    
    for state_code in ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']:
        s = states[state_code]
        print(f"{state_code:<6} {s['population']:>12,} {s['pop_share']*100:>6.2f}% "
              f"{s['demographic_factor']:>11.2f}x {s['weighted_share']*100:>10.2f}% "
              f"{s['rationale']:<50}")
    
    print("-" * 110)
    print(f"{'TOTAL':<6} {total_pop:>12,} {100.0:>6.2f}%                 {100.0:>10.2f}%")
    
    return states

def apply_distribution(monthly_national_data, state_model):
    """Apply state distribution to national data"""
    print("\n" + "="*80)
    print("Applying State Distribution")
    print("="*80)
    
    state_monthly_data = {}
    
    for state_code, state_info in state_model.items():
        state_monthly_data[state_code] = {}
        
        for month, nat_data in monthly_national_data.items():
            # Distribute national data by weighted share
            state_rx = int(nat_data['prescriptions'] * state_info['weighted_share'])
            state_cost = nat_data['cost'] * state_info['weighted_share']
            
            state_monthly_data[state_code][month] = {
                'prescriptions': state_rx,
                'cost': state_cost
            }
    
    # Verify distribution (should sum to national totals)
    print(f"\nVerification for sample month (202410):")
    month = '202410'
    
    total_distributed_rx = sum(state_monthly_data[s][month]['prescriptions'] 
                               for s in state_model.keys())
    total_distributed_cost = sum(state_monthly_data[s][month]['cost'] 
                                for s in state_model.keys())
    
    actual_rx = monthly_national_data[month]['prescriptions']
    actual_cost = monthly_national_data[month]['cost']
    
    print(f"  National (actual):     {actual_rx:,} Rx, ${actual_cost:,.2f} AUD")
    print(f"  Distributed (summed):  {total_distributed_rx:,} Rx, ${total_distributed_cost:,.2f} AUD")
    print(f"  Difference:            {abs(actual_rx - total_distributed_rx)} Rx ({abs(actual_rx - total_distributed_rx)/actual_rx*100:.2f}%)")
    
    # Show per-state breakdown for sample month
    print(f"\nState Breakdown for Oct 2024 (202410):")
    for state_code in ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']:
        data = state_monthly_data[state_code][month]
        share = data['prescriptions'] / actual_rx * 100
        print(f"  {state_code}: {data['prescriptions']:>7,} Rx ({share:>5.2f}%), ${data['cost']:>12,.2f} AUD")
    
    return state_monthly_data

def export_for_integration(state_monthly_data, state_model):
    """Export data in format ready for data_sources_au.py integration"""
    print("\n" + "="*80)
    print("Exporting for Integration")
    print("="*80)
    
    # Create comprehensive export with metadata
    export_data = {
        'metadata': {
            'source': 'PBS (Pharmaceutical Benefits Scheme)',
            'source_url': 'https://www.pbs.gov.au/statistics/dos-and-dop/',
            'data_type': 'Real national data with demographic state distribution',
            'drug': 'Metformin (all formulations)',
            'atc_code': 'A10BA02',
            'period_start': '2024-07',
            'period_end': '2025-06',
            'update_frequency': 'Monthly',
            'created': '2026-02-04'
        },
        'state_model': {
            state_code: {
                'name': info['name'],
                'population': info['population'],
                'demographic_factor': info['demographic_factor'],
                'weighted_share': info['weighted_share']
            }
            for state_code, info in state_model.items()
        },
        'monthly_data': state_monthly_data
    }
    
    # Save to JSON
    output_file = 'pbs_data/pbs_metformin_real_data.json'
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n✓ Exported to {output_file}")
    print(f"  File size: {len(json.dumps(export_data)) / 1024:.1f} KB")
    print(f"  States: {len(state_model)}")
    print(f"  Months: {len(list(state_monthly_data.values())[0])}")
    
    # Also create simple CSV for easy inspection
    csv_file = 'pbs_data/pbs_metformin_by_state_month.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'Month', 'Prescriptions', 'Cost_AUD', 'Demographic_Factor'])
        
        for state_code in sorted(state_monthly_data.keys()):
            for month in sorted(state_monthly_data[state_code].keys()):
                data = state_monthly_data[state_code][month]
                demo_factor = state_model[state_code]['demographic_factor']
                writer.writerow([
                    state_code, 
                    month, 
                    data['prescriptions'],
                    f"{data['cost']:.2f}",
                    demo_factor
                ])
    
    print(f"✓ Also exported CSV to {csv_file}")
    
    return export_data

def main():
    """Main execution"""
    try:
        # Step 1: Load real PBS national data
        monthly_national_data = load_metformin_national_data()
        
        # Step 2: Create state distribution model
        state_model = create_state_distribution_model()
        
        # Step 3: Apply distribution
        state_monthly_data = apply_distribution(monthly_national_data, state_model)
        
        # Step 4: Export for integration
        export_data = export_for_integration(state_monthly_data, state_model)
        
        print("\n" + "="*80)
        print("✅ SUCCESS")
        print("="*80)
        print(f"\nReal PBS data prepared and ready for integration!")
        print(f"\nNext step: Update data_sources_au.py to load from:")
        print(f"  pbs_data/pbs_metformin_real_data.json")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
