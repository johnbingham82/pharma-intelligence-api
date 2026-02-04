#!/usr/bin/env python3
"""
Leqvio Competitive Analysis
Compare Leqvio vs competitor PCSK9 inhibitors and statins
"""
import sys
sys.path.append('/Users/administrator/.openclaw/workspace')
from gp_profiler import GPProfiler

profiler = GPProfiler()

print("\n" + "="*70)
print("LEQVIO (INCLISIRAN) COMPETITIVE INTELLIGENCE")
print("PCSK9 Inhibitor Market Analysis")
print("="*70)

# Analyze each drug in the therapeutic class
drugs = {
    'leqvio': 'inclisiran',
    'repatha': 'evolocumab', 
    'praluent': 'alirocumab',
    'high_intensity_statin': 'atorvastatin'  # As reference
}

results = {}

for brand, generic in drugs.items():
    print(f"\n{'='*70}")
    print(f"Analyzing {brand.upper()} ({generic})")
    print(f"{'='*70}")
    
    opportunities = profiler.analyze_therapeutic_area(
        drug_name=generic,
        region_code=None
    )
    
    if opportunities:
        results[brand] = {
            'practices': len(opportunities),
            'top_20': opportunities[:20]
        }

# Comparative summary
print("\n" + "="*70)
print("🎯 COMPETITIVE SUMMARY")
print("="*70)

for brand, data in results.items():
    if data:
        print(f"\n{brand.upper()}:")
        print(f"  Total Prescribing Practices: {data['practices']:,}")
        if data['top_20']:
            top_practice = data['top_20'][0]
            print(f"  Highest Volume Practice: {top_practice['name'][:40]}")
            print(f"  Top Practice Prescriptions: {top_practice['items']:,}")

print("\n" + "="*70)
print("💡 STRATEGIC INSIGHTS")
print("="*70)
print("""
Key Questions for Your Sales Team:
1. Which high-volume statin practices aren't using any PCSK9 inhibitor?
2. Which practices use Repatha/Praluent but not Leqvio? (switch opportunity)
3. Which ICBs have formulary restrictions on Leqvio?
4. What's the patient overlap potential (statin → PCSK9i pathway)?
""")
