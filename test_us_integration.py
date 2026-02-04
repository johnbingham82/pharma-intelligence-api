#!/usr/bin/env python3
"""
Quick test of US data source integration
"""
from pharma_intelligence_engine import PharmaIntelligenceEngine, create_drug
from data_sources_us import USDataSource

print("\n" + "="*80)
print("TESTING US DATA SOURCE INTEGRATION")
print("="*80)

# Initialize US data source
print("\n1. Initializing US data source...")
us_data = USDataSource()
print("   ✅ US data source initialized")

# Find a drug
print("\n2. Finding drug code for 'metformin'...")
drug_code = us_data.find_drug_code("metformin")
print(f"   ✅ Found: {drug_code}")

# Create drug object
print("\n3. Creating drug object...")
drug = create_drug(
    name="Metformin",
    generic_name="metformin",
    therapeutic_area="Diabetes - Type 2",
    company="Generic",
    country_codes={'US': drug_code}
)
print(f"   ✅ Drug created: {drug.name}")

# Initialize engine
print("\n4. Initializing intelligence engine...")
engine = PharmaIntelligenceEngine(data_source=us_data)
print("   ✅ Engine initialized")

# Run analysis (small sample for speed)
print("\n5. Running analysis (top 10 prescribers)...")
print("   ⏳ Fetching Medicare Part D data...\n")

try:
    report = engine.analyze_drug(
        drug=drug,
        country='US',
        top_n=10
    )
    
    print("\n" + "="*80)
    print("✅ SUCCESS! US INTEGRATION WORKING")
    print("="*80)
    print(f"\n📊 Results:")
    print(f"   Total Prescribers: {report['market_summary']['total_prescribers']:,}")
    print(f"   Total Prescriptions: {report['market_summary']['total_prescriptions']:,}")
    print(f"   Total Cost: ${report['market_summary']['total_cost']:,.0f}")
    
    if report['top_opportunities']:
        print(f"\n🎯 Top Opportunity:")
        top = report['top_opportunities'][0]
        print(f"   Prescriber: {top['prescriber_name']}")
        print(f"   Location: {top['location']}")
        print(f"   Prescriptions: {top['current_volume']:,}")
        print(f"   Score: {top['opportunity_score']:.1f}")
    
    print(f"\n💾 Report saved: {drug.name}_US_{report['period']}.json")
    print()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
