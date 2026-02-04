#!/usr/bin/env python3
"""
Australia Data Source - PBS (Pharmaceutical Benefits Scheme)
Implements DataSource interface for Australian prescribing data

Data Source: Australian Institute of Health and Welfare (AIHW)
URL: https://www.aihw.gov.au/reports/medicines/pbs-monthly-data
Update Frequency: MONTHLY (best update cadence found!)

Coverage: All PBS-subsidized prescriptions in Australia
Data Type: Regional/aggregate (State/Territory level)
"""
import requests
from typing import List, Dict, Optional
from pharma_intelligence_engine import (
    DataSource, PrescribingData, Prescriber
)


class AustraliaDataSource(DataSource):
    """
    Australian PBS prescribing data - State/Territory level
    
    PBS (Pharmaceutical Benefits Scheme) provides subsidized medications
    to all Australians. Data published monthly by AIHW.
    
    8 States/Territories:
    - New South Wales (NSW)
    - Victoria (VIC)
    - Queensland (QLD)
    - Western Australia (WA)
    - South Australia (SA)
    - Tasmania (TAS)
    - Australian Capital Territory (ACT)
    - Northern Territory (NT)
    """
    
    def __init__(self):
        self.cache = {}
        self.base_url = "https://www.aihw.gov.au/reports/medicines/pbs-monthly-data"
        
        # State/Territory configuration
        self.states = {
            'NSW': {
                'name': 'New South Wales',
                'population': 8_166_000,
                'capital': 'Sydney'
            },
            'VIC': {
                'name': 'Victoria',
                'population': 6_613_000,
                'capital': 'Melbourne'
            },
            'QLD': {
                'name': 'Queensland',
                'population': 5_185_000,
                'capital': 'Brisbane'
            },
            'WA': {
                'name': 'Western Australia',
                'population': 2_667_000,
                'capital': 'Perth'
            },
            'SA': {
                'name': 'South Australia',
                'population': 1_771_000,
                'capital': 'Adelaide'
            },
            'TAS': {
                'name': 'Tasmania',
                'population': 541_000,
                'capital': 'Hobart'
            },
            'ACT': {
                'name': 'Australian Capital Territory',
                'population': 431_000,
                'capital': 'Canberra'
            },
            'NT': {
                'name': 'Northern Territory',
                'population': 246_000,
                'capital': 'Darwin'
            }
        }
        
        self.total_population = 25_620_000
    
    def search_drug(self, name: str) -> List[Dict]:
        """
        Search for drug codes by name
        
        Australia uses ATC codes (WHO standard) + PBS codes
        """
        # Common ATC codes for major drugs
        atc_lookup = {
            'metformin': [
                {'id': 'A10BA02', 'name': 'Metformin', 'type': 'atc', 'pbs_code': '2338B'},
            ],
            'atorvastatin': [
                {'id': 'C10AA05', 'name': 'Atorvastatin', 'type': 'atc', 'pbs_code': '8275K'},
            ],
            'inclisiran': [
                {'id': 'C10AX16', 'name': 'Inclisiran', 'type': 'atc', 'pbs_code': 'NEW'},
            ],
            'rosuvastatin': [
                {'id': 'C10AA07', 'name': 'Rosuvastatin', 'type': 'atc', 'pbs_code': '8913L'},
            ],
            'apixaban': [
                {'id': 'B01AF02', 'name': 'Apixaban', 'type': 'atc', 'pbs_code': '10447W'},
            ],
            'empagliflozin': [
                {'id': 'A10BK03', 'name': 'Empagliflozin', 'type': 'atc', 'pbs_code': '11082T'},
            ]
        }
        
        name_lower = name.lower()
        if name_lower in atc_lookup:
            return atc_lookup[name_lower]
        
        # Fuzzy match
        for drug, codes in atc_lookup.items():
            if name_lower in drug or drug in name_lower:
                return codes
        
        return []
    
    def get_prescribing_data(self, drug_code: str, period: str,
                           region: Optional[str] = None) -> List[PrescribingData]:
        """
        Get PBS prescribing data by State/Territory
        
        Args:
            drug_code: ATC code or drug name
            period: Year-Month (e.g., "2023-12") or Year (e.g., "2023")
            region: Optional state code (NSW, VIC, etc.)
            
        Returns:
            List of PrescribingData objects (one per state/territory)
        """
        print(f"⚠️  MOCK DATA: Australia PBS analysis for {drug_code}")
        print(f"   Real implementation requires AIHW PBS monthly data integration")
        print(f"   Data available at: {self.base_url}")
        
        # Parse period (support YYYY or YYYY-MM format)
        if '-' in period:
            year, month = period.split('-')
        else:
            year = period
            month = '12'  # Default to December for annual queries
        
        # Generate realistic mock data based on state populations
        # Using metformin as baseline (common diabetes medication)
        mock_data = self._generate_state_data(drug_code)
        
        result = []
        for state_code, data in mock_data.items():
            if region and region.upper() != state_code:
                continue
            
            state_info = self.states[state_code]
            
            prescriber = Prescriber(
                id=f"AU-{state_code}",
                name=f"State: {state_info['name']}",
                type="State/Territory",
                location=f"{state_info['capital']}, {state_info['name']}, Australia"
            )
            
            prescribing = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=f"{year}-{month}",
                prescriptions=data['prescriptions'],
                quantity=data['quantity'],
                cost=data['cost']  # Cost in AUD
            )
            
            result.append(prescribing)
        
        return result
    
    def _generate_state_data(self, drug_code: str) -> Dict[str, Dict]:
        """
        Generate realistic mock data for states based on population
        
        Uses population-proportional distribution with regional variations
        for prescribing rates (urban vs rural, age demographics, etc.)
        """
        # Base prescribing rate per 1,000 population (varies by drug)
        # Metformin (diabetes): ~25 per 1,000 people
        # Statins (cholesterol): ~30 per 1,000 people
        
        base_rate = 25  # prescriptions per 1,000 population per year
        
        # Regional multipliers (account for age demographics, urban/rural mix)
        regional_factors = {
            'NSW': 1.05,   # Sydney + coastal, slightly higher
            'VIC': 1.02,   # Melbourne + regional
            'QLD': 1.10,   # Older population, high diabetes rates
            'WA': 0.95,    # Younger population
            'SA': 1.08,    # Older population
            'TAS': 1.15,   # Oldest population, highest rates
            'ACT': 0.85,   # Youngest population, health-conscious
            'NT': 0.90     # Remote, younger population
        }
        
        # Cost per prescription (AUD) - includes PBS subsidy + patient co-payment
        cost_per_rx = 42.50  # Average PBS prescription cost
        
        # Quantity per prescription (e.g., 60 tablets)
        quantity_per_rx = 60
        
        state_data = {}
        
        for state_code, state_info in self.states.items():
            population = state_info['population']
            factor = regional_factors[state_code]
            
            # Calculate prescriptions (annual)
            annual_prescriptions = int((population / 1000) * base_rate * factor)
            
            state_data[state_code] = {
                'prescriptions': annual_prescriptions,
                'quantity': annual_prescriptions * quantity_per_rx,
                'cost': annual_prescriptions * cost_per_rx
            }
        
        return state_data
    
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        """Get state/territory details"""
        result = []
        for state_id in prescriber_ids:
            state_code = state_id.replace('AU-', '')
            if state_code in self.states:
                state_info = self.states[state_code]
                prescriber = Prescriber(
                    id=state_id,
                    name=f"State: {state_info['name']}",
                    type="State/Territory",
                    location=f"{state_info['capital']}, {state_info['name']}, Australia"
                )
                result.append(prescriber)
        return result
    
    def get_latest_period(self) -> str:
        """
        Get most recent data period
        
        PBS data is published monthly with ~2 month lag
        """
        return "2024-10"  # October 2024 (example)
    
    def find_drug_code(self, name: str, prefer_generic: bool = True) -> Optional[str]:
        """
        Find ATC code for drug name
        
        Returns ATC code for querying
        """
        results = self.search_drug(name)
        if results:
            return results[0]['id']
        return name  # Use name as-is if no ATC found


# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_australia_data_source():
    """Test Australia PBS data source"""
    print("="*80)
    print("Testing Australia PBS Data Source")
    print("="*80)
    
    ds = AustraliaDataSource()
    
    print(f"\nTotal Population: {ds.total_population:,}")
    print(f"States/Territories: {len(ds.states)}")
    
    # Test drug search
    print(f"\n1. Search for 'metformin':")
    results = ds.search_drug('metformin')
    if results:
        print(f"   Found: {results[0]['name']} (ATC: {results[0]['id']}, PBS: {results[0]['pbs_code']})")
    
    # Test prescribing data
    print(f"\n2. Get state-level prescribing data (2023):")
    drug_code = ds.find_drug_code('metformin')
    data = ds.get_prescribing_data(drug_code, '2023')
    
    if data:
        print(f"   Found {len(data)} states/territories")
        
        # Calculate totals
        total_prescriptions = sum(d.prescriptions for d in data)
        total_cost = sum(d.cost for d in data)
        total_quantity = sum(d.quantity for d in data)
        
        print(f"\n   National Totals:")
        print(f"   Total Prescriptions: {total_prescriptions:,}")
        print(f"   Total Cost: ${total_cost:,.0f} AUD")
        print(f"   Total Quantity: {total_quantity:,} units")
        print(f"   Rx per capita: {total_prescriptions/ds.total_population*1000:.1f} per 1,000 people")
        
        print(f"\n   Top 5 States by Volume:")
        sorted_data = sorted(data, key=lambda d: d.prescriptions, reverse=True)
        for i, d in enumerate(sorted_data[:5], 1):
            share = (d.prescriptions / total_prescriptions) * 100
            print(f"   {i}. {d.prescriber.name}: {d.prescriptions:,} Rx ({share:.1f}%)")
    
    # Test specific state filter
    print(f"\n3. Test state filter (New South Wales):")
    nsw_data = ds.get_prescribing_data(drug_code, '2023', region='NSW')
    if nsw_data:
        print(f"   ✓ {nsw_data[0].prescriber.name}")
        print(f"   Prescriptions: {nsw_data[0].prescriptions:,}")
        print(f"   Cost: ${nsw_data[0].cost:,.0f} AUD")
    
    # Test monthly data
    print(f"\n4. Test monthly data (2023-12):")
    monthly_data = ds.get_prescribing_data(drug_code, '2023-12')
    if monthly_data:
        total_monthly = sum(d.prescriptions for d in monthly_data)
        print(f"   ✓ December 2023 data retrieved")
        print(f"   Total prescriptions: {total_monthly:,}")
    
    print("\n" + "="*80)
    print("✅ Australia PBS Data Source Test Complete")
    print("="*80)


if __name__ == "__main__":
    test_australia_data_source()
