#!/usr/bin/env python3
"""
Process CMS Medicare Part D CSV file and generate cache files

File: MUP_DPR_RY25_P04_V10_DY23_NPIBN.csv (3.6GB)
Source: https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers

This script processes the full CMS dataset (~40M rows) and aggregates to:
- State-level summaries
- Drug-specific state breakdowns
"""

import pandas as pd
import os
import json
from datetime import datetime
from collections import defaultdict

# Top drugs to process (most prescribed in Medicare Part D)
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
    'SERTRALINE'
]

def process_cms_csv():
    """Process the full CMS CSV file"""
    
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'cms', 
                            'MUP_DPR_RY25_P04_V10_DY23_NPIBN.csv')
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        print("\nExpected file: MUP_DPR_RY25_P04_V10_DY23_NPIBN.csv")
        print("Download from: https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers")
        return None
    
    file_size = os.path.getsize(csv_file) / (1024**3)  # GB
    print("=" * 80)
    print("CMS MEDICARE PART D CSV PROCESSOR")
    print("=" * 80)
    print(f"\nFile: {os.path.basename(csv_file)}")
    print(f"Size: {file_size:.2f} GB")
    print(f"Processing top {len(TOP_DRUGS)} drugs...")
    print("\nThis will take 15-30 minutes depending on your machine.\n")
    
    # Data structure: state -> drug -> metrics
    state_drug_data = defaultdict(lambda: defaultdict(lambda: {
        'total_claims': 0,
        'total_cost': 0.0,
        'prescriber_count': set(),
        'beneficiary_count': 0
    }))
    
    # Track overall progress
    total_rows = 0
    matched_rows = 0
    chunk_size = 100000  # Process 100K rows at a time
    
    print("Reading CSV in chunks...")
    print("(This is a large file - please wait)\n")
    
    try:
        # Read CSV in chunks to handle 3.6GB file
        for chunk_num, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunk_size), 1):
            total_rows += len(chunk)
            
            # Filter for top drugs only (case-insensitive)
            chunk['Gnrc_Name_Upper'] = chunk['Gnrc_Name'].str.upper()
            filtered = chunk[chunk['Gnrc_Name_Upper'].isin(TOP_DRUGS)]
            matched_rows += len(filtered)
            
            # Process each row in this chunk
            for _, row in filtered.iterrows():
                state = row['Prscrbr_State_Abrvtn']
                drug = row['Gnrc_Name_Upper']
                
                # Skip if invalid state
                if pd.isna(state) or len(str(state).strip()) != 2:
                    continue
                
                state = str(state).strip().upper()
                
                # Extract metrics (handle missing values)
                try:
                    claims = float(row['Tot_Clms']) if pd.notna(row['Tot_Clms']) else 0
                    cost = float(row['Tot_Drug_Cst']) if pd.notna(row['Tot_Drug_Cst']) else 0
                    benes = float(row['Tot_Benes']) if pd.notna(row['Tot_Benes']) else 0
                    npi = str(row['Prscrbr_NPI']) if pd.notna(row['Prscrbr_NPI']) else None
                except (ValueError, TypeError):
                    continue
                
                # Aggregate
                state_drug_data[state][drug]['total_claims'] += claims
                state_drug_data[state][drug]['total_cost'] += cost
                state_drug_data[state][drug]['beneficiary_count'] += benes
                if npi:
                    state_drug_data[state][drug]['prescriber_count'].add(npi)
            
            # Progress update
            if chunk_num % 10 == 0:
                print(f"  Processed {total_rows:,} rows ({matched_rows:,} matched top drugs)...")
    
    except Exception as e:
        print(f"\n❌ Error processing CSV: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    print(f"\n✓ Processing complete!")
    print(f"  Total rows: {total_rows:,}")
    print(f"  Matched rows (top drugs): {matched_rows:,}")
    print(f"  States found: {len(state_drug_data)}")
    
    # Convert prescriber sets to counts
    for state in state_drug_data:
        for drug in state_drug_data[state]:
            state_drug_data[state][drug]['prescriber_count'] = len(
                state_drug_data[state][drug]['prescriber_count']
            )
    
    return state_drug_data

def save_to_cache(state_drug_data):
    """Save aggregated data to cache files"""
    
    if not state_drug_data:
        print("No data to save!")
        return
    
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    print("\n" + "=" * 80)
    print("SAVING CACHE FILES")
    print("=" * 80)
    
    # 1. Create state summary
    state_summary = {}
    
    for state, drugs in state_drug_data.items():
        state_summary[state] = {
            'state_code': state,
            'total_prescriptions': int(sum(d['total_claims'] for d in drugs.values())),
            'total_cost': int(sum(d['total_cost'] for d in drugs.values())),
            'total_prescribers': sum(d['prescriber_count'] for d in drugs.values()),
            'total_beneficiaries': int(sum(d['beneficiary_count'] for d in drugs.values())),
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
                'name': drug_name.title(),
                'prescriptions': int(metrics['total_claims']),
                'cost': int(metrics['total_cost']),
                'prescribers': metrics['prescriber_count'],
                'beneficiaries': int(metrics['beneficiary_count'])
            })
    
    # Save state summary
    state_file = os.path.join(cache_dir, 'us_state_data.json')
    with open(state_file, 'w') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'source': 'CMS Medicare Part D Prescribers by Provider and Drug',
            'year': '2023',
            'data_type': 'real_cms_data',
            'coverage': '40M+ Medicare Part D beneficiaries',
            'note': 'Aggregated from full CMS prescriber-level CSV',
            'national_totals': {
                'total_prescriptions': sum(s['total_prescriptions'] for s in state_summary.values()),
                'total_cost': sum(s['total_cost'] for s in state_summary.values()),
                'total_prescribers': sum(s['total_prescribers'] for s in state_summary.values()),
                'total_beneficiaries': sum(s['total_beneficiaries'] for s in state_summary.values())
            },
            'states': state_summary
        }, f, indent=2)
    
    print(f"\n✓ State summary: {state_file}")
    print(f"  States: {len(state_summary)}")
    print(f"  Total prescriptions: {sum(s['total_prescriptions'] for s in state_summary.values()):,}")
    print(f"  Total cost: ${sum(s['total_cost'] for s in state_summary.values()):,.0f}")
    
    # 2. Create drug-specific files
    print("\nCreating drug-specific files...")
    
    for drug in TOP_DRUGS:
        drug_data = {
            'drug_name': drug.title(),
            'generated_at': datetime.now().isoformat(),
            'source': 'CMS Medicare Part D',
            'year': '2023',
            'data_type': 'real_cms_data',
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
        
        print(f"  ✓ {drug.title()}: {drug_data['national_total']['total_prescriptions']:,} prescriptions")
    
    print("\n" + "=" * 80)
    print("COMPLETE!")
    print("=" * 80)
    print("\nCache files saved to: api/cache/")
    print("\nNext steps:")
    print("  1. Commit cache files: git add api/cache/*.json")
    print("  2. Deploy to Heroku: git push heroku main")
    print("  3. Test: curl https://pharma-intelligence-api...herokuapp.com/api/country/US")

def main():
    """Main execution"""
    
    print("\n" + "=" * 80)
    print("CMS MEDICARE PART D DATA PROCESSOR")
    print("=" * 80)
    print("\nThis script processes the full CMS CSV file (~3.6GB)")
    print("and generates state-level cache files.\n")
    
    # Process the CSV
    state_drug_data = process_cms_csv()
    
    if not state_drug_data:
        print("\n❌ Processing failed. Check error messages above.")
        return
    
    # Save to cache
    save_to_cache(state_drug_data)

if __name__ == '__main__':
    main()
