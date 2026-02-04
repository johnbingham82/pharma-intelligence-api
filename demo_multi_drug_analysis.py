#!/usr/bin/env python3
"""
Multi-Drug Analysis Demo
Demonstrates the generalized engine with various therapeutic areas
"""
from pharma_intelligence_engine import (
    PharmaIntelligenceEngine,
    create_drug,
    MarketShareScorer,
    SimpleVolumeScorer
)
from data_sources_uk import UKDataSource

def main():
    print("\n" + "="*80)
    print("PHARMA INTELLIGENCE ENGINE - MULTI-DRUG DEMO")
    print("="*80)
    print("\nDemonstrating drug-agnostic analysis across therapeutic areas\n")
    
    # Initialize engine
    uk_data = UKDataSource()
    engine = PharmaIntelligenceEngine(
        data_source=uk_data,
        scorer=MarketShareScorer()
    )
    
    # Define various drugs across different therapeutic areas
    drugs = [
        # Cardiovascular
        create_drug(
            name="Inclisiran",
            generic_name="inclisiran",
            therapeutic_area="Cardiovascular - Lipid Management",
            company="Novartis",
            country_codes={'UK': uk_data.find_drug_code('inclisiran')}
        ),
        
        # Diabetes
        create_drug(
            name="Metformin",
            generic_name="metformin",
            therapeutic_area="Diabetes - Type 2",
            company="Generic",
            country_codes={'UK': uk_data.find_drug_code('metformin')}
        ),
        
        # Oncology
        create_drug(
            name="Pembrolizumab",
            generic_name="pembrolizumab",
            therapeutic_area="Oncology - Immunotherapy",
            company="MSD",
            country_codes={'UK': uk_data.find_drug_code('pembrolizumab')}
        ),
        
        # Respiratory
        create_drug(
            name="Salbutamol",
            generic_name="salbutamol",
            therapeutic_area="Respiratory - Asthma/COPD",
            company="Generic",
            country_codes={'UK': uk_data.find_drug_code('salbutamol')}
        ),
        
        # Cardiovascular (different class)
        create_drug(
            name="Atorvastatin",
            generic_name="atorvastatin",
            therapeutic_area="Cardiovascular - Lipid Management",
            company="Generic (originally Pfizer)",
            country_codes={'UK': uk_data.find_drug_code('atorvastatin')}
        )
    ]
    
    # Filter out drugs where we couldn't find codes
    valid_drugs = [d for d in drugs if d.country_codes.get('UK')]
    
    print(f"Found valid drug codes for {len(valid_drugs)}/{len(drugs)} drugs\n")
    
    # Analyze each drug
    results = {}
    
    for i, drug in enumerate(valid_drugs, 1):
        print(f"\n{'#'*80}")
        print(f"ANALYSIS {i}/{len(valid_drugs)}")
        print(f"{'#'*80}")
        
        try:
            result = engine.analyze_drug(
                drug=drug,
                country='UK',
                top_n=20
            )
            
            results[drug.name] = result
            
            # Brief pause between API calls to be respectful
            if i < len(valid_drugs):
                print("\n⏸️  Pausing 2 seconds before next analysis...\n")
                import time
                time.sleep(2)
                
        except Exception as e:
            print(f"\n❌ Error analyzing {drug.name}: {e}\n")
            continue
    
    # Summary comparison
    print("\n" + "="*80)
    print("CROSS-DRUG COMPARISON")
    print("="*80 + "\n")
    
    print(f"{'Drug':<25} {'Therapeutic Area':<35} {'Prescribers':<15} {'Total Volume'}")
    print("-" * 80)
    
    for drug_name, result in results.items():
        if result:
            summary = result['market_summary']
            ta = result['drug']['therapeutic_area']
            print(f"{drug_name:<25} {ta:<35} "
                  f"{summary['total_prescribers']:<15,} "
                  f"{summary['total_prescriptions']:,}")
    
    print("\n" + "="*80)
    print("✅ MULTI-DRUG ANALYSIS COMPLETE")
    print("="*80)
    print(f"\n{len(results)} drugs analyzed successfully")
    print("Individual reports saved as: analysis_<drug>_UK_<period>.json\n")
    
    return results

if __name__ == "__main__":
    main()
