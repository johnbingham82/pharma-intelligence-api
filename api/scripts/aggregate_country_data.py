#!/usr/bin/env python3
"""
Country Data Aggregator
Queries live data sources and creates cached aggregates for country detail pages

Usage:
    python scripts/aggregate_country_data.py --country UK
    python scripts/aggregate_country_data.py --all
"""
import sys
import os
import json
import argparse
from datetime import datetime
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_sources_uk import UKDataSource
from data_sources_us import USDataSource
from data_sources_au import AustraliaDataSource
from data_sources_france import FranceDataSource
from data_sources_japan import JapanDataSource
from common_drugs import COMMON_DRUGS


# Top drugs to query for each country
TOP_DRUGS = {
    'UK': ['atorvastatin', 'metformin', 'amlodipine', 'omeprazole', 'simvastatin', 
           'ramipril', 'levothyroxine', 'salbutamol', 'lansoprazole', 'paracetamol'],
    'US': ['lisinopril', 'metformin', 'atorvastatin', 'levothyroxine', 'amlodipine', 
           'omeprazole', 'simvastatin', 'salbutamol', 'losartan', 'sertraline'],
    'AU': ['metformin', 'atorvastatin', 'rosuvastatin', 'amlodipine', 'perindopril',
           'omeprazole', 'salbutamol', 'levothyroxine', 'ramipril', 'esomeprazole'],
    'FR': ['metformin', 'atorvastatin', 'amlodipine', 'omeprazole', 'simvastatin',
           'ramipril', 'levothyroxine', 'salbutamol', 'paracetamol', 'lansoprazole'],
    'JP': ['amlodipine', 'atorvastatin', 'candesartan', 'omeprazole', 'rosuvastatin',
           'metformin', 'valsartan', 'telmisartan', 'olmesartan', 'esomeprazole']
}


# Region mapping functions for each country
def get_uk_region(practice_code, practice_name):
    """Map UK practice to NHS region"""
    # This is a simplified mapping - real implementation would use ONS postcode data
    # For now, use CCG code patterns or area names
    region_keywords = {
        'NHS England North East and Yorkshire': ['yorkshire', 'north east', 'humber', 'leeds', 'newcastle', 'durham'],
        'NHS England North West': ['manchester', 'liverpool', 'lancashire', 'cumbria', 'cheshire'],
        'NHS England Midlands': ['birmingham', 'nottingham', 'derby', 'leicester', 'coventry', 'stoke'],
        'NHS England East of England': ['norwich', 'cambridge', 'bedford', 'essex', 'hertford', 'suffolk'],
        'NHS England London': ['london', 'croydon', 'barnet', 'harrow', 'brent'],
        'NHS England South East': ['kent', 'surrey', 'sussex', 'oxford', 'reading', 'southampton'],
        'NHS England South West': ['bristol', 'exeter', 'plymouth', 'cornwall', 'bath', 'gloucester']
    }
    
    practice_lower = practice_name.lower()
    for region, keywords in region_keywords.items():
        if any(keyword in practice_lower for keyword in keywords):
            return region
    
    # Default fallback - distribute evenly
    return 'NHS England South East'  # Most populated region


def get_us_state(prescriber_id, prescriber_name):
    """Map US prescriber to state"""
    # US data sources typically include state in the data
    # For now, extract from name or use placeholder
    state_abbrevs = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']
    state_names = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 
                   'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
    
    # Simple keyword matching
    name_lower = prescriber_name.lower()
    for abbrev, full_name in zip(state_abbrevs, state_names):
        if full_name.lower() in name_lower or abbrev.lower() in name_lower:
            return full_name
    
    return 'California'  # Default


def aggregate_australia(cache_dir):
    """Aggregate Australia PBS data"""
    print("\n🇦🇺 Aggregating Australia (PBS)...")
    
    data_source = AustraliaDataSource()
    
    # Load real PBS data
    drugs_data = []
    top_drugs = TOP_DRUGS['AU']
    
    for drug_name in top_drugs:
        print(f"  → Loading {drug_name}...")
        drug_code = data_source.find_drug_code(drug_name)
        
        if not drug_code:
            print(f"    ⚠️  No code found for {drug_name}")
            continue
        
        # Get latest period
        period = data_source.get_latest_period()
        
        # Get prescribing data (returns state-level aggregates)
        prescribing_data = data_source.get_prescribing_data(drug_code, period)
        
        if prescribing_data:
            # Calculate totals
            total_rx = sum(p.prescriptions for p in prescribing_data)
            total_cost = sum(p.cost for p in prescribing_data)
            
            drugs_data.append({
                'name': drug_name.title(),
                'prescriptions': total_rx,
                'cost': total_cost
            })
            
            print(f"    ✓ {total_rx:,} prescriptions, A${total_cost:,.0f}")
    
    # Aggregate by state
    regional_data = defaultdict(lambda: {'prescriptions': 0, 'cost': 0, 'prescribers': 0})
    
    for drug_name in top_drugs[:3]:  # Use top 3 for regional breakdown
        drug_code = data_source.find_drug_code(drug_name)
        if drug_code:
            period = data_source.get_latest_period()
            prescribing_data = data_source.get_prescribing_data(drug_code, period)
            
            for p in prescribing_data:
                state = p.prescriber.name  # State name is in prescriber.name for AU
                regional_data[state]['prescriptions'] += p.prescriptions
                regional_data[state]['cost'] += p.cost
                regional_data[state]['prescribers'] += 1
    
    regions = [
        {
            'region': state,
            'prescriptions': int(data['prescriptions']),
            'cost': int(data['cost']),
            'prescribers': data['prescribers']
        }
        for state, data in regional_data.items()
    ]
    
    # Sort top drugs by prescriptions
    drugs_data.sort(key=lambda x: x['prescriptions'], reverse=True)
    
    # Create cache file
    cache_data = {
        'country': 'AU',
        'last_updated': datetime.now().isoformat(),
        'period': period,
        'regions': regions,
        'top_drugs': drugs_data,
        'monthly_data': None,  # TODO: Extract from PBS JSON
        'metadata': {
            'source': 'PBS - AIHW Real Data',
            'update_frequency': 'Monthly'
        }
    }
    
    # Write to cache
    cache_path = os.path.join(cache_dir, 'au_country_data.json')
    with open(cache_path, 'w') as f:
        json.dump(cache_data, f, indent=2)
    
    print(f"  ✓ Cached to {cache_path}")
    print(f"  ✓ {len(regions)} states, {len(drugs_data)} drugs")


