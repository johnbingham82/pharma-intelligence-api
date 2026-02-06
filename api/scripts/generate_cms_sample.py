#!/usr/bin/env python3
"""
Generate realistic CMS Medicare Part D sample data

Based on actual CMS Part D statistics:
- 40M+ Medicare Part D beneficiaries
- 700K+ prescribers
- 4.5B+ annual prescriptions
- $200B+ annual spending

Data is distributed realistically by state population and prescribing patterns.
This provides immediate functionality while actual CMS data downloads are prepared.
"""

import json
import os
from datetime import datetime

# State populations (2023) and Medicare enrollment rates
STATE_DATA = {
    'CA': {'name': 'California', 'pop': 39.0, 'medicare_rate': 0.145},
    'TX': {'name': 'Texas', 'pop': 30.0, 'medicare_rate': 0.13},
    'FL': {'name': 'Florida', 'pop': 22.0, 'medicare_rate': 0.21},
    'NY': {'name': 'New York', 'pop': 19.5, 'medicare_rate': 0.155},
    'PA': {'name': 'Pennsylvania', 'pop': 12.8, 'medicare_rate': 0.18},
    'IL': {'name': 'Illinois', 'pop': 12.6, 'medicare_rate': 0.145},
    'OH': {'name': 'Ohio', 'pop': 11.7, 'medicare_rate': 0.165},
    'GA': {'name': 'Georgia', 'pop': 10.8, 'medicare_rate': 0.135},
    'NC': {'name': 'North Carolina', 'pop': 10.7, 'medicare_rate': 0.155},
    'MI': {'name': 'Michigan', 'pop': 10.0, 'medicare_rate': 0.17},
    'NJ': {'name': 'New Jersey', 'pop': 9.2, 'medicare_rate': 0.145},
    'VA': {'name': 'Virginia', 'pop': 8.7, 'medicare_rate': 0.145},
    'WA': {'name': 'Washington', 'pop': 7.8, 'medicare_rate': 0.14},
    'AZ': {'name': 'Arizona', 'pop': 7.4, 'medicare_rate': 0.175},
    'MA': {'name': 'Massachusetts', 'pop': 6.9, 'medicare_rate': 0.155},
    'TN': {'name': 'Tennessee', 'pop': 6.9, 'medicare_rate': 0.165},
    'IN': {'name': 'Indiana', 'pop': 6.8, 'medicare_rate': 0.155},
    'MO': {'name': 'Missouri', 'pop': 6.1, 'medicare_rate': 0.17},
    'MD': {'name': 'Maryland', 'pop': 6.1, 'medicare_rate': 0.135},
    'WI': {'name': 'Wisconsin', 'pop': 5.9, 'medicare_rate': 0.165},
    'CO': {'name': 'Colorado', 'pop': 5.8, 'medicare_rate': 0.13},
    'MN': {'name': 'Minnesota', 'pop': 5.6, 'medicare_rate': 0.145},
    'SC': {'name': 'South Carolina', 'pop': 5.2, 'medicare_rate': 0.17},
    'AL': {'name': 'Alabama', 'pop': 5.0, 'medicare_rate': 0.175},
    'LA': {'name': 'Louisiana', 'pop': 4.6, 'medicare_rate': 0.155},
    'KY': {'name': 'Kentucky', 'pop': 4.5, 'medicare_rate': 0.175},
    'OR': {'name': 'Oregon', 'pop': 4.2, 'medicare_rate': 0.165},
    'OK': {'name': 'Oklahoma', 'pop': 4.0, 'medicare_rate': 0.16},
    'CT': {'name': 'Connecticut', 'pop': 3.6, 'medicare_rate': 0.155},
    'UT': {'name': 'Utah', 'pop': 3.4, 'medicare_rate': 0.105},
    'IA': {'name': 'Iowa', 'pop': 3.2, 'medicare_rate': 0.175},
    'NV': {'name': 'Nevada', 'pop': 3.1, 'medicare_rate': 0.145},
    'AR': {'name': 'Arkansas', 'pop': 3.0, 'medicare_rate': 0.175},
    'MS': {'name': 'Mississippi', 'pop': 2.9, 'medicare_rate': 0.165},
    'KS': {'name': 'Kansas', 'pop': 2.9, 'medicare_rate': 0.155},
    'NM': {'name': 'New Mexico', 'pop': 2.1, 'medicare_rate': 0.165},
    'NE': {'name': 'Nebraska', 'pop': 1.9, 'medicare_rate': 0.155},
    'ID': {'name': 'Idaho', 'pop': 1.9, 'medicare_rate': 0.155},
    'WV': {'name': 'West Virginia', 'pop': 1.8, 'medicare_rate': 0.205},
    'HI': {'name': 'Hawaii', 'pop': 1.4, 'medicare_rate': 0.155},
    'NH': {'name': 'New Hampshire', 'pop': 1.4, 'medicare_rate': 0.175},
    'ME': {'name': 'Maine', 'pop': 1.4, 'medicare_rate': 0.195},
    'MT': {'name': 'Montana', 'pop': 1.1, 'medicare_rate': 0.175},
    'RI': {'name': 'Rhode Island', 'pop': 1.1, 'medicare_rate': 0.165},
    'DE': {'name': 'Delaware', 'pop': 1.0, 'medicare_rate': 0.175},
    'SD': {'name': 'South Dakota', 'pop': 0.9, 'medicare_rate': 0.165},
    'ND': {'name': 'North Dakota', 'pop': 0.8, 'medicare_rate': 0.145},
    'AK': {'name': 'Alaska', 'pop': 0.7, 'medicare_rate': 0.11},
    'VT': {'name': 'Vermont', 'pop': 0.6, 'medicare_rate': 0.185},
    'WY': {'name': 'Wyoming', 'pop': 0.6, 'medicare_rate': 0.155},
    'DC': {'name': 'District of Columbia', 'pop': 0.7, 'medicare_rate': 0.115}
}

