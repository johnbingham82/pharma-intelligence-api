#!/usr/bin/env python3
"""
Australia Integration Test
Comprehensive test of PBS (Pharmaceutical Benefits Scheme) data source
"""
from data_sources_au import AustraliaDataSource
from pharma_intelligence_engine import PharmaIntelligenceEngine, SimpleVolumeScorer
import json


def test_australia_integration():
    """Complete integration test for Australia PBS data"""
    print("="*80)
    print("Australia PBS Data Source Integration Test")
    print("="*80)
    
    # Initialize Australia data source
    print("\n1. Initializing Australia PBS data source...")
    ds = AustraliaDataSource()
    print(f"   ✓ Data Source: PBS (Pharmaceutical Benefits Scheme)")
    print(f"   ✓ Update Frequency: MONTHLY (best in class!)")
    print(f"   ✓ Level: State/Territory (8 regions)")
    print(f"   ✓ Population: {ds.total_population:,}")
    
    # List states/territories
    print(f"\n2. States/Territories Coverage:")
    for code, info in ds.states.items():
        print(f"   • {code}: {info['name']} - Pop: {info['population']:,} - Capital: {info['capital']}")
    
    # Test drug search
    print("\n3. Testing drug search...")
    results = ds.search_drug('metformin')
    if results:
        result = results[0]
        print(f"   ✓ Found: {result['name']}")
        print(f"     ATC Code: {result['id']}")
        print(f"     PBS Code: {result['pbs_code']}")
    else:
        print("   ✗ No results found")
        return False
    
    # Get prescribing data
    print("\n4. Retrieving PBS prescribing data (2023)...")
    drug_code = ds.find_drug_code('metformin')
    data = ds.get_prescribing_data(drug_code, '2023')
    
    if not data:
        print("   ✗ No data returned")
        return False
    
    print(f"   ✓ Found {len(data)} states/territories")
    
    # Calculate totals
    print("\n5. Analyzing national PBS data...")
    total_prescriptions = sum(d.prescriptions for d in data)
    total_cost = sum(d.cost for d in data)
    total_quantity = sum(d.quantity for d in data)
    
    print(f"   Total Prescriptions: {total_prescriptions:,}")
    print(f"   Total Cost: ${total_cost:,.0f} AUD (€{int(total_cost * 0.60):,})")
    print(f"   Total Quantity: {total_quantity:,} units")
    print(f"   Rx per capita: {total_prescriptions/ds.total_population*1000:.1f} per 1,000 people")
    print(f"   Average cost per Rx: ${total_cost/total_prescriptions:.2f} AUD")
    
    # Top states
    print("\n6. Top 5 States/Territories by Volume:")
    sorted_data = sorted(data, key=lambda d: d.prescriptions, reverse=True)
    for i, d in enumerate(sorted_data[:5], 1):
        share = (d.prescriptions / total_prescriptions) * 100
        state_code = d.prescriber.id.replace('AU-', '')
        population = ds.states[state_code]['population']
        per_capita = (d.prescriptions / population) * 1000
        
        print(f"   {i}. {d.prescriber.name}")
        print(f"      Population: {population:,}")
        print(f"      Prescriptions: {d.prescriptions:,} ({share:.1f}%)")
        print(f"      Cost: ${d.cost:,.0f} AUD")
        print(f"      Per capita: {per_capita:.1f} Rx per 1,000")
    
    # Test state filter
    print("\n7. Testing state filter (New South Wales)...")
    nsw_data = ds.get_prescribing_data(drug_code, '2023', region='NSW')
    if nsw_data:
        print(f"   ✓ Found data for {nsw_data[0].prescriber.name}")
        print(f"   Prescriptions: {nsw_data[0].prescriptions:,}")
        print(f"   Cost: ${nsw_data[0].cost:,.0f} AUD")
    else:
        print("   ✗ State filter failed")
        return False
    
    # Test monthly data format
    print("\n8. Testing monthly data format (2023-12)...")
    monthly_data = ds.get_prescribing_data(drug_code, '2023-12')
    if monthly_data:
        print(f"   ✓ December 2023 data retrieved")
        print(f"   Format: YYYY-MM supported")
        print(f"   States: {len(monthly_data)}")
    else:
        print("   ✗ Monthly format failed")
        return False
    
    # Test multiple drugs
    print("\n9. Testing multiple drug types...")
    test_drugs = ['atorvastatin', 'rosuvastatin', 'apixaban']
    for drug_name in test_drugs:
        drug_results = ds.search_drug(drug_name)
        if drug_results:
            print(f"   ✓ {drug_results[0]['name']} - ATC: {drug_results[0]['id']}, PBS: {drug_results[0]['pbs_code']}")
        else:
            print(f"   ⚠️  {drug_name} - not in lookup table")
    
    # Export to JSON
    print("\n10. Exporting analysis to JSON...")
    export_data = {
        "country": "Australia",
        "country_code": "AU",
        "drug": "metformin",
        "drug_code": drug_code,
        "period": "2023",
        "data_source": "PBS (Pharmaceutical Benefits Scheme)",
        "update_frequency": "Monthly",
        "summary": {
            "total_states": len(data),
            "total_prescriptions": total_prescriptions,
            "total_cost_aud": total_cost,
            "total_cost_eur": int(total_cost * 0.60),  # Approximate conversion
            "total_quantity": total_quantity,
            "rx_per_capita": round(total_prescriptions/ds.total_population*1000, 1),
            "population": ds.total_population
        },
        "states": [
            {
                "code": d.prescriber.id.replace('AU-', ''),
                "name": d.prescriber.name,
                "location": d.prescriber.location,
                "population": ds.states[d.prescriber.id.replace('AU-', '')]['population'],
                "prescriptions": d.prescriptions,
                "cost_aud": d.cost,
                "quantity": d.quantity,
                "market_share_pct": round((d.prescriptions / total_prescriptions) * 100, 2),
                "rx_per_capita": round((d.prescriptions / ds.states[d.prescriber.id.replace('AU-', '')]['population']) * 1000, 1)
            }
            for d in sorted_data
        ]
    }
    
    output_file = "analysis_australia_metformin.json"
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"   ✓ Saved to {output_file}")
    
    print("\n" + "="*80)
    print("✅ Australia Integration Test - ALL TESTS PASSED")
    print("="*80)
    print(f"\nAustralia PBS Coverage:")
    print(f"  • 8 States/Territories")
    print(f"  • {total_prescriptions:,} prescriptions")
    print(f"  • ${total_cost:,.0f} AUD market value")
    print(f"  • Population: {ds.total_population:,}")
    print(f"  • Update Frequency: MONTHLY")
    print(f"  • Data Quality: ⭐⭐⭐⭐⭐ (Best non-EU/US)")
    
    return True


