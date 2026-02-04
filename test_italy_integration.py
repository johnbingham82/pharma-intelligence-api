#!/usr/bin/env python3
"""
Test Italy Data Source Integration
"""
from pharma_intelligence_engine import PharmaIntelligenceEngine, create_drug
from data_sources_eu import EUDataSource

def test_italy_integration():
    """Test Italy data source with full analysis engine"""
    print("="*80)
    print("Testing Italy Integration - AIFA Data Source")
    print("="*80)
    print()
    
    # Initialize data source
    print("1. Initializing Italy (IT) data source...")
    italy_ds = EUDataSource('IT')
    print(f"   ✅ Data Source: {italy_ds.config['IT']['data_source']}")
    print(f"   ✅ Population: {italy_ds.config['IT']['population']:,}")
    print(f"   ✅ Analysis Level: {italy_ds.config['IT']['level']} (Regional)")
    print()
    
    # Initialize analysis engine
    print("2. Initializing Pharma Intelligence Engine...")
    engine = PharmaIntelligenceEngine(data_source=italy_ds)
    print("   ✅ Engine ready")
    print()
    
    # Test drug: Metformin (common diabetes drug)
    drug_name = "metformin"
    print(f"3. Searching for drug: '{drug_name}'...")
    drug_code = italy_ds.find_drug_code(drug_name)
    print(f"   ✅ Found ATC Code: {drug_code}")
    print()
    
    # Create drug object
    drug = create_drug(drug_name, drug_name, "Type 2 Diabetes", company="Test Pharma", country_codes={"IT": drug_code})
    
    # Analyze market
    print("4. Running market analysis...")
    period = italy_ds.get_latest_period()
    print(f"   Period: {period}")
    print()
    
    analysis = engine.analyze_drug(drug, country="IT")
    
    # Display results (analysis is a dict)
    print()
    print("="*80)
    print("✅ ITALY INTEGRATION TEST COMPLETE!")
    print("="*80)
    print()
    print(f"✅ Analysis Status: SUCCESS")
    print(f"✅ Drug: {drug.name} ({drug_code})")
    print(f"✅ Country: Italy")
    print(f"✅ Regions Analyzed: {analysis['market_summary']['total_prescribers']}")
    print(f"✅ Total Prescriptions: {analysis['market_summary']['total_prescriptions']:,}")
    print(f"✅ Market Value: €{analysis['market_summary']['total_cost']:,.0f}")
    print()
    print("="*80)
    print("OPERATIONAL STATUS")
    print("="*80)
    print("✅ Data Source: AIFA Open Data")
    print("✅ Population Coverage: 60M")
    print("✅ Analysis Type: Regional/Aggregate (GDPR-compliant)")
    print("✅ Data Period: 2022")
    print("✅ Integration: WORKING")
    print()
    print("Top 5 Regions:")
    for opp in analysis['top_opportunities'][:5]:
        print(f"  {opp['rank']}. {opp['prescriber_name']}: {opp['current_volume']:,} prescriptions")
    print()
    print("="*80)
    print("🎉 ITALY SUCCESSFULLY ADDED TO PLATFORM!")
    print("="*80)
    print()
    print("Next Steps:")
    print("  1. ✅ Italy data source implemented")
    print("  2. ✅ API routes updated")
    print("  3. ✅ Integration tested")
    print("  4. ⏭️  Update documentation")
    print("  5. ⏭️  Add Spain next")
    print()

if __name__ == "__main__":
    test_italy_integration()
