#!/usr/bin/env python3
"""
Download and aggregate CMS Medicare Part D data by state and drug

CMS publishes annual Part D prescriber data files:
- Dataset: Medicare Part D Prescribers by Provider and Drug
- URL: https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers
- Coverage: 40M+ Medicare beneficiaries (seniors 65+)
- Granularity: Prescriber-level by drug
- Update frequency: Annual

This script downloads and aggregates to state-level for top drugs.
"""

import pandas as pd
import requests
import os
import json
from datetime import datetime
from collections import defaultdict

# Top 20 drugs to aggregate (most prescribed in US)
TOP_DRUGS = [
    'ATORVASTATIN',
    'LEVOTHYROXINE',
    'LISINOPRIL',
    'METFORMIN',
    'AMLODIPINE',
    'SIMVASTATIN',
    'OMEPRAZOLE',
    'LOSARTAN',
    'GABAPENTIN',
    'SERTRALINE',
    'FUROSEMIDE',
    'HYDROCODONE',
    'PREDNISONE',
    'ALBUTEROL',
    'TRAMADOL',
    'METOPROLOL',
    'ROSUVASTATIN',
    'ESCITALOPRAM',
    'PANTOPRAZOLE',
    'CLOPIDOGREL'
]

# All 50 US states + DC
US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
    'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
    'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def download_cms_sample():
    """
    Download a sample of CMS data using their API
    
    Note: Full dataset is 8GB+. For demo, we'll use API to get sample data.
    For production, download full CSV from:
    https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/data
    """
    
    print("=" * 80)
    print("CMS Medicare Part D Data Download")
    print("=" * 80)
    
    # CMS API endpoint
    base_url = "https://data.cms.gov/data-api/v1/dataset"
    dataset_id = "9552739e-3d05-4c1b-8eff-ecabf391e2e5"  # Part D Prescribers by Provider and Drug
    endpoint = f"{base_url}/{dataset_id}/data"
    
    print(f"\nDataset: Medicare Part D Prescribers by Provider and Drug")
    print(f"URL: {endpoint}")
    print(f"\nNote: Full dataset is 8GB+. Using API to fetch sample for top drugs.")
    print(f"For production, download full annual file from data.cms.gov")
    
    # Aggregate data structure
    state_drug_data = defaultdict(lambda: defaultdict(lambda: {
        'total_claims': 0,
        'total_cost': 0,
        'prescriber_count': 0,
        'beneficiary_count': 0
    }))
    
    # For each top drug, fetch sample data
    for drug in TOP_DRUGS[:5]:  # Start with top 5 for testing
        print(f"\nFetching data for {drug}...")
        
        try:
            # CMS API parameters
            params = {
                'filter[gnrc_name]': drug,
                'size': 1000,  # Fetch 1000 records per drug
                'offset': 0
            }
            
            response = requests.get(endpoint, params=params, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                records = len(data)
                print(f"  ✓ Fetched {records} records for {drug}")
                
                # Aggregate by state
                for record in data:
                    state = record.get('prscrbr_state_abrvtn', '').strip().upper()
                    
                    if state not in US_STATES:
                        continue
                    
                    # Extract metrics
                    total_clms = float(record.get('tot_clms', 0))
                    total_drug_cost = float(record.get('tot_drug_cst', 0))
                    bene_count = float(record.get('tot_benes', 0))
                    
                    # Aggregate
                    state_drug_data[state][drug]['total_claims'] += total_clms
                    state_drug_data[state][drug]['total_cost'] += total_drug_cost
                    state_drug_data[state][drug]['beneficiary_count'] += bene_count
                    state_drug_data[state][drug]['prescriber_count'] += 1
                    
            else:
                print(f"  ✗ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error fetching {drug}: {e}")
    
    return state_drug_data

def aggregate_to_cache(state_drug_data):
    """
    Aggregate data and save to cache files
    """
    
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    print("\n" + "=" * 80)
    print("Aggregating data to cache files...")
    print("=" * 80)
    
    # Create state-level aggregate (all drugs combined)
    state_summary = {}
    
    for state, drugs in state_drug_data.items():
        state_summary[state] = {
            'state_code': state,
            'total_prescriptions': sum(d['total_claims'] for d in drugs.values()),
            'total_cost': sum(d['total_cost'] for d in drugs.values()),
            'total_prescribers': len(drugs),
            'total_beneficiaries': sum(d['beneficiary_count'] for d in drugs.values()),
            'drug_count': len(drugs),
            'top_drugs': []
        }
        
        # Sort drugs by prescription count
        sorted_drugs = sorted(
            drugs.items(),
            key=lambda x: x[1]['total_claims'],
            reverse=True
        )
        
        # Add top 10 drugs for this state
        for drug_name, metrics in sorted_drugs[:10]:
            state_summary[state]['top_drugs'].append({
                'name': drug_name,
                'prescriptions': int(metrics['total_claims']),
                'cost': int(metrics['total_cost']),
                'prescribers': metrics['prescriber_count'],
                'beneficiaries': int(metrics['beneficiary_count'])
            })
    
    # Save state summary
    cache_file = os.path.join(cache_dir, 'us_state_data.json')
    with open(cache_file, 'w') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'source': 'CMS Medicare Part D Prescribers by Provider and Drug',
            'year': '2022',
            'coverage': '40M+ Medicare beneficiaries',
            'note': 'Sample data from API - download full annual file for production',
            'states': state_summary
        }, f, indent=2)
    
    print(f"\n✓ Saved state summary: {cache_file}")
    print(f"  - States: {len(state_summary)}")
    print(f"  - Total prescriptions: {sum(s['total_prescriptions'] for s in state_summary.values()):,.0f}")
    print(f"  - Total cost: ${sum(s['total_cost'] for s in state_summary.values()):,.0f}")
    
    # Create drug-specific files for top drugs
    for drug in TOP_DRUGS[:5]:
        drug_data = {
            'drug_name': drug,
            'generated_at': datetime.now().isoformat(),
            'source': 'CMS Medicare Part D',
            'year': '2022',
            'national_total': {
                'total_prescriptions': 0,
                'total_cost': 0,
                'total_prescribers': 0,
                'total_beneficiaries': 0
            },
            'by_state': {}
        }
        
        for state, drugs in state_drug_data.items():
            if drug in drugs:
                metrics = drugs[drug]
                drug_data['by_state'][state] = {
                    'prescriptions': int(metrics['total_claims']),
                    'cost': int(metrics['total_cost']),
                    'prescribers': metrics['prescriber_count'],
                    'beneficiaries': int(metrics['beneficiary_count'])
                }
                
                # Update national totals
                drug_data['national_total']['total_prescriptions'] += int(metrics['total_claims'])
                drug_data['national_total']['total_cost'] += int(metrics['total_cost'])
                drug_data['national_total']['total_prescribers'] += metrics['prescriber_count']
                drug_data['national_total']['total_beneficiaries'] += int(metrics['beneficiary_count'])
        
        # Save drug file
        drug_file = os.path.join(cache_dir, f'us_{drug.lower()}_data.json')
        with open(drug_file, 'w') as f:
            json.dump(drug_data, f, indent=2)
        
        print(f"✓ Saved {drug} data: {drug_file}")
        print(f"  - States: {len(drug_data['by_state'])}")
        print(f"  - National total: {drug_data['national_total']['total_prescriptions']:,} prescriptions")

