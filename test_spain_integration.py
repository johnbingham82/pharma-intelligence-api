#!/usr/bin/env python3
"""
Spain Integration Test
Verify Spain data source is fully operational
"""
from data_sources_eu import EUDataSource
from pharma_intelligence_engine import PharmaIntelligenceEngine, SimpleVolumeScorer
import json


def test_spain_integration():
    """Complete integration test for Spain"""
    print("="*80)
    print("Spain Data Source Integration Test")
    print("="*80)
    
    # Initialize Spain data source
    print("\n1. Initializing Spain data source...")
    ds = EUDataSource('ES')
    print(f"   ✓ Data Source: {ds.config['ES']['data_source']}")
    print(f"   ✓ Level: {ds.config['ES']['level']}")
    print(f"   ✓ Population: {ds.config['ES']['population']:,}")
    
    # Test drug search
    print("\n2. Testing drug search...")
    results = ds.search_drug('metformin')
    if results:
        print(f"   ✓ Found: {results[0]['name']} (Code: {results[0]['id']})")
    else:
        print("   ✗ No results found")
        return False
    
    # Get prescribing data
    print("\n3. Retrieving regional prescribing data...")
    drug_code = ds.find_drug_code('metformin')
    data = ds.get_prescribing_data(drug_code, '2022')
    
    if not data:
        print("   ✗ No data returned")
        return False
    
    print(f"   ✓ Found {len(data)} Autonomous Communities")
    
    # Calculate totals
    print("\n4. Analyzing market data...")
    total_prescriptions = sum(d.prescriptions for d in data)
    total_cost = sum(d.cost for d in data)
    avg_per_region = total_prescriptions // len(data)
    
    print(f"   Total Prescriptions: {total_prescriptions:,}")
    print(f"   Total Cost: €{total_cost:,.0f}")
    print(f"   Average per Region: {avg_per_region:,}")
    print(f"   Cost per Prescription: €{total_cost/total_prescriptions:.2f}")
    
    # Top regions
    print("\n5. Top 5 Autonomous Communities by Volume:")
    for i, d in enumerate(data[:5], 1):
        share = (d.prescriptions / total_prescriptions) * 100
        print(f"   {i}. {d.prescriber.name}")
        print(f"      Prescriptions: {d.prescriptions:,} ({share:.1f}%)")
        print(f"      Cost: €{d.cost:,.0f}")
    
    # Test specific region filter
    print("\n6. Testing region filter (Andalucía - AN)...")
    andalucia_data = ds.get_prescribing_data(drug_code, '2022', region='AN')
    if andalucia_data:
        print(f"   ✓ Found data for {andalucia_data[0].prescriber.name}")
        print(f"   Prescriptions: {andalucia_data[0].prescriptions:,}")
    else:
        print("   ✗ Region filter failed")
        return False
    
    # Export to JSON
    print("\n7. Exporting analysis to JSON...")
    export_data = {
        "country": "Spain",
        "country_code": "ES",
        "drug": "metformin",
        "drug_code": drug_code,
        "period": "2022",
        "summary": {
            "total_regions": len(data),
            "total_prescriptions": total_prescriptions,
            "total_cost_eur": total_cost,
            "avg_per_region": avg_per_region
        },
        "regions": [
            {
                "code": d.prescriber.id,
                "name": d.prescriber.name,
                "location": d.prescriber.location,
                "prescriptions": d.prescriptions,
                "cost_eur": d.cost,
                "market_share_pct": round((d.prescriptions / total_prescriptions) * 100, 2)
            }
            for d in data
        ]
    }
    
    output_file = "analysis_spain_metformin.json"
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"   ✓ Saved to {output_file}")
    
    print("\n" + "="*80)
    print("✅ Spain Integration Test - ALL TESTS PASSED")
    print("="*80)
    print(f"\nSpain Coverage:")
    print(f"  • 17 Autonomous Communities")
    print(f"  • {total_prescriptions:,} prescriptions")
    print(f"  • €{total_cost:,.0f} market value")
    print(f"  • Population: 47.4M")
    
    return True


def test_eu5_summary():
    """Summary of EU-5 major markets"""
    print("\n" + "="*80)
    print("EU-5 Major Markets Summary")
    print("="*80)
    
    countries = {
        'FR': 'France',
        'DE': 'Germany',
        'IT': 'Italy',
        'ES': 'Spain',
        'NL': 'Netherlands'
    }
    
    eu5_data = {}
    
    for code, name in countries.items():
        ds = EUDataSource(code)
        drug_code = ds.find_drug_code('metformin')
        data = ds.get_prescribing_data(drug_code, '2022')
        
        total_rx = sum(d.prescriptions for d in data)
        total_cost = sum(d.cost for d in data)
        
        eu5_data[name] = {
            'code': code,
            'regions': len(data),
            'prescriptions': total_rx,
            'cost': total_cost,
            'population': ds.config[code]['population']
        }
    
    # Sort by prescriptions
    sorted_countries = sorted(eu5_data.items(), key=lambda x: x[1]['prescriptions'], reverse=True)
    
    print("\nRanking by Volume:")
    for i, (country, stats) in enumerate(sorted_countries, 1):
        print(f"\n{i}. {country} ({stats['code']})")
        print(f"   Population: {stats['population']:,}")
        print(f"   Regions: {stats['regions']}")
        print(f"   Prescriptions: {stats['prescriptions']:,}")
        print(f"   Cost: €{stats['cost']:,.0f}")
        print(f"   Rx per capita: {stats['prescriptions']/stats['population']*1000:.1f} per 1,000 people")
    
    # EU-5 Totals
    total_pop = sum(s['population'] for s in eu5_data.values())
    total_rx = sum(s['prescriptions'] for s in eu5_data.values())
    total_cost = sum(s['cost'] for s in eu5_data.values())
    
    print("\n" + "="*80)
    print("EU-5 TOTALS")
    print("="*80)
    print(f"Combined Population: {total_pop:,}")
    print(f"Total Prescriptions: {total_rx:,}")
    print(f"Total Cost: €{total_cost:,.0f}")
    print(f"Average Rx per capita: {total_rx/total_pop*1000:.1f} per 1,000 people")
    print(f"\n✅ EU-5 Major Markets Complete!")


if __name__ == "__main__":
    # Test Spain specifically
    success = test_spain_integration()
    
    if success:
        # Show EU-5 summary
        test_eu5_summary()
    
    exit(0 if success else 1)
