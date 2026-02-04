#!/usr/bin/env python3
"""
Test France, Germany, and Netherlands Data Sources
Verify all three EU countries are operational before adding Spain
"""
from data_sources_eu import EUDataSource
from pharma_intelligence_engine import PharmaIntelligenceEngine, SimpleVolumeScorer


def test_country(country_code: str, country_name: str):
    """Test a single EU country"""
    print(f"\n{'='*80}")
    print(f"Testing {country_name} ({country_code})")
    print('='*80)
    
    try:
        # Initialize data source
        ds = EUDataSource(country_code)
        
        # Test 1: Drug search
        print(f"\n✓ Test 1: Drug Search")
        results = ds.search_drug('metformin')
        if results:
            print(f"  Found: {results[0]['name']} (Code: {results[0]['id']})")
        else:
            print(f"  ⚠️  No results found")
            return False
        
        # Test 2: Get prescribing data
        print(f"\n✓ Test 2: Regional Data Retrieval")
        drug_code = ds.find_drug_code('metformin')
        data = ds.get_prescribing_data(drug_code, '2022')
        
        if not data:
            print(f"  ⚠️  No prescribing data returned")
            return False
        
        print(f"  Found {len(data)} regions")
        
        # Test 3: Data quality check
        print(f"\n✓ Test 3: Data Quality Check")
        total_prescriptions = sum(d.prescriptions for d in data)
        total_cost = sum(d.cost for d in data)
        
        print(f"  Total Prescriptions: {total_prescriptions:,}")
        print(f"  Total Cost: €{total_cost:,.0f}")
        print(f"  Average per Region: {total_prescriptions // len(data):,} prescriptions")
        
        # Test 4: Top regions
        print(f"\n✓ Test 4: Top 3 Regions by Volume")
        for i, d in enumerate(data[:3], 1):
            print(f"  {i}. {d.prescriber.name}: {d.prescriptions:,} Rx, €{d.cost:,.0f}")
        
        # Test 5: Integration with analysis engine
        print(f"\n✓ Test 5: Engine Integration Test")
        engine = PharmaIntelligenceEngine(
            data_source=ds,
            scorer=SimpleVolumeScorer()
        )
        
        result = engine.analyze('metformin', '2022')
        
        print(f"  Analysis Complete:")
        print(f"  - Country: {result.country}")
        print(f"  - Regions Analyzed: {result.total_prescribers}")
        print(f"  - Opportunities: {len(result.opportunities)}")
        print(f"  - Recommendations: {len(result.recommendations)}")
        
        if result.opportunities:
            top_opp = result.opportunities[0]
            print(f"  - Top Opportunity: {top_opp.prescriber_name} (Score: {top_opp.opportunity_score:.1f})")
        
        print(f"\n✅ {country_name} - ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ {country_name} - TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Test all three existing EU countries"""
    print("="*80)
    print("EU Country Integration Tests")
    print("Testing: France, Germany, Netherlands")
    print("="*80)
    
    countries = [
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('NL', 'Netherlands')
    ]
    
    results = {}
    for code, name in countries:
        results[name] = test_country(code, name)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All EU countries operational - Ready to add Spain!")
    else:
        print("\n⚠️  Some tests failed - fix issues before adding Spain")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