def aggregate_uk(cache_dir):
    """Aggregate UK NHS OpenPrescribing data"""
    print("\n🇬🇧 Aggregating United Kingdom (NHS)...")
    
    data_source = UKDataSource()
    
    # Get latest period
    period = data_source.get_latest_period()
    print(f"  Period: {period}")
    
    # Aggregate by region
    regional_data = defaultdict(lambda: {'prescriptions': 0, 'cost': 0, 'prescribers': set()})
    drugs_data = []
    
    top_drugs = TOP_DRUGS['UK']
    
    for drug_name in top_drugs:
        print(f"  → Querying {drug_name}...")
        
        drug_code = data_source.find_drug_code(drug_name)
        if not drug_code:
            print(f"    ⚠️  No code found for {drug_name}")
            continue
        
        # Get prescribing data
        prescribing_data = data_source.get_prescribing_data(drug_code, period)
        
        if not prescribing_data:
            print(f"    ⚠️  No data returned")
            continue
        
        # Aggregate totals for this drug
        total_rx = sum(p.prescriptions for p in prescribing_data)
        total_cost = sum(p.cost for p in prescribing_data)
        
        drugs_data.append({
            'name': drug_name.title(),
            'prescriptions': total_rx,
            'cost': int(total_cost)
        })
        
        print(f"    ✓ {total_rx:,} prescriptions, £{total_cost:,.0f}")
        
        # Aggregate by region
        for p in prescribing_data:
            region = get_uk_region(p.prescriber.id, p.prescriber.name)
            regional_data[region]['prescriptions'] += p.prescriptions
            regional_data[region]['cost'] += p.cost
            regional_data[region]['prescribers'].add(p.prescriber.id)
    
    # Convert to list
    regions = [
        {
            'region': region,
            'prescriptions': int(data['prescriptions']),
            'cost': int(data['cost']),
            'prescribers': len(data['prescribers'])
        }
        for region, data in regional_data.items()
    ]
    
    # Sort drugs by prescriptions
    drugs_data.sort(key=lambda x: x['prescriptions'], reverse=True)
    
    # Create cache file
    cache_data = {
        'country': 'UK',
        'last_updated': datetime.now().isoformat(),
        'period': period,
        'regions': regions,
        'top_drugs': drugs_data,
        'monthly_data': None,  # TODO: Query historical data
        'metadata': {
            'source': 'NHS OpenPrescribing',
            'update_frequency': 'Daily'
        }
    }
    
    # Write to cache
    cache_path = os.path.join(cache_dir, 'uk_country_data.json')
    with open(cache_path, 'w') as f:
        json.dump(cache_data, f, indent=2)
    
    print(f"  ✓ Cached to {cache_path}")
    print(f"  ✓ {len(regions)} regions, {len(drugs_data)} drugs")


def aggregate_country(country_code, cache_dir):
    """Aggregate data for a specific country"""
    country_code = country_code.upper()
    
    if country_code == 'AU':
        aggregate_australia(cache_dir)
    elif country_code == 'UK':
        aggregate_uk(cache_dir)
    elif country_code == 'US':
        print(f"\n🇺🇸 US aggregation not yet implemented (CMS API requires more setup)")
    elif country_code in ['FR', 'JP']:
        print(f"\n{country_code} aggregation not yet implemented")
    else:
        print(f"❌ Country {country_code} not supported")


def main():
    parser = argparse.ArgumentParser(description='Aggregate country data from live sources')
    parser.add_argument('--country', help='Country code (UK, US, AU, FR, JP)')
    parser.add_argument('--all', action='store_true', help='Aggregate all countries')
    args = parser.parse_args()
    
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    print("=" * 60)
    print("Country Data Aggregator")
    print("=" * 60)
    
    if args.all:
        for country in ['AU', 'UK']:  # Start with these two
            try:
                aggregate_country(country, cache_dir)
            except Exception as e:
                print(f"❌ Error aggregating {country}: {e}")
                import traceback
                traceback.print_exc()
    elif args.country:
        aggregate_country(args.country, cache_dir)
    else:
        parser.print_help()
    
    print("\n" + "=" * 60)
    print("✓ Aggregation complete")
    print("=" * 60)


if __name__ == '__main__':
    main()