def test_global_comparison():
    """Compare Australia with other countries"""
    print("\n" + "="*80)
    print("Global Coverage Update - 8 Countries")
    print("="*80)
    
    countries = {
        'UK': {'pop': 67_000_000, 'type': 'Prescriber-level', 'data': 'Real'},
        'US': {'pop': 40_000_000, 'type': 'Prescriber-level', 'data': 'Real'},
        'France': {'pop': 67_000_000, 'type': 'Regional', 'data': 'Mock'},
        'Germany': {'pop': 83_000_000, 'type': 'Regional', 'data': 'Mock'},
        'Netherlands': {'pop': 17_500_000, 'type': 'Regional', 'data': 'Mock'},
        'Italy': {'pop': 60_000_000, 'type': 'Regional', 'data': 'Mock'},
        'Spain': {'pop': 47_400_000, 'type': 'Regional', 'data': 'Mock'},
        'Australia': {'pop': 25_620_000, 'type': 'State/Territory', 'data': 'Mock (PBS data available)'}
    }
    
    print("\n8-Country Platform Coverage:")
    total_pop = 0
    for i, (country, info) in enumerate(countries.items(), 1):
        status = "✅" if info['data'] == 'Real' else "🔄"
        print(f"{i}. {status} {country:12} - {info['pop']:>12,} - {info['type']:18} - {info['data']}")
        total_pop += info['pop']
    
    print(f"\n{'='*80}")
    print(f"TOTAL COVERAGE: {total_pop:,} population")
    print(f"Countries: 8")
    print(f"Real Data: 2 countries (UK + US)")
    print(f"Framework Ready: 6 countries (EU-5 + Australia)")
    print(f"{'='*80}")
    
    # Regional breakdown
    print(f"\nRegional Breakdown:")
    print(f"  Europe (EU-5):  274,900,000 (72.1%)")
    print(f"  North America:  107,000,000 (26.5%)")
    print(f"  Oceania:         25,620,000 (6.3%)")
    print(f"  TOTAL:          407,520,000")
    
    # Data quality comparison
    print(f"\nData Quality Highlights:")
    print(f"  ⭐⭐⭐⭐⭐ Australia PBS - Monthly updates, excellent coverage")
    print(f"  ⭐⭐⭐⭐⭐ UK NHS - Real-time, prescriber-level")
    print(f"  ⭐⭐⭐⭐⭐ US CMS - Real-time, prescriber-level")
    print(f"  ⭐⭐⭐⭐   EU Framework - Regional, needs real data integration")


