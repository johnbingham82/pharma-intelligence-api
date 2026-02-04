#!/usr/bin/env python3
"""
Global Analysis Demo
Demonstrates multi-country analysis with UK, US, and EU data sources
"""
from pharma_intelligence_engine import (
    PharmaIntelligenceEngine,
    create_drug,
    MarketShareScorer
)
from data_sources_uk import UKDataSource
from data_sources_us import USDataSource
from data_sources_eu import EUDataSource


def analyze_drug_globally(drug_name: str, generic_name: str, 
                         therapeutic_area: str, company: str):
    """
    Analyze a drug across multiple countries
    
    Args:
        drug_name: Brand name
        generic_name: Generic name
        therapeutic_area: Therapeutic category
        company: Pharma company
    """
    print("\n" + "="*80)
    print(f"GLOBAL ANALYSIS: {drug_name} ({generic_name})")
    print(f"Company: {company} | Therapeutic Area: {therapeutic_area}")
    print("="*80)
    
    # Initialize data sources
    data_sources = {
        'UK': UKDataSource(),
        'US': USDataSource(),
        'FR': EUDataSource('FR'),
        'DE': EUDataSource('DE')
    }
    
    results = {}
    
    for country_code, data_source in data_sources.items():
        print(f"\n{'#'*80}")
        print(f"Analyzing: {country_code}")
        print(f"{'#'*80}")
        
        try:
            # Find drug code for this country
            drug_code = data_source.find_drug_code(generic_name)
            
            if not drug_code:
                print(f"⚠️  Drug not found in {country_code}")
                continue
            
            print(f"Drug code: {drug_code}")
            
            # Create drug object
            drug = create_drug(
                name=drug_name,
                generic_name=generic_name,
                therapeutic_area=therapeutic_area,
                company=company,
                country_codes={country_code: drug_code}
            )
            
            # Run analysis
            engine = PharmaIntelligenceEngine(
                data_source=data_source,
                scorer=MarketShareScorer()
            )
            
            report = engine.analyze_drug(
                drug=drug,
                country=country_code,
                top_n=10  # Top 10 only for demo
            )
            
            results[country_code] = report
            
        except Exception as e:
            print(f"\n❌ Error analyzing {country_code}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Cross-country comparison
    print("\n" + "="*80)
    print("GLOBAL MARKET SUMMARY")
    print("="*80 + "\n")
    
    print(f"{'Country':<15} {'Level':<20} {'Prescribers':<15} {'Total Volume':<15} {'Total Cost'}")
    print("-" * 80)
    
    total_prescribers = 0
    total_volume = 0
    total_cost = 0
    
    for country_code, report in results.items():
        if report:
            summary = report['market_summary']
            
            # Determine analysis level
            if country_code in ['UK', 'US']:
                level = 'Prescriber'
            else:
                level = 'Regional/Aggregate'
            
            prescribers = summary['total_prescribers']
            volume = summary['total_prescriptions']
            cost = summary['total_cost']
            
            print(f"{country_code:<15} {level:<20} {prescribers:<15,} {volume:<15,} ${cost:,.0f}")
            
            total_prescribers += prescribers
            total_volume += volume
            total_cost += cost
    
    print("-" * 80)
    print(f"{'TOTAL':<15} {'Mixed':<20} {total_prescribers:<15,} {total_volume:<15,} ${total_cost:,.0f}")
    
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    
    if results:
        print(f"\n✓ Analyzed {len(results)} markets")
        print(f"✓ Total addressable prescribers/regions: {total_prescribers:,}")
        print(f"✓ Total market volume: {total_volume:,} prescriptions")
        print(f"✓ Total market value: ${total_cost:,.0f}")
        
        # Find largest market
        largest_market = max(results.items(), 
                           key=lambda x: x[1]['market_summary']['total_prescriptions'])
        print(f"✓ Largest market: {largest_market[0]} "
              f"({largest_market[1]['market_summary']['total_prescriptions']:,} prescriptions)")
    
    print()
    
    return results


def main():
    print("\n" + "="*80)
    print("PHARMA INTELLIGENCE PLATFORM - GLOBAL ANALYSIS DEMO")
    print("="*80)
    print("\nDemonstrating multi-country analysis")
    print("Coverage: UK, US (Medicare), France, Germany")
    print()
    
    # Analyze Metformin (widely prescribed, available in all markets)
    results = analyze_drug_globally(
        drug_name="Metformin",
        generic_name="metformin",
        therapeutic_area="Diabetes - Type 2",
        company="Generic"
    )
    
    print("\n" + "="*80)
    print("✅ GLOBAL ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nAnalyzed {len(results)} countries")
    print("Individual reports saved as: analysis_<drug>_<country>_<period>.json\n")


if __name__ == "__main__":
    main()
