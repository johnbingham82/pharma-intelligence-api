#!/usr/bin/env python3
"""Quick test of LA aggregation logic"""
import sys
import os
sys.path.insert(0, 'api')

from data_sources_uk import UKDataSource
from ccg_to_la_mapping import map_practice_to_la
from collections import defaultdict

print("Testing LA aggregation with atorvastatin...")

ds = UKDataSource()
drug_code = ds.find_drug_code('atorvastatin')
print(f"Drug code: {drug_code}")

# Get prescribing data
data = ds.get_prescribing_data(drug_code, '2025-10-01')
print(f"Total practices: {len(data)}")

# Take first 100 practices only for testing
sample_data = data[:100]
print(f"Testing with {len(sample_data)} practices\n")

# Map to LAs
la_data = defaultdict(lambda: {'prescriptions': 0, 'cost': 0, 'count': 0})
unmapped = 0

for p in sample_data:
    la_name = map_practice_to_la(p.prescriber.name, p.prescriber.id)
    
    if la_name:
        la_data[la_name]['prescriptions'] += p.prescriptions
        la_data[la_name]['cost'] += p.cost
        la_data[la_name]['count'] += 1
    else:
        unmapped += 1

print(f"Mapped to {len(la_data)} Local Authorities")
print(f"Unmapped: {unmapped} ({unmapped/len(sample_data)*100:.1f}%)")
print(f"\nTop 10 LAs by prescriptions:")
sorted_las = sorted(la_data.items(), key=lambda x: x[1]['prescriptions'], reverse=True)
for la_name, data in sorted_las[:10]:
    print(f"  {la_name}: {data['prescriptions']:,} Rx, £{data['cost']:,.0f} ({data['count']} practices)")