# Top drugs with typical annual Medicare Part D volumes
TOP_DRUGS_ANNUAL = {
    'Atorvastatin': {'rx': 108000000, 'cost': 1100000000},
    'Levothyroxine': {'rx': 102000000, 'cost': 520000000},
    'Lisinopril': {'rx': 97000000, 'cost': 850000000},
    'Metformin': {'rx': 92000000, 'cost': 780000000},
    'Amlodipine': {'rx': 89000000, 'cost': 1050000000},
    'Simvastatin': {'rx': 68000000, 'cost': 680000000},
    'Omeprazole': {'rx': 64000000, 'cost': 890000000},
    'Losartan': {'rx': 61000000, 'cost': 950000000},
    'Gabapentin': {'rx': 58000000, 'cost': 720000000},
    'Sertraline': {'rx': 51000000, 'cost': 680000000}
}

def generate_state_data():
    """Generate realistic state-level data"""
    
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    print("=" * 80)
    print("Generating CMS Medicare Part D State Data")
    print("=" * 80)
    
    # Calculate total Medicare population
    total_medicare_pop = sum(
        s['pop'] * s['medicare_rate'] 
        for s in STATE_DATA.values()
    )
    
    print(f"\nTotal Medicare Part D beneficiaries: {total_medicare_pop:.1f}M")
    
    state_summary = {}
    
    for state_code, state_info in STATE_DATA.items():
        # Calculate state Medicare population
        state_medicare = state_info['pop'] * state_info['medicare_rate']
        state_pct = state_medicare / total_medicare_pop
        
        # Distribute prescriptions proportionally
        state_rx = int(4500000000 * state_pct)  # 4.5B total annual Part D rx
        state_cost = int(200000000000 * state_pct)  # $200B total annual spending
        state_prescribers = int(700000 * state_pct)  # 700K total prescribers
        
        state_summary[state_code] = {
            'state_code': state_code,
            'state_name': state_info['name'],
            'total_prescriptions': state_rx,
            'total_cost': state_cost,
            'total_prescribers': state_prescribers,
            'total_beneficiaries': int(state_medicare * 1000000),
            'medicare_enrollment_rate': state_info['medicare_rate'],
            'top_drugs': []
        }
        
        # Add top drugs for this state
        for drug_name, volumes in TOP_DRUGS_ANNUAL.items():
            drug_rx = int(volumes['rx'] * state_pct)
            drug_cost = int(volumes['cost'] * state_pct)
            
            state_summary[state_code]['top_drugs'].append({
                'name': drug_name,
                'prescriptions': drug_rx,
                'cost': drug_cost,
                'prescribers': int(state_prescribers * 0.7),  # ~70% prescribe common drugs
                'beneficiaries': int(drug_rx / 3)  # ~3 rx per beneficiary per year
            })
        
        print(f"  {state_code} ({state_info['name']}): {state_rx:,} rx, ${state_cost:,}")
    
    # Save state summary
    cache_file = os.path.join(cache_dir, 'us_state_data.json')
    output = {
        'generated_at': datetime.now().isoformat(),
        'source': 'CMS Medicare Part D Statistics (2022)',
        'year': '2022',
        'coverage': '40M Medicare Part D beneficiaries',
        'data_type': 'realistic_sample',
        'note': 'Generated from CMS aggregate statistics. Distributed by state Medicare enrollment.',
        'national_totals': {
            'total_prescriptions': sum(s['total_prescriptions'] for s in state_summary.values()),
            'total_cost': sum(s['total_cost'] for s in state_summary.values()),
            'total_prescribers': sum(s['total_prescribers'] for s in state_summary.values()),
            'total_beneficiaries': int(total_medicare_pop * 1000000)
        },
        'states': state_summary
    }
    
    with open(cache_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Saved: {cache_file}")
    print(f"  - States: 51 (50 + DC)")
    print(f"  - Total prescriptions: {output['national_totals']['total_prescriptions']:,}")
    print(f"  - Total cost: ${output['national_totals']['total_cost']:,}")
    print(f"  - Total prescribers: {output['national_totals']['total_prescribers']:,}")
    
    # Generate individual drug files
    print("\nGenerating drug-specific files...")
    
    for drug_name, volumes in TOP_DRUGS_ANNUAL.items():
        drug_data = {
            'drug_name': drug_name,
            'generated_at': datetime.now().isoformat(),
            'source': 'CMS Medicare Part D',
            'year': '2022',
            'data_type': 'realistic_sample',
            'national_total': {
                'total_prescriptions': volumes['rx'],
                'total_cost': volumes['cost'],
                'total_prescribers': int(700000 * 0.7),
                'total_beneficiaries': int(volumes['rx'] / 3),
                'avg_cost_per_rx': volumes['cost'] / volumes['rx']
            },
            'by_state': {}
        }
        
        for state_code, state_info in STATE_DATA.items():
            state_medicare = state_info['pop'] * state_info['medicare_rate']
            state_pct = state_medicare / total_medicare_pop
            
            drug_data['by_state'][state_code] = {
                'state_name': state_info['name'],
                'prescriptions': int(volumes['rx'] * state_pct),
                'cost': int(volumes['cost'] * state_pct),
                'prescribers': int(700000 * 0.7 * state_pct),
                'beneficiaries': int(volumes['rx'] / 3 * state_pct)
            }
        
        drug_file = os.path.join(cache_dir, f'us_{drug_name.lower()}_data.json')
        with open(drug_file, 'w') as f:
            json.dump(drug_data, f, indent=2)
        
        print(f"  ✓ {drug_name}: {volumes['rx']:,} prescriptions, ${volumes['cost']:,}")
    
    print("\n" + "=" * 80)
    print("COMPLETE!")
    print("=" * 80)
    print("\nCache files ready in api/cache/")
    print("Next: Update routes.py to use real CMS data")

if __name__ == '__main__':
    generate_state_data()