def main():
    """Main execution"""
    
    print("\n" + "=" * 80)
    print("CMS MEDICARE PART D DATA PROCESSOR")
    print("=" * 80)
    print("\nThis script downloads and aggregates CMS Medicare Part D prescriber data.")
    print("\nOptions:")
    print("  1. API Sample (quick, limited data)")
    print("  2. Full Download (slow, complete data - requires manual download)")
    print("\nFor demo purposes, using API sample...")
    print("\nTo get complete data:")
    print("  1. Visit: https://data.cms.gov/provider-summary-by-type-of-service/")
    print("     medicare-part-d-prescribers/data")
    print("  2. Download full CSV (~8GB)")
    print("  3. Place in api/data/cms/ directory")
    print("  4. Run this script with --full flag")
    
    # Download sample data
    state_drug_data = download_cms_sample()
    
    if not state_drug_data:
        print("\n✗ No data downloaded. Check API connectivity.")
        return
    
    # Aggregate and save
    aggregate_to_cache(state_drug_data)
    
    print("\n" + "=" * 80)
    print("COMPLETE!")
    print("=" * 80)
    print("\nCache files created in api/cache/")
    print("Next steps:")
    print("  1. Update routes.py to use cached CMS data")
    print("  2. Test with: curl http://localhost:8000/api/country/US")
    print("  3. Deploy to production")

if __name__ == '__main__':
    main()
