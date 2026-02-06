#!/usr/bin/env python3
"""Quick test of postcode-based LA aggregation"""
import sys
import os
import json
sys.path.insert(0, 'api')

from data_sources_uk import UKDataSource
from postcode_geocoding import PostcodeGeocoder
from collections import defaultdict

print("Testing postcode-based LA aggregation...\n")

ds = UKDataSource()
geocoder = PostcodeGeocoder()

drug_code = ds.find_drug_code('atorvastatin')
print(f"Drug code: {drug_code}")

# Get prescribing data
data = ds.get_prescribing_data(drug_code, '2025-10-01')
print(f"Total practices: {len(data)}\n")

# Test with first 50 practices
sample_data = data[:50]
print(f"Testing with {len(sample_data)} practices\n")

# Map to LAs using postcodes
la_data = defaultdict(lambda: {'prescriptions': 0, 'cost': 0, 'count': 0})
practice_locations = {}
unmapped = 0

for i, p in enumerate(sample_data):
    if (i + 1) % 10 == 0:
        print(f"  Progress: {i+1}/{len(sample_data)}")
    
    location = geocoder.get_practice_location_and_la(p.prescriber.id)
    
    if location and location.get('la_name'):
        la_name = location['la_name']
        la_data[la_name]['prescriptions'] += p.prescriptions
        la_data[la_name]['cost'] += p.cost
        la_data[la_name]['count'] += 1
        
        # Store location
        practice_locations[p.prescriber.id] = {
            'name': p.prescriber.name,
            'lat': location['lat'],
            'lng': location['lng'],
            'postcode': location['postcode'],
            'la': la_name
        }
    else:
        unmapped += 1

print(f"\n✓ Mapped to {len(la_data)} Local Authorities")
print(f"✓ Geocoded {len(practice_locations)} practice locations")
print(f"⚠️  Unmapped: {unmapped} ({unmapped/len(sample_data)*100:.1f}%)")

print(f"\nTop 10 LAs by prescriptions:")
sorted_las = sorted(la_data.items(), key=lambda x: x[1]['prescriptions'], reverse=True)
for la_name, data in sorted_las[:10]:
    print(f"  {la_name}: {data['prescriptions']:,} Rx, £{data['cost']:,.0f} ({data['count']} practices)")

print(f"\nSample practice locations:")
for i, (code, loc) in enumerate(list(practice_locations.items())[:5]):
    print(f"  {code}: {loc['name'][:30]:30s} | {loc['postcode']:8s} | {loc['la']:20s} | {loc['lat']:.4f}, {loc['lng']:.4f}")