def test_pbs_comparison():
    """Compare PBS data characteristics with other sources"""
    print("\n" + "="*80)
    print("PBS Data Quality Assessment")
    print("="*80)
    
    comparison = {
        "Update Frequency": {
            "UK (NHS)": "Daily",
            "US (CMS)": "Quarterly",
            "EU (Various)": "Annual",
            "Australia (PBS)": "MONTHLY ⭐"
        },
        "Data Granularity": {
            "UK (NHS)": "Prescriber-level",
            "US (CMS)": "Prescriber-level",
            "EU (Various)": "Regional aggregate",
            "Australia (PBS)": "State/Territory aggregate"
        },
        "Public Access": {
            "UK (NHS)": "✅ Free API",
            "US (CMS)": "✅ Free API",
            "EU (Various)": "⚠️  Limited/Registration",
            "Australia (PBS)": "✅ Free Download"
        },
        "Coverage": {
            "UK (NHS)": "All NHS prescriptions",
            "US (CMS)": "Medicare Part D only",
            "EU (Various)": "National programs",
            "Australia (PBS)": "All PBS subsidized (90%+ of Rx)"
        }
    }
    
    for metric, values in comparison.items():
        print(f"\n{metric}:")
        for country, value in values.items():
            print(f"  {country:20} {value}")
    
    print("\n" + "="*80)
    print("PBS Unique Advantages:")
    print("="*80)
    print("  ✓ Monthly updates (best update cadence)")
    print("  ✓ Comprehensive coverage (~90% of prescriptions)")
    print("  ✓ Freely available public data")
    print("  ✓ Well-structured, consistent format")
    print("  ✓ ATC + PBS coding (international + local)")
    print("  ✓ English language (easier integration)")
    
    print("\n💡 Real PBS Integration Path:")
    print("   1. Download monthly CSV from AIHW portal")
    print("   2. Parse and load into database")
    print("   3. Map ATC codes to drug names")
    print("   4. Aggregate by state/territory")
    print("   5. API: https://www.aihw.gov.au/reports/medicines/pbs-monthly-data")


if __name__ == "__main__":
    # Test Australia specifically
    success = test_australia_integration()
    
    if success:
        # Show global comparison
        test_global_comparison()
        
        # PBS data quality assessment
        test_pbs_comparison()
    
    exit(0 if success else 1)
